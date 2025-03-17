# Evaluation

In this competition, the evaluation of your Named Entity Recognition (NER) predictions will be based on the labeled sentences in the each Readme file.
The evaluation process ensures that only the predictions that overlap with the labeled sentences are considered, and non-overlapping predictions are ignored.
Below, we explain the evaluation process in detail.

## Key Points of Evaluation

1. **Labeled vs. Unlabeled Sentences**

* Each README file contains both labeled sentences and unlabeled sentences.
* Only the labeled sentences are used for evaluation. Predictions on unlabeled sentences will be ignored.

2. **Entity-Specific Labeling**

* For each of the 10 entity types, only the sentences that have been labeled with that entity type are considered as labeled data for that entity.
* For example, if a sentence is labeled with *SOFTWARE*, it will be used to evaluate predictions for the *SOFTWARE* entity type, but not for other entity types unless they are also labeled in that sentence.

3. **Multiple Entity Types per Token**

* A single token (or character) can belong to multiple entity types. For example, a token might be labeled as both *SOFTWARE* and *PROJECT*.
* The evaluation treats each entity type independently. This means that different entity types are not rivals, and a token can be correctly predicted for multiple entity types.

4. **No Overlapping Positions for the Same Entity Type**

* While a token can belong to multiple entity types, it cannot have overlapping positions for the same entity type. For example, a token cannot be labeled as both "B-SOFTWARE" and "I-SOFTWARE" at the same time.

5. **Character-Level Annotations**

* Our annotations are character-level, meaning that each character in the text is labeled with the appropriate entity type(s).
* The evaluation is also based on the character-level BIO tagging scheme.

## Evaluation Process

1. **BIO Tagging Scheme**

* The evaluation uses the BIO tagging scheme (Begin, Inside, Outside) to represent entity spans.

* Each character in the text is labeled with:

    * B-ENTITY: The beginning of an entity.

    * I-ENTITY: Inside an entity.

    * O: Outside any entity.
* For example, here is the character-level BIO tagging for the sentence "The ACL 2023 paper uses Tensorflow." with tags for *CONFERENCE* and *SOFTWARE*.
    ```
        T   O
        h   O
        e   O
            O
        A   B-CONFERENCE
        C   I-CONFERENCE
        L   I-CONFERENCE
            I-CONFERENCE
        2   I-CONFERENCE
        0   I-CONFERENCE
        2   I-CONFERENCE
        3   I-CONFERENCE
            O
        p   O
        a   O
        p   O
        e   O
        r   O
            O
        u   O
        s   O
        e   O
        s   O
            O
        T   B-SOFTWARE
        e   I-SOFTWARE
        n   I-SOFTWARE
        s   I-SOFTWARE
        o   I-SOFTWARE
        r   I-SOFTWARE
        f   I-SOFTWARE
        l   I-SOFTWARE
        o   I-SOFTWARE
        w   I-SOFTWARE
        .   O
    ```
2. **Scoring Script**

* The scoring script (scoring.py) compares your predictions against the ground truth labels using the seqeval library, which is designed for sequence labeling tasks like NER.

* The script calculates the following evaluation metrics for each of the 10 entity type independently.

    * Precision: The percentage of predicted entities that are correct.

    * Recall: The percentage of actual entities that were correctly predicted.

    * F1-Score: The harmonic mean of precision and recall.

* These metrics are calculated for each of the 10 entity types separately.

3. **Handling Predictions out of the Labeled Sentences**:

* The evaluation script will automatically ignore predictions on unlabeled sentences. For example, if a sentence is not labeled with "Conference", any predictions for "Conference" in that sentence will not affect the evaluation for that entity type.
