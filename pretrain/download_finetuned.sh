#!/bin/bash

model_path=lr0.0001_mask0.5_debugAlphamin-word-count-2/model

if [ ! -d ${model_path} ]; then
  mkdir -p ${model_path}
fi

wget -P ${model_path} http://192.168.190.78:8010/lr0.0001_mask0.5_debugAlphamin-word-count-2/model/last.pth
