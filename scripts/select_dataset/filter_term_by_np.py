#  通过np的结果对字典树匹配的术语进行过滤: 匹配术语和np一致才标注语义类型
import json

text_path = 'term_indexing_text.txt'
text_tagged_path = 'term_indexing_text_tagged.txt'
text_nps_path = 'term_indexing_text_nps.txt'

with open(text_path, 'r') as r:
    texts = r.readlines()
with open(text_tagged_path, 'r') as r:
    tagged_by_tries = r.readlines()
with open(text_nps_path, 'r') as r:
    tagged_by_nps = r.readlines()

print('texts ', len(texts))
print('tagged_by_trie ', len(tagged_by_tries))
print('tagged_by_np ', len(tagged_by_nps))

term2cnt = dict()
with open('term_indexing_text_filtered_by_np.txt', 'w') as w0:
    with open('term_indexing_tagged_filtered_by_np.txt', 'w') as w1:
        for i in range(len(texts)):
            text = texts[i]
            trie = tagged_by_tries[i]
            nps = tagged_by_nps[i]

            trie_json = json.loads(trie)
            nps_json = json.loads(nps)

            term = trie_json['phrase']
            if term2cnt.get(term, 0) >= 3:
                continue
            if len(term.split('\t')) >= 4 or trie_json in nps_json:
                term2cnt[term] = term2cnt.get(term, 0) + 1
                w0.write(text)
                w1.write(trie)

print('terms cnt filtered by np: ', len(term2cnt))

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
# 开始统计
sty2cnt = dict()
for term in term2cnt.keys():
    stys = term2sty[term]
    for sty in stys:
        sty2cnt[sty] = sty2cnt.get(sty, 0) + 1

print('出现的语义类型个数: ', len(sty2cnt))
print('不同语义类型术语句子的分布占比: ')
for sty, cnt in sty2cnt.items():
    print(sty + ', ' + str(cnt) + ', ' + str(round(cnt / len(term2cnt), 4)))

