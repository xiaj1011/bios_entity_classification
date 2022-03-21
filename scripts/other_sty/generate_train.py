'''
按照实体来生成训练集和测试集。

医学实体部分：
    每句话只标记一个实体；
    每个实体最多有10句话；
    一句话可以用多次，防止实体覆盖太少；
Other部分：
    从旧的数据中抽取一些other类的实体即可


'''
import json

tagged_path = '/Users/xiaj/keyanzhushou/relation_extract/data/eval_text_tagged.txt'
text_path = '/Users/xiaj/keyanzhushou/relation_extract/data/eval_text.txt'

terms_sents_tagged = dict()

with open(tagged_path, 'r') as r0:
    with open(text_path, 'r') as r1:
        for text in r1:
            tagged = r0.readline()
            tagged_json = json.loads(tagged)

            for entity in tagged_json:
                term = entity['phrase']
                if term not in terms_sents_tagged or len(terms_sents_tagged.get(term)) < 10:
                    terms_sents_tagged[term] = [(text, entity)] + terms_sents_tagged.get(term, [])

print('all terms cnt ', len(terms_sents_tagged))

with open('term_indexing_text.txt', 'w') as w0:
    with open('term_indexing_text_tagged.txt', 'w') as w1:
        for term, sents in terms_sents_tagged.items():
            for sent, entity in sents:
                w0.write(sent)
                w1.write(json.dumps(entity) + '\n')

with open('terms_cnt.txt', 'w') as w:
    len1cnt = 0
    for term, sents in terms_sents_tagged.items():
        w.write(str(len(sents)) + '\t' + term + '\n')
        if len(sents) == 1:
            len1cnt += 1

print('cnt 1 terms ', len1cnt)
print('cnt 1 terms ratio: ', len1cnt / len(terms_sents_tagged))
print('over')
