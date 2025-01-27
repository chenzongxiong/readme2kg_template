#!/bin/bash

mode="${1:-test}";

python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction

if [ "$mode" = "-debug" ];
then
    python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/missing_files
    python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/dummy
    python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/empty
fi;
