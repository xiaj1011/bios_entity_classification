#!/bin/bash

CUDA_VISIBLE_DEVICES='1' python -u train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '../scripts/other_sty/term_train_v5.1.txt' \
	--train_match_file '../scripts/other_sty/term_train_tagged_v5.1.txt' \
        --eval_text_file '../scripts/other_sty/term_test.txt' \
        --eval_match_file '../scripts/other_sty/term_test_tagged.txt' \
	--clean_term_path '../data/merge_cleanterms_25w_other.txt' \
	--output_dir 'output_merge_cleanterms_v5.1_ep3' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 \
        --learning_rate 1e-4 \
        --train_epoch 3 \
        --save_step 500 \
        --eval_step 500 \
        > train.log 2>&1 &
