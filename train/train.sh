#!/bin/bash

CUDA_VISIBLE_DEVICES=0 python train.py \
        --model_name_or_path "$HOME/models/pubmedbert_abs" \
        --train_text_file '../example/data/corpus.txt' \
	--train_match_file '../example/data/corpus_tagged.txt' \
	--clean_term_path '../example/cleanterms/cleanterms.txt.example' \
	--output_dir 'output' \
	--do_train \
	--device 'cuda:0' \
        --train_batch_size 512 
