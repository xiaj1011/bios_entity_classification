# EntityTypeClassification

Classify medical terms types with context.

语义分类模型是用于标注文本医学实体的语义类型，其中语义类型来自于UMLS.  

## Usage
在bios_ner项目的preprocess模块中，由corpus.txt经过字典树匹配生成corpus_tagged.txt之后，输入到本模型中，即可预测出corpus_annotated.txt结果，实现训练集的伪标注过程。

注：我们已经在pubmed语料上fine-tune好了一个模型，下载链接： 
链接: https://pan.baidu.com/s/1rWjYJIKFJPiqAE7dUL5WiQ  密码: t4gl

cleanterms 下载:
链接: https://pan.baidu.com/s/1GXnsSa_39nbX_YdJVnQh2g 密码: 4501

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

