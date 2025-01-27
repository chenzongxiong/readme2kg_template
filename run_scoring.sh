#!/bin/bash

mode="${1:-test}";

python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/prediction

if [ "$mode" = "-debug" ];
then
    python src/scoring.py --reference_dir ./data/train --prediction_dir ./results/missing_files
    python src/scoring.py --reference_dir ./data/val --prediction_dir ./results/dummy_all_sent_all_label
    python src/scoring.py --reference_dir ./data/val --prediction_dir ./results/dummy_all_doc_2_Software
fi;
