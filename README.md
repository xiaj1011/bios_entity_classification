# EntityTypeClassification

Classify medical terms types with context.

语义分类模型是用于标注文本中医学实体的语义类型，其中语义类型来自于UMLS.  

## Background
在bios_ner项目的preprocess模块中，由corpus.txt经过字典树匹配生成corpus_tagged.txt之后，输入到本模型中，即可预测出corpus_annotated.txt结果，实现训练集的伪标注过程。

注：我们已经在pubmed语料上fine-tune好了一个模型，可以使用 `sh pretrain/download_finetuned.sh` 下载使用。

## Mask ratio

| Mask 概率 | 训练数据量 | 是否包含多sty训练数据 | 单sty实体sty准确率 | 单sty实体sgr准确率 | 多sty实体sty准确率 | 多sty实体sgr准确率 |
| :-------: | :--------: | :-------------------: | :----------------: | :----------------: | :----------------: | :----------------: |
|    0.0    |    100W    |         True          |       97.67        |       98.88        |       90.16        |       89.07        |
|   0.15    |    100W    |         True          |       97.51        |       98.91        |       90.94        |       87.99        |
|    1.0    |    100W    |         True          |       71.75        |       87.00        |       65.49        |       71.49        |
|    0.0    |    100W    |         False         |       97.58        |       99.08        |       27.95        |       27.46        |
|   0.15    |    100W    |         False         |       97.17        |       98.46        |       27.95        |       27.46        |
