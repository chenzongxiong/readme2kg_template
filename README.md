# README2KG Template Project

This repository hosts the template project used for the [README2KG Shared Task](https://www.codabench.org/competitions/4925/) hosted on [Condabench](https://www.codabench.org).


# Contents

The contents of this repository includes scripts and data files used for the aforementioned competition:
* The dataset used for README2KG can be found in [readme2kg_template/data](https://github.com/chenzongxiong/readme2kg_template/blob/main/data)
* [predictor.py](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/predictor.py) in the [src](https://github.com/chenzongxiong/readme2kg_template/blob/main/src/) directory contain a sample source code for parsing and writing WebAnno TSV files.
* A [scoring script](https://github.com/chenzongxiong/readme2kg_template/blob/main/run_scoring.sh) is also provided to allow participants to evaluate their NER system locally.


# Usage

To run the scoring script directly:
      `python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction`
