'''
够，分离出3万术语当测试。而且我觉得不一定都用，可能每个术语用2句甚至1句就好，防止背词。
other可能也不用50万那么多，占正样本10-20%就可以了。

'''
import json
import random

test_size = 30000

term_indexing_text_path = 'term_indexing_text_filtered_by_np.txt'
term_indexing_tagged_path = 'term_indexing_tagged_filtered_by_np.txt'

all_terms = set()

with open(term_indexing_tagged_path, 'r') as r:
    taggeds = r.readlines()
with open(term_indexing_text_path, 'r') as r:
    texts = r.readlines()

for tag in taggeds:
    tag_json = json.loads(tag)
    all_terms.add(tag_json['phrase'])

print('all terms ', len(all_terms))

test_terms = random.sample(list(taggeds), test_size)
test_terms = set(test_terms)
print('test terms ', len(test_terms))

with open('eval_v2.txt', 'w') as we1:
    with open('eval_tagged_v2.txt', 'w') as we2:
        with open('train_v2.txt', 'w') as wt1:
            with open('train_tagged_v2', 'w') as wt2:
                train_term_cnt = dict()
                for i in range(len(texts)):
                    tagged = taggeds[i]
                    tag_json = json.loads(tag)
                    term = tag_json['phrase']

                    if term in test_terms:
                        we1.write(texts[i])
                        we2.write(tagged)
                    else:
                        if term not in train_term_cnt or train_term_cnt.get(term, 0) <= 2:
                            train_term_cnt[term] = 1 + train_term_cnt.get(term, 0)
                            wt1.write(texts[i])
                            wt2.write(tagged)
