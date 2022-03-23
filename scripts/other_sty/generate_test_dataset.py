'''
够，分离出3万术语当测试。而且我觉得不一定都用，可能每个术语用2句甚至1句就好，防止背词。
other可能也不用50万那么多，占正样本10-20%就可以了。

'''
import json
import random
import os

random.seed(1)

term_indexing_text_path = 'term_indexing_text_filtered_by_np.txt'
term_indexing_tagged_path = 'term_indexing_tagged_filtered_by_np.txt'

with open(term_indexing_tagged_path, 'r') as r:
    taggeds = r.readlines()
with open(term_indexing_text_path, 'r') as r:
    texts = r.readlines()

all_terms = set()
for tag in taggeds:
    tag_json = json.loads(tag)
    all_terms.add(tag_json['phrase'])


def generate_negative():
    other_terms_path = '/platform_tech/aigraph/entity_classification/data/otherterms_cleaned.txt'

    other_text_path = '/platform_tech/aigraph/entity_classification/data/train_text.txt'
    tagged_other_path = '/platform_tech/aigraph/entity_classification/data/train_text_tagged_by_25w_other.txt'

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

                for entity in tagged_json:
                    term = entity['phrase']
                    if term not in other_terms:
                        continue
                    if term not in otherterms_sents_tagged or len(otherterms_sents_tagged.get(term)) < 5:
                        cnt += 1
                        otherterms_sents_tagged[term] = [(text, entity)] + otherterms_sents_tagged.get(term, [])

    print('negative sents ', cnt)

    negative_samples = [(k, v) for k, v in otherterms_sents_tagged.items()]
    random.shuffle(negative_samples)
    print('negative samples ', len(negative_samples))

    with open('negative_samples_for_test.txt', 'w') as w:
        with open('negative_samples_for_train.txt', 'w') as w1:
            test_negative_size = 3000  # 测试集3w个正样本术语，3k个负样本术语
            train_negative_size = 34000  # 训练集34w个正样本术语，3.4w个负样本术语
            for i, (term, sents) in enumerate(negative_samples):
                if i < test_negative_size:
                    for sent, entity in sents:
                        entity['sty'] = 'Other'
                        w.write(json.dumps((sent, [entity])) + '\n')
                elif i < train_negative_size:
                    for sent, entity in sents:
                        entity['sty'] = 'Other'
                        w1.write(json.dumps((sent, [entity])) + '\n')


def dump_test_terms():
    test_size = 30000

    print('all terms ', len(all_terms))
    test_terms = random.sample(list(all_terms), test_size)
    test_terms = set(test_terms)
    print('test terms ', len(test_terms))
    with open('test_terms.txt', 'w') as w:
        for term in test_terms:
            w.write(term + '\n')
    print('dump test terms, ', len(test_terms))
    return test_terms


def generate_eval():
    test_terms = set()
    with open('test_terms.txt', 'r') as r:
        for line in r:
            test_terms.add(line.strip())

    eval_text2tagged = []

    term_cnt = dict()
    for i in range(len(texts)):
        tagged = taggeds[i]
        tag_json = json.loads(tagged)
        term = tag_json['phrase']
        if term not in test_terms:
            continue

        if term not in term_cnt or term_cnt.get(term, 0) < 2:
            term_cnt[term] = 1 + term_cnt.get(term, 0)
        else:
            continue

        eval_text2tagged.append((texts[i], json.dumps([tag_json])))

    with open('negative_samples_for_test.txt', 'r') as r:
        for line in r:
            sent, taggs = json.loads(line)
            eval_text2tagged.append((sent, json.dumps(taggs)))

    random.shuffle(eval_text2tagged)

    with open(f'term_test.txt', 'w') as wt1:
        with open(f'term_test_tagged.txt', 'w') as wt2:
            for text, tagged in eval_text2tagged:
                wt1.write(text)
                wt2.write(tagged + '\n')

    print('test data over')


version = 'v3.2'
min_sentsize = 1


def generate_train():
    test_terms = set()
    with open('test_terms.txt', 'r') as r:
        for line in r:
            test_terms.add(line.strip())

    train_text2tagged = []

    term_cnt = dict()
    for i in range(len(texts)):
        tagged = taggeds[i]
        tag_json = json.loads(tagged)
        term = tag_json['phrase']
        if term in test_terms:
            continue

        if term not in term_cnt or term_cnt.get(term, 0) < min_sentsize:
            term_cnt[term] = 1 + term_cnt.get(term, 0)
        else:
            continue

        train_text2tagged.append((texts[i], json.dumps([tag_json])))

    with open('negative_samples_for_train.txt', 'r') as r:
        for line in r:
            sent, taggs = json.loads(line)
            train_text2tagged.append((sent, json.dumps(taggs)))

    random.shuffle(train_text2tagged)

    with open(f'term_train_{version}.txt', 'w') as wt1:
        with open(f'term_train_tagged_{version}.txt', 'w') as wt2:
            for text, tagged in train_text2tagged:
                wt1.write(text)
                wt2.write(tagged + '\n')

    print('train data over')


if __name__ == '__main__':
    # generate_negative()  # negative样例不够，重新跑字典树匹配other类
    # dump_test_terms()
    generate_eval()
    #
    # generate_train()
