import random
from collections import defaultdict
from webanno_tsv import webanno_tsv_read_file, Document, Annotation, Token
import utils

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


class BasePredictor:
    pass


class DummpyPredictor(BasePredictor):
    def __call__(self, doc: Document):
        annotations = []
        for sent in doc.sentences:
            tokens = doc.sentence_tokens(sent)
            # NOTE: PUT YOUR PREDICTION LOGIC HERE
            span_tokens, label = self.predict(sentence=sent, tokens=tokens)
            # create the annotation instances
            if span_tokens is None:
                continue

            annotation = utils.make_annotation(tokens=span_tokens, label=label)
            annotations.append(annotation)

        result = utils.make_webanno_document(
            annotations=annotations,
            sentences=doc.sentences,
            tokens=doc.tokens
        )

        return result

    def predict(self, sentence, tokens):
        '''
        Only predict one label for each sentence
        '''
        start_char = random.randint(tokens[0].start, tokens[-1].end - 1)
        end_char = random.randint(start_char + 1, tokens[-1].end)

        span_tokens = []
        for token in tokens:
            if token.end < start_char:
                continue
            if token.start > end_char:
                continue

            span_tokens.append(token)

        if len(span_tokens) == 0:
            return None, None

        first, last = span_tokens[0], span_tokens[-1]
        span_tokens = span_tokens[1:-1]
        if first.start < start_char:
            text = token.text[start_char - first.start:]
            if len(text) > 0:
                token = Token(idx=f'{first.idx}.99', sentence_idx=first.sentence_idx, start=start_char, end=first.end, text=text)
                span_tokens.insert(0, token)
        if last.end > end_char:
            text = token.text[:end_char-last.start]
            if len(text) > 0:
                token = Token(idx=f'{last.idx}.99', sentence_idx=last.sentence_idx, start=last.start, end=end_char, text=text)
                span_tokens.append(token)

        if len(span_tokens) == 0:
            return None, None

        # Random select a label from LABELS
        label = random.choice(LABELS)
        return span_tokens, label


if __name__ == "__main__":
    # Path to annotated files
    file_path = './data/train/231sm_Low_Resource_KBP_master_README.md.tsv'
    # Path to un-annotated files
    file_path = './data/test/231sm_Low_Resource_KBP_master_README.md.tsv'
    ref_doc = webanno_tsv_read_file(file_path)

    predictor = DummpyPredictor()
    predicted_doc = predictor(ref_doc)

    # Verify
    assert ref_doc.text == predicted_doc.text, 'content changed'
    assert len(ref_doc.sentences) == len(predicted_doc.sentences), 'sentences changed'
    assert len(ref_doc.tokens) == len(predicted_doc.tokens), 'tokens changed'
    for s1, s2 in zip(ref_doc.sentences, predicted_doc.sentences):
        assert s1 == s2, f'sentence changed, \n{s1}\n{s2}'

    for t1, t2 in zip(ref_doc.tokens, predicted_doc.tokens):
        assert t1 == t2, f'token changed: \n{t1}\n{t2}'

    print(f"Predicted {len(predicted_doc.annotations)} annotations")
    print(predicted_doc.annotations)
    prediction_path = 'results/prediction/231sm_Low_Resource_KBP_master_README.md.tsv'
    with open(prediction_path, 'w') as fd:
        fd.write(predicted_doc.tsv())
