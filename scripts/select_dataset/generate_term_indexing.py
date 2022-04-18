'''
按照实体来生成训练集和测试集。

医学实体部分：
    每句话只标记一个实体；
    每个实体最多有x句话；
    一句话可以用多次，防止实体覆盖太少；
Other部分：
    从旧的数据中抽取一些other类的实体即可


'''
import json

tagged_path = '/platform_tech/aigraph/bios_ner/tasks/data/pmd2021_0.5abs_0.3bulks_tagged_0411.txt'
text_path = '/platform_tech/aigraph/bios_ner/tasks/data/pmd2021_0.5abs_0.3bulks.txt'

terms_sents_tagged = dict()

with open(tagged_path, 'r') as r0:
    with open(text_path, 'r') as r1:
        for i, text in enumerate(r1):
            if i >= 10000 * 10000:
                break
                
            tagged = r0.readline()
            tagged_json = json.loads(tagged)

            for entity in tagged_json:
                term = entity['phrase']
                if term not in terms_sents_tagged or len(terms_sents_tagged.get(term)) < 10:
                    terms_sents_tagged[term] = [(text, entity)] + terms_sents_tagged.get(term, [])

print('all terms cnt ', len(terms_sents_tagged))

sents_num = 0
with open('term_indexing_text.txt', 'w') as w0:
    with open('term_indexing_text_tagged.txt', 'w') as w1:
        for term, sents in terms_sents_tagged.items():
            for sent, entity in sents:
                sents_num += 1
                w0.write(sent)
                w1.write(json.dumps(entity) + '\n')

# 统计分布
cleanterm_path = '/platform_tech/aigraph/cleanterms/c5_4ex/cleanterms5_4ex03_core_stymap.txt'

term2sty = dict()
with open(cleanterm_path, 'r') as r:
    _ = r.readline()
    for line in r:
        arrs = line.split('\t')
        term, stys = arrs[1], arrs[2]
        stys = set(stys.split('|'))
        if term in term2sty:
            term2sty[term].update(stys)
        else:
            term2sty.setdefault(term, stys)
print('cleanterms ', len(term2sty))

sty2cnt = dict()
for term in terms_sents_tagged.keys():
    stys = term2sty[term]
    for sty in stys:
        sty2cnt[sty] = sty2cnt.get(sty, 0) + 1

print('出现的语义类型个数: ', len(sty2cnt))
print('不同语义类型术语句子的分布占比: ')
for sty, cnt in sty2cnt.items():
    print(sty + ', ' + str(cnt) + ', ' + str(round(cnt / sents_num, 4)))

