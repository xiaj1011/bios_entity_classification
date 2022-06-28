#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python predict_detail.py \
       --predict_text_file ../example/data/2k_train_text.txt \
       --predict_match_file ../example/data/2k_train_match.txt \
       --clean_term_path  ../example/cleanterms/cleanterms5.txt \
       --model_name_or_path $HOME/models/pubmedbert_abs \
       --save_model_folder ../train/output_lr0.0001_minwordcount-1_maxstyn-3/ \
       --output output_test_lr0.0001_minwordcount-1_maxstyn-3/ \
       > predict.log 2>&1 &
