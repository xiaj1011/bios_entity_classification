#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python predict_detail.py \
       --predict_text_file ../example/data/corpus.txt \
       --predict_match_file ../example/data/corpus_c5.4ex02core_tagged.txt \
       --clean_term_path  /platform_tech/aigraph/cleanterms/c5_4ex/cleanterms5_4ex02.core.txt \
       --model_name_or_path $HOME/models/pubmedbert_abs \
       --save_model_folder ../train/output_c5.4ex02core_lr0.0001_minwordcount-1_maxstyn-3/ \
       --output output_test_lr0.0001_minwordcount-1_maxstyn-3/
