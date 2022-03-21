'''
1。 统计other类和其他类的词频的占比
2。 挑选2000句测试集，要求句子中的实体在训练集中没有出现过


0318版本：
因为500w训练集过大导致过拟合，本版本随机抽取300w行训练集，并扩大测试集。

'''
import json
import random

import pandas as pd

tagged_path = 'train_text_with_5w_other_tagged.txt'
text_path = 'train_text.txt'

merge_cleanterms_path = 'merge_cleanterms.txt'


def get_text2tagged():
    text2tagged = []
    with open(tagged_path, 'r') as r1:
        taggs = r1.readlines()
    with open(text_path, 'r') as r2:
        texts = r2.readlines()

    for i in range(len(taggs)):
        text = texts[i]
        tagg = json.loads(taggs[i])

        text2tagged.append((text, tagg))

    return text2tagged


def get_cleanterms():
    data = pd.read_csv(merge_cleanterms_path, sep='\t')
    terms = data['str.lower'].tolist()
    stys = data['sty'].tolist()

    return {str(term): sty for term, sty in zip(terms, stys)}


'''
v1: 所有的umls排除类术语 34w(清洗后)
matched all cnt    44646472
matched other cnt  34952914
sub 9,693,558
v2: 随机挑选一部分的umls排除类术语 5w
matched all cnt  27534720
matched other cnt  14,558,530
sub 12,976,190
'''


def stat_other_ratio(text2tagged: list, term2sty: dict):
    taggs = [tagg for _, tagg in text2tagged]

    matched_all_cnt = 0
    matched_other_cnt = 0
    match_terms_cnt = dict()
    for tagg in taggs:
        for entity in tagg:
            term = entity['phrase']
            matched_all_cnt += 1
            if term2sty.get(term) == 'Other':
                matched_other_cnt += 1

            if term in match_terms_cnt:
                match_terms_cnt[term] += 1
            else:
                match_terms_cnt.setdefault(term, 1)

    print('matched all cnt ', matched_all_cnt)
    print('matched other cnt ', matched_other_cnt)

    return match_terms_cnt


def get_test_from_train(use_text2tagged: list, term2sty: dict, match_terms_cnt: dict):
    tests = []
    tests_tagged = []
    trains = []
    trains_tagged = []
    for text, taggs in use_text2tagged:
        is_single = True
        all_other = True
        for entity in taggs:
            term = entity['phrase']
            sty = term2sty[term]
            if match_terms_cnt[term] > 1:
                is_single = False
                break

            if sty != 'Other':
                all_other = False

            entity['sty'] = sty

        if is_single and not all_other:
            tests.append(text)
            tests_tagged.append(taggs)
        else:
            trains.append(text)
            trains_tagged.append(taggs)

    return tests, tests_tagged, trains, trains_tagged


def get_test_from_drop(trains_tagged, drop_text2tagged: list, term2sty: dict, match_terms_cnt: dict):
    already_train_terms = set()
    for taggs in trains_tagged:
        for entity in taggs:
            term = entity['phrase']
            sty = term2sty[term]
            if sty != 'Other':
                already_train_terms.add(entity['phrase'])

    tests = []
    tests_tagged = []
    for text, taggs in drop_text2tagged:
        all_other = True
        is_new = True
        for entity in taggs:
            term = entity['phrase']
            sty = term2sty[term]
            if term in already_train_terms:
                is_new = False
                break

            if sty != 'Other':
                all_other = False

            entity['sty'] = sty

        if is_new and not all_other:
            tests.append(text)
            tests_tagged.append(taggs)

    return tests, tests_tagged


def generate_test(text2tagged: list, term2sty: dict, match_terms_cnt: dict):
    random.shuffle(text2tagged)
    print('shuffle ', len(text2tagged))
    use_text2tagged = text2tagged[:300 * 10000]
    drop_text2tagged = text2tagged[300 * 10000:]

    tests, tests_tagged, trains, trains_tagged = get_test_from_train(use_text2tagged, term2sty, match_terms_cnt)
    print('get tests from train ', len(tests))

    more_tests, more_tests_tagged = get_test_from_drop(trains_tagged, drop_text2tagged, term2sty, match_terms_cnt)
    print('get tests from drop ', len(more_tests))

    tests.extend(more_tests)
    tests_tagged.extend(more_tests_tagged)
    print('all tests ', len(tests))

    with open('eval_text_0318.txt', 'w') as w:
        for line in tests:
            w.write(line)
    with open('eval_text_tagged_0318.txt', 'w') as w:
        for line in tests_tagged:
            w.write(json.dumps(line) + '\n')

    print('test done')

    with open('train_text_exclude_eval_0318.txt', 'w') as w:
        for line in trains:
            w.write(line)
    with open('train_text_exclude_eval_tagged_0318.txt', 'w') as w:
        for line in trains_tagged:
            w.write(json.dumps(line) + '\n')

    print('over')


if __name__ == '__main__':
    text2tagged = get_text2tagged()
    term2sty = get_cleanterms()

    match_terms_cnt = stat_other_ratio(text2tagged, term2sty)

    generate_test(text2tagged, term2sty, match_terms_cnt)
