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

test_terms = random.sample(list(all_terms), test_size)
test_terms = set(test_terms)
print('test terms ', len(test_terms))

version = 'v5'
min_sentsize = 4

with open(f'term_eval_{version}.txt', 'w') as we1:
    with open(f'term_eval_tagged_{version}.txt', 'w') as we2:
        with open(f'term_train_{version}.txt', 'w') as wt1:
            with open(f'term_train_tagged_{version}.txt', 'w') as wt2:
                term_cnt = dict()
                for i in range(len(texts)):
                    tagged = taggeds[i]
                    tag_json = json.loads(tagged)
                    term = tag_json['phrase']

                    if term not in term_cnt or term_cnt.get(term, 0) < min_sentsize:
                        term_cnt[term] = 1 + term_cnt.get(term, 0)
                    else:
                        continue

                    if term in test_terms:
                        we1.write(texts[i])
                        we2.write(json.dumps([tag_json]) + '\n')
                    else:
                        wt1.write(texts[i])
                        wt2.write(json.dumps([tag_json]) + '\n')


def add_other_for_train():
    other_terms_path = '/platform_tech/aigraph/entity_classification/data/otherterms_cleaned.txt'

    other_text_path = '/platform_tech/aigraph/entity_classification/data/v1_train_data/train_text.txt'
    tagged_other_path = '/platform_tech/aigraph/entity_classification/data/v1_train_data/train_text_with_5w_other_tagged.txt'

    other_size = 10 * 10000

    other_terms = set()
    with open(other_terms_path, 'r') as r:
        _ = r.readline()
        for line in r:
            other_terms.add(line.split('\t')[1])

    otherterms_sents_tagged = dict()
    with open(tagged_other_path, 'r') as r0:
        with open(other_text_path, 'r') as r1:
            cnt = 0
            for text in r1:
                tagged = r0.readline()
                tagged_json = json.loads(tagged)

                if cnt > other_size:
                    break

                for entity in tagged_json:
                    term = entity['phrase']
                    if term not in other_terms:
                        continue
                    if term not in otherterms_sents_tagged or len(otherterms_sents_tagged.get(term)) < 10:
                        cnt += 1
                        otherterms_sents_tagged[term] = [(text, entity)] + otherterms_sents_tagged.get(term, [])

    print('other term sents ', cnt)

    negative_samples = [(k, v) for k, v in otherterms_sents_tagged.items()]
    random.shuffle(negative_samples)
    print('negative samples ', len(negative_samples))

    with open(f'term_train_{version}.txt', 'a+') as w0:
        with open(f'term_train_tagged_{version}.txt', 'a+') as w1:
            for term, sents in negative_samples[:int(0.9 * len(negative_samples))]:
                for sent, entity in sents:
                    w0.write(sent)
                    entity['sty'] = 'Other'
                    w1.write(json.dumps([entity]) + '\n')

    with open(f'term_eval_{version}.txt', 'a+') as w0:
        with open(f'term_eval_tagged_{version}.txt', 'a+') as w1:
            for term, sents in negative_samples[int(0.9 * len(negative_samples)):]:
                for sent, entity in sents:
                    w0.write(sent)
                    entity['sty'] = 'Other'
                    w1.write(json.dumps([entity]) + '\n')


add_other_for_train()

print('over')

