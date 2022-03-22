#  通过np的结果对字典树匹配的术语进行过滤: 匹配术语和np一致才标注语义类型
import json

text_path = 'term_indexing_text.txt'
tagged_path = 'term_indexing_text_tagged.txt'
tagged_by_np_path = 'term_indexing_text.txt_tagged_by_np.txt'

with open(text_path, 'r') as r:
    texts = r.readlines()
with open(tagged_path, 'r') as r:
    tagged_by_tries = r.readlines()
with open(tagged_by_np_path, 'r') as r:
    tagged_by_nps = r.readlines()

print('texts ', len(texts))
print('tagged_by_trie ', len(tagged_by_tries))
print('tagged_by_np ', len(tagged_by_nps))

terms = set()
with open('term_indexing_text_filtered_by_np.txt', 'w') as w0:
    with open('term_indexing_tagged_filtered_by_np.txt', 'w') as w1:
        for i in range(len(texts)):
            text = texts[i]
            trie = tagged_by_tries[i]
            nps = tagged_by_nps[i]

            trie_json = json.loads(trie)
            nps_json = json.loads(nps)

            if trie_json in nps_json:
                terms.add(trie_json['phrase'])
                w0.write(text)
                w1.write(trie)

print('terms cnt filtered by np: ', len(terms))
print('over')

