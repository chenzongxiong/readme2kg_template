# README2KG Template Project

This repository hosts the template project used for the [README2KG Shared Task](https://www.codabench.org/competitions/4925/) hosted on [Condabench](https://www.codabench.org).


# Contents

The contents of this repository includes scripts and data files used for the aforementioned competition:
* The dataset used for README2KG can be found in [readme2kg_template/data](https://github.com/chenzongxiong/readme2kg_template/blob/main/data)
* List of scripts:
    1. A [scoring script](run_scoring.sh) is provided to allow participants to evaluate their NER system locally.
    2. [src/TryMe.ipynb](src/TryMe.ipynb) gives simple read / write examples for parsing and writing WebAnno TSV files.
    3. [src/predictor.py](src/predictor.py) gives a sample source code for writing predictions in WebAnno TSV format. Please note that an annotation may start and end in the middle of a token, thus new tokens must be created. It is also possible that an annotation spans over more than one sentence.
    4. [src/utils.py](src/utils.py) contains methods used by `predictor.py`.
    5. [src/webanno_tsv.py](webanno_tsv.py) is adapted from [neuged/webanno_tsv](https://github.com/neuged/webanno_tsv/tree/master) to handle reading and generation of the dataset used in the README2KG Shared Task. 


# Usage

To run the scoring script directly:
      `python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction`
