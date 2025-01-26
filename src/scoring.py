import argparse
import json
import os
from functools import reduce
from webanno_tsv import webanno_tsv_read_file, Document, Annotation
from typing import List, Union
from seqeval.metrics import classification_report
from seqeval.scheme import IOB2


LABELS = [
    'CONFERENCE',
    'DATASET',
    'EVALMETRIC',
    'LICENSE',
    'ONTOLOGY',
    'PROGLANG',
    'PROJECT',
    'PUBLICATION',
    'SOFTWARE',
    'WORKSHOP'
]


def to_char_bio(src_path: str, ref_path: str) -> List[List[str]]:
    ref_doc = webanno_tsv_read_file(ref_path)

    # Parse the WebAnno TSV file
    doc = webanno_tsv_read_file(src_path)
    # Initialize a list to store character-level BIO tags
    bio_tags_list = []
    for target_label in LABELS:
        bio_tags = ['#'] * len(doc.text)  # Default to '#' for all characters
        # Pick interested sentences and default to 'O'
        for annotation in ref_doc.annotations:
            label = annotation.label
            if label != target_label:
                continue
            sentences = doc.annotation_sentences(annotation)
            for sentence in sentences:
                tokens = doc.sentence_tokens(sentence)
                start_char, end_char = tokens[0].start, tokens[-1].end
                bio_tags[start_char:end_char] = ['O'] * (end_char-start_char)

        for annotation in doc.annotations:
            label = annotation.label
            if label != target_label:
                continue

            start_token, end_token = annotation.tokens[0], annotation.tokens[-1]
            start_char = start_token.start
            end_char = end_token.end
            # Sanity check
            if ref_doc.text[start_char:end_char] != annotation.text:
                msg = f"ERROR: src: {src_path}, annotated '{annotation.text}', text: '{ref_doc.text[start_char:end_char]}'"
                print(msg)

            # Assign BIO tags to characters in the entity span
            if 'I-' in bio_tags[start_char]:
                # It's inside other ENTITY, skip it
                pass
            else:
                bio_tags[start_char] = f'B-{label}'  # Beginning of the entity

            for i in range(start_char + 1, end_char):
                bio_tags[i] = f'I-{label}'  # Inside the entity

        # Remove unannotated sentences from bio list.
        bio_tags = [x for x in filter(lambda x: x != '#', bio_tags)]
        if len(bio_tags) > 0:
            bio_tags_list.append(bio_tags)

    return bio_tags_list

def get_parse():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--reference_dir', type=str, help='Path to the reference data, e.g. training/validation/test data', required=True)
    parser.add_argument('--prediction_dir', type=str, help='Path to save the prediction results', required=True)
    parser.add_argument('--score_dir', type=str, help='Path to store scores', default='./results/scores')
    return parser


if __name__ == "__main__":
    parser = get_parse()
    args = parser.parse_args()

    ref_dir = args.reference_dir
    pred_dir = args.prediction_dir
    score_dir = args.score_dir

    os.makedirs(pred_dir, exist_ok=True)
    os.makedirs(score_dir, exist_ok=True)

    ref_file_names = sorted([fp for fp in os.listdir(ref_dir) if os.path.isfile(f'{ref_dir}/{fp}') and fp.endswith('.tsv')])

    if len(ref_file_names) == 0:
        raise Exception("ERROR: No reference files found, configuration error?")

    all_ref_bio_tags_list = []
    for ref_file_name in ref_file_names:
        src_path = os.path.join(ref_dir, ref_file_name)
        ref_path = src_path
        all_ref_bio_tags_list.append(to_char_bio(src_path, ref_path))

    pred_file_names = sorted([fp for fp in os.listdir(pred_dir) if os.path.isfile(f'{pred_dir}/{fp}') and fp.endswith('.tsv')])

    all_pred_bio_tags_list = []
    for idx, ref_file_name in enumerate(ref_file_names):
        try:
            src_path = os.path.join(pred_dir, ref_file_name)
            ref_path = os.path.join(ref_dir, ref_file_name)
            all_pred_bio_tags_list.append(to_char_bio(src_path, ref_path))
        except FileNotFoundError:
            nbr_labels = len(all_ref_bio_tags_list[idx])
            pred = []
            for label_idx in range(nbr_labels):
                pred.append(['O'] * len(all_ref_bio_tags_list[idx][label_idx]))
            print(f"WARN: {ref_file_name} is missing, fill 'O' list as default prediction")
            all_pred_bio_tags_list.append(pred)

    # Sanity checking
    for ref_list, pred_list in zip(all_ref_bio_tags_list, all_pred_bio_tags_list):
        for ref, pred in zip(ref_list, pred_list):
            assert len(ref) == len(pred)

    flatten_ref_bio_tags_list = reduce(lambda x, y: x + y, all_ref_bio_tags_list)
    flatten_pred_bio_tags_list = reduce(lambda x, y: x + y, all_pred_bio_tags_list)
    scores = classification_report(flatten_ref_bio_tags_list, flatten_pred_bio_tags_list, output_dict=True, scheme=IOB2)

    flatten_scores = {}
    for k1 in scores.keys():
        for k2 in scores[k1]:
            k = f'{k1}_{k2}'.replace(' ', '_')
            k = f'{k}'.replace('-', '_')
            if scores[k1][k2].dtype == float:
                flatten_scores[k] = float(scores[k1][k2])
            elif scores[k1][k2].dtype == int:
                flatten_scores[k] = int(scores[k1][k2])
            else:
                flatten_scores[k] = scores[k1][k2]

    print("Score: \n", json.dumps(flatten_scores, indent=2))
    with open(os.path.join(score_dir, 'scores.json'), 'w') as fd:
        json.dump(flatten_scores, fd, indent=2)
