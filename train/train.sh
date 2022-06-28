#!/bin/bash

CUDA_VISIBLE_DEVICES='1' python -u train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '../example/data/2k_train_text.txt' \
	--train_match_file '../example/data/2k_train_match.txt' \
        --eval_text_file '../example/data/1k_test_text.txt' \
        --eval_match_file '../example/data/1k_test_match.txt' \
	--clean_term_path '../example/cleanterms/cleanterms5.txt' \
	--output_dir 'output' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 \
        --learning_rate 1e-4 \
        --train_epoch 2 \
        --save_step 10 \
        --eval_step 10 \
        > train.log 2>&1 &
