# BIOS_EntityClassification
## Contents

- [Overview](#overview)
- [Repo Contents](#repo-contents)
- [System Requirements](#system-requirements)
- [Installation Guide](#installation-guide)
- [Demo](#demo)
- [Results](#results)
- [License](./LICENSE)
- [Issues](https://github.com/ebridge2/lol/issues)
- [Citation](#citation)

## Overview
A Semantic Type Annotator(STA) to predict the semantic type of a medical term using the term
itself as well as its surrounding text as input. Training samples were multi-word terms from the 
UMLS, as they generally do not have ambiguous daily meaning. The semantic types of these 
terms were used as the label, and in case a term has multiple semantic types in the UMLS, a 
random one is used, leveraging the fact that a large sample size can overcome moderate noise 
in the data. The classification model was trained on PubMedBERT, a BERT model pretrained 
on PubMed abstracts.

## Repo Contents
- [pretrain](./pretrain): scripts for downloading pretrained models
- [example](./example): small dataset to demo the code
- [train](./train): train codes
- [predict](./predict): predict codes
- [utils](./utils): utils codes

## System Requirements
### Hardware Requirements
For optimal performance, we recommend a computer with following specs:
  
RAM: 16+ GB  
CPU: 4+ cores, 3.3+ GHz/core  
GPU Memory: 40 GB  

### Software requirements
The package is tested on `Linux 20.04` operating system.   
#### Install requirements
``
!pip install -r requirements.txt
``

## Installation Guide
  1. Download [cleanterms5.txt](https://pan.baidu.com/s/1e7hzcl6ZVTu_euwZBDVV2w) (password: d9ol) and put it under `./example/cleanterms/`.
  2. Download pretrained models: `cd pretrain && sh download_pubmedbert.sh`  
which will take about a few minutes to complete the download.
     
## Demo
### Train
make sure `cleanterms5.txt` has been downloaded, and then:  

```commandline
1. cd train
2. bash train.sh
```
after a few minutes, you can find your fine-tuned model and eval result under `./output_xxx` by default.

### Predict
configure your fine-tuned model path in the predict.sh, and then:
```commandline
1. cd predict
2. bash predict.sh
```
after a few minutes, you can find the results under `./output_xxx`

## Instructions for use
1. generate your cleanterms.txt from UMLS by your rules. and `python utils/label_util.py` to generate the `entity_type.json` 
and `entity_group.json`.
   
2. prepare your training texts and the FMM results.

3. use your datasets to train and predict!


## Citation
```text
@misc{https://doi.org/10.48550/arxiv.2203.09975,
  doi = {10.48550/ARXIV.2203.09975},
  url = {https://arxiv.org/abs/2203.09975},
  author = {Yu, Sheng and Yuan, Zheng and Xia, Jun and Luo, Shengxuan and Ying, Huaiyuan and Zeng, Sihang and Ren, Jingyi and Yuan, Hongyi and Zhao, Zhengyun and Lin, Yucong and Lu, Keming and Wang, Jing and Xie, Yutao and Shum, Heung-Yeung},
  keywords = {Computation and Language (cs.CL), Machine Learning (cs.LG), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {BIOS: An Algorithmically Generated Biomedical Knowledge Graph},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution Non Commercial Share Alike 4.0 International}
}
```


