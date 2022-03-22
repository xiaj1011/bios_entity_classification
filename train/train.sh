#!/bin/bash

CUDA_VISIBLE_DEVICES='1' python -u train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '../data/v5_term_indexing/term_train_v5.txt' \
	--train_match_file '../data/v5_term_indexing/term_train_tagged_v5.txt' \
        --eval_text_file '../data/v5_term_indexing/term_eval_v5.txt' \
        --eval_match_file '../data/v5_term_indexing/term_eval_tagged_v5.txt' \
	--clean_term_path '../data/merge_cleanterms.txt' \
	--output_dir 'output_merge_cleanterms_v5_ep4' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 \
        --learning_rate 1e-4 \
        --train_epoch 4 \
        --save_step 500 \
        --eval_step 500 \
        > train_v5.log 2>&1 &
