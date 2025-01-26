from functools import reduce
from collections import defaultdict
from webanno_tsv import Document, Annotation, Token, Sentence
from typing import List
from dataclasses import replace


LABEL_IDS = defaultdict(int)
TOKEN_LABEL_IDS = {}


def get_label_id(label: str) -> int:
    global LABEL_IDS
    lid = LABEL_IDS[label]
    LABEL_IDS[label] += 1
    return lid


def get_layer_name():
    return 'de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity'


def get_field_name():
    return 'value'


def make_annotation(tokens: List[Token], label: str) -> Annotation:
    global TOKEN_LABEL_IDS

    key = f'{tokens[0].start},{tokens[-1].end},{label}'
    if key not in TOKEN_LABEL_IDS:
        lid = get_label_id(label)
        TOKEN_LABEL_IDS[key] = lid
    else:
        lid = TOKEN_LABEL_IDS[key]

    return Annotation(
        tokens=tokens,
        label=label,
        layer=get_layer_name(),
        field=get_field_name(),
        label_id=lid
    )


def make_webanno_document(sentences: List[Sentence], tokens: List[Token], annotations: List[Annotation]) -> Document:
    layer_defs = [('de.tudarmstadt.ukp.dkpro.core.api.ner.type.NamedEntity', ['identifier', 'value'])]

    annotations = reduce(lambda acc, item: acc if any(item.should_merge(existing) for existing in acc) else acc + [item], annotations, [])
    return Document(
        layer_defs=layer_defs,
        sentences=sentences,
        tokens=tokens,
        annotations=annotations,
    )


def replace_webanno_annotations(doc: Document, annotations: List[Annotation]) -> Document:
    doc = replace(doc, annotations=annotations)
    return doc
