#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python -u train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '../data/train_text_exclude_eval.txt' \
	--train_match_file '../data/train_text_exclude_eval_tagged.txt' \
        --eval_text_file '../data/eval_text.txt' \
        --eval_match_file '../data/eval_text_tagged.txt' \
	--clean_term_path '../data/v1.2/merge_cleanterms.txt' \
	--output_dir 'output_merge_cleanterms' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 \
        --learning_rate 1e-4 \
        --train_epoch 1 \
        --save_step 5000 \
        --eval_step 5000 \
        > train.log 2>&1 
