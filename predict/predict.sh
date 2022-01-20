#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python predict_detail.py \
       --predict_text_file ../example/data/corpus.txt \
       --predict_match_file ../example/data/corpus_tagged.txt \
       --clean_term_path  ../example/cleanterms/cleanterms.txt.example \
       --model_name_or_path $HOME/models/pubmedbert_abs \
       --save_model_folder $HOME/models/lr0.0001_mask0.5_debugAlphamin-word-count-2 \
       --output output/
