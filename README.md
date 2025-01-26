# README2KG Template Project

This repository hosts the template project used for the [README2KG Shared Task](https://www.codabench.org/competitions/4925/) hosted on [Condabench](https://www.codabench.org).


# Contents

The contents of this repository includes scripts and data files used for the aforementioned competition:
* The dataset used for README2KG can be found in [readme2kg_template/data](https://github.com/chenzongxiong/readme2kg_template/blob/main/data)
* List of scripts:
    1. A [scoring script](https://github.com/chenzongxiong/readme2kg_template/blob/main/run_scoring.sh) is provided to allow participants to evaluate their NER system locally.
    2. [src/predictor.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/predictor.py) directory contains a sample source code for parsing and writing WebAnno TSV files.
    3. [src/scoring.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/scoring.py) is based on the seqeval sequence labeling evaluation strategy for NER systems using the BIO tagging scheme. 
    4. [src/utils.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/utils.py) contains methods used by `predictor.py`.
    5. [src/webanno_tsv.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/webanno_tsv.py) is adapted from [neuged/webanno_tsv](https://github.com/neuged/webanno_tsv/tree/master) to handle reading and generation of the dataset used in the README2KG Shared Task. 


# Usage

To run the scoring script directly:
      `python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction`
