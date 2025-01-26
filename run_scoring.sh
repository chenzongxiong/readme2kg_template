#!/bin/bash

python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction
python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/missing_files
python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/dummy
python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/empty
