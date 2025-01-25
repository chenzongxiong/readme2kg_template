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
            label = self.predict(sentence=sent)
            # create the annotation instances
            annotation = utils.make_annotation(tokens=tokens, label=label)
            annotations.append(annotation)

        result = utils.make_webanno_document(
            annotations=annotations,
            sentences=doc.sentences,
            tokens=doc.tokens
        )

        return result

    def predict(self, sentence, **kwargs):
        # Random select a label from LABELS
        label = random.choice(LABELS)
        return label


if __name__ == "__main__":
    file_path = './data/231sm_Low_Resource_KBP_master_README.md.tsv'
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
