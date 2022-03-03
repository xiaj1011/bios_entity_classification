#!/bin/bash

CUDA_VISIBLE_DEVICES=1 python train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '/platform_tech/aigraph/data/entity_type_classify/sty_classifer_train_text_0303.txt' \
	--train_match_file '/platform_tech/aigraph/bios_ner/preprocess/task_sty_cls/sty_classifer_train_text_0303_tagged.txt' \
	--clean_term_path '/platform_tech/aigraph/cleanterms/c5_4ex/cleanterms5_4ex.txt' \
	--output_dir 'output-c5.4ex-0303' \
	--do_train \
	--device 'cuda:1' \
        --train_batch_size 512 
