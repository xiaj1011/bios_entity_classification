#!/bin/bash

dst=$HOME/models/lr0.0001_mask0.5_debugAlphamin-word-count-2
if [ -d $dst ]; 
then
  echo "$dst already exists, skip download"
  exit 0
fi

wget -P $HOME/models -N -nH -r -R index.html* http://192.168.190.78:8010/lr0.0001_mask0.5_debugAlphamin-word-count-2/
