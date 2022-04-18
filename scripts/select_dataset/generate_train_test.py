#  构建train和test
import json
import random

random.seed(100)

# 载入cleanterms
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

# 读取文件
tagged_path = 'term_indexing_tagged_filtered_by_np.txt'
text_path = 'term_indexing_text_filtered_by_np.txt'

sty2termnum = dict()
with open(tagged_path, 'r') as r:
    for line in r:
        entity = json.loads(line)
        term = entity['phrase']
        sty = random.sample(term2sty[term], 1)[0]
        sty2termnum[sty] = sty2termnum.get(sty, 0) + 1
        
print('sty2terms ', len(sty2termnum))
for sty, num in sty2termnum.items():
    print(sty, ', ', num)

#  切分生成train test
ratio = 0.1
max_num = 5000

sty2chosenum = dict()

with open(text_path, 'r') as rt:
    with open(tagged_path, 'r') as ra:
        text_lines = rt.readlines()
        tagged_lines = ra.readlines()

tuple_lines = list(zip(text_lines, tagged_lines))
random.shuffle(tuple_lines)

train_terms = []
test_terms = []
with open('train_text.txt', 'w') as wt0:
    with open('train_text_tagged.txt', 'w') as wt1:
        with open('test_text.txt', 'w') as we0:
            with open('test_text_tagged.txt', 'w') as we1:
                for text_line, tagged_line in tuple_lines:
                    term = json.loads(tagged_line)['phrase']
                    sty = random.sample(term2sty[term], 1)[0]
                    cur_chose_num = sty2chosenum.get(sty, 0)
                    if cur_chose_num <= sty2termnum[sty] * ratio and \
                            cur_chose_num <= max_num:
                        sty2chosenum[sty] = sty2chosenum.get(sty, 0) + 1
                        we0.write(text_line)
                        we1.write(tagged_line)
                        test_terms.append(term)
                    else:
                        wt0.write(text_line)
                        wt1.write(tagged_line)
                        train_terms.append(term)

#  统计train的分布
sty2cnt = dict()
for term in set(train_terms):
    stys = term2sty[term]
    for sty in stys:
        sty2cnt[sty] = sty2cnt.get(sty, 0) + 1

print('\ntrain中出现的语义类型个数: ', len(sty2cnt))
print('train中不同语义类型术语句子的分布占比: ')
for sty, cnt in sty2cnt.items():
    print(sty + ', ' + str(cnt) + ', ' + str(round(cnt / len(train_terms), 4)))

#  统计test的分布
sty2cnt = dict()
for term in set(test_terms):
    stys = term2sty[term]
    for sty in stys:
        sty2cnt[sty] = sty2cnt.get(sty, 0) + 1

print('\ntest中出现的语义类型个数: ', len(sty2cnt))
print('test中不同语义类型术语句子的分布占比: ')
for sty, cnt in sty2cnt.items():
    print(sty + ', ' + str(cnt) + ', ' + str(round(cnt / len(test_terms), 4)))

