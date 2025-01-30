# README2KG Template Project

This repository hosts the template project used for the [README2KG Shared Task](https://www.codabench.org/competitions/5396/) hosted on [Condabench](https://www.codabench.org).


# Contents

The contents of this repository include scripts and data files used for the aforementioned competition:
* The dataset used for README2KG can be found in [readme2kg_template/data](https://github.com/chenzongxiong/readme2kg_template/blob/main/data)
* List of scripts:
    1. The official scoring script [src/scoring.py](src/scoring.py) allows participants to evaluate their NER system locally before uploading the prediction to Codabench.
    2. [src/TryMe.ipynb](src/TryMe.ipynb) gives simple read / write examples for parsing and writing WebAnno TSV files.
    3. [src/predictor.py](src/predictor.py) gives a sample source code for writing predictions in WebAnno TSV format. Please note that an annotation may start and end in the middle of a token. It is also possible that an annotation spans more than one sentence.
    4. [src/utils.py](src/utils.py) contains methods used by `predictor.py`.
    5. [src/webanno_tsv.py](webanno_tsv.py) is adapted from [neuged/webanno_tsv](https://github.com/neuged/webanno_tsv/tree/master) to handle reading and generation of the dataset used in the README2KG Shared Task.


# Usage
## Setup
We use [poertry](https://python-poetry.org/docs/) to manage our template project by default.

```
conda create --name readme poetry
poetry install
```

Or
use `pip` to install dependencies

```
pip install -r requirements.txt
```

## Run Dummy Predictor
You can use the [dummy predictor](src/predictor.py) give in the template to generate the prediction

```
python src/predictor.py
```

## Run Scoring
To run the scoring script directly:
```
python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction
```

The scoring script is exactly the same as we used in codabench to evaluate the results.
