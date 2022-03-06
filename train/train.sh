#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python -u train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '/platform_tech/aigraph/bios_ner/tasks/ner_v1.6.0/sty_classifer_train_text.txt' \
	--train_match_file '/platform_tech/aigraph/bios_ner/tasks/ner_v1.6.0/sty_classifer_train_text_tagged.txt' \
        --eval_text_file '../eval_data/eval_text.txt' \
        --eval_match_file '../eval_data/eval_text_tagged.txt' \
	--clean_term_path '/platform_tech/aigraph/cleanterms/c5_4ex/cleanterms5_4ex02.core.txt' \
	--output_dir 'output_c5.4ex02core' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 \
        --learning_rate 1e-4 \
        --train_epoch 2 \
        > train.log 2>&1 &
