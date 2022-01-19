#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python predict_detail.py \
       --predict_text_file ../example/data/corpus.txt \
       --predict_match_file ../example/data/corpus_tagged.txt \
       --clean_term_path  ../example/cleanterms/cleanterms.txt.example \
       --save_model_folder ../pretrain/lr0.0001_mask0.5_debugAlphamin-word-count-2 \
       --output output/
