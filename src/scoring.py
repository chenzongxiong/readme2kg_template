import argparse
import json
import os
from collections import defaultdict
from functools import reduce
from webanno_tsv import webanno_tsv_read_file, Document, Annotation
from typing import List, Union
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


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


def flatten(lst):
    return reduce(lambda x, y: x + y, lst)


def to_char_bio(src_path: str, ref_path: str) -> List[List[str]]:
    ref_doc = webanno_tsv_read_file(ref_path)
    # Parse the WebAnno TSV file
    doc = webanno_tsv_read_file(src_path)
    # Initialize a list to store character-level BIO tags
    bio_tags_list = []
    for target_label in LABELS:
        bio_tags = ['#'] * len(ref_doc.text)  # Default to '#' for all characters
        # Pick interested sentences and default them to 'O'
        for annotation in ref_doc.annotations:
            label = annotation.label
            if label != target_label:
                continue
            sentences = ref_doc.annotation_sentences(annotation)
            for sentence in sentences:
                tokens = ref_doc.sentence_tokens(sentence)
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

            if 'I-' in bio_tags[start_char]:
                # Overlapping, it's annotated by another annotations, we connect them as one annotations
                pass
            else:
                if bio_tags[start_char] != '#':
                    # Assign BIO tags to characters in the entity span
                    bio_tags[start_char] = f'B-{label}'  # Beginning of the entity

            for i in range(start_char + 1, end_char):
                if bio_tags[i] != '#':
                    bio_tags[i] = f'I-{label}'  # Inside the entity

        # Remove unannotated sentences from bio list.
        bio_tags = [x for x in filter(lambda x: x != '#', bio_tags)]
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
            assert nbr_labels == len(LABELS), "ERROR: reference tags doesn't have ${len(LABELS)} labels."
            pred = []
            for label_idx in range(nbr_labels):
                pred.append(['O'] * len(all_ref_bio_tags_list[idx][label_idx]))

            print(f"WARN: {ref_file_name} is missing, fill 'O' list as default prediction")
            all_pred_bio_tags_list.append(pred)
    # Sanity checking
    for idx, (ref_list, pred_list) in enumerate(zip(all_ref_bio_tags_list, all_pred_bio_tags_list)):
        for label_idx, (ref, pred) in enumerate(zip(ref_list, pred_list)):
            assert len(ref) == len(pred), f'ERROR: {ref_file_names[idx]}, label: {LABELS[label_idx]}, reference length: {len(ref)}, prediction length: {len(pred)}'

    scores = {}
    ################################################################################
    # Consider whole dataset
    ################################################################################
    ref_bio_tags_list = flatten(flatten(all_ref_bio_tags_list))
    pred_bio_tags_list = flatten(flatten(all_pred_bio_tags_list))

    accuracy = accuracy_score(ref_bio_tags_list, pred_bio_tags_list)
    scores['overall_accuracy'] = accuracy
    average = 'micro'
    ref_bio_tags_list = flatten(flatten(all_ref_bio_tags_list))
    pred_bio_tags_list = flatten(flatten(all_pred_bio_tags_list))

    f1 = f1_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
    precision = precision_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
    recall = recall_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
    scores[f"overall_{average}_precision"] = precision
    scores[f"overall_{average}_recall"] = recall
    scores[f"overall_{average}_f1"] = f1


    ################################################################################
    # For each class
    ################################################################################
    label_to_ref_bio_tags_list = defaultdict(list)
    label_to_pred_bio_tags_list = defaultdict(list)
    for ref_bio_tags_list, pred_bio_tags_list in zip(all_ref_bio_tags_list, all_pred_bio_tags_list):
        if len(ref_bio_tags_list) != len(LABELS):
            print('ERROR: ref bio tags list')
        if len(pred_bio_tags_list) != len(LABELS):
            print('ERROR: pred bio tags list')

        for label, ref_bio_tags, pred_bio_tags in zip(LABELS, ref_bio_tags_list, pred_bio_tags_list):
            label_to_ref_bio_tags_list[label].extend(ref_bio_tags)
            label_to_pred_bio_tags_list[label].extend(pred_bio_tags)
            if len(label_to_ref_bio_tags_list[label]) != len(label_to_pred_bio_tags_list[label]):
                print('ERROR: label_to_ref_pred_bio_tags')


    for label in label_to_ref_bio_tags_list.keys():
        ref_bio_tags_list = label_to_ref_bio_tags_list[label]
        pred_bio_tags_list = label_to_pred_bio_tags_list[label]
        accuracy = accuracy_score(ref_bio_tags_list, pred_bio_tags_list)
        f1 = f1_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
        precision = precision_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
        recall = recall_score(ref_bio_tags_list, pred_bio_tags_list, average=average)
        scores[f"{label}_{average}_precision"] = precision
        scores[f"{label}_{average}_recall"] = recall
        scores[f"{label}_{average}_f1"] = f1

    print("Scores:\n", json.dumps(scores, indent=2))

    with open(os.path.join(score_dir, 'scores.json'), 'w') as fd:
        json.dump(scores, fd, indent=2)
