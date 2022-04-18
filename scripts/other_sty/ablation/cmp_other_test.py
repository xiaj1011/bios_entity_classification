# 比较other的影响
# 都隔离训练集，一个有other,一个无other
import json
import random

test_text_path = '../term_test.txt'
test_tagged_path = '../term_test_tagged.txt'
train_text_path = '../term_train_v2.1.txt'
train_tagged_path = '../term_train_tagged_v2.1.txt'

with open(test_tagged_path, 'r') as r0:
    test_tagged_lines = r0.readlines()
with open(test_text_path, 'r') as r1:
    test_text_lines = r1.readlines()

test_tagged_lines_no_other = []
test_text_lines_no_other = []
for i, test_tagged in enumerate(test_tagged_lines):
    data = json.loads(test_tagged)[0]
    if data.get('sty', None) == 'Other':
        continue
    test_tagged_lines_no_other.append(test_tagged)
    test_text_lines_no_other.append(test_text_lines[i])
print('test tagged no other ', len(test_tagged_lines_no_other))
print('test text no other ', len(test_text_lines_no_other))

with open('no_other_test_text.txt', 'w') as w0:
    with open('no_other_test_tagged.txt', 'w') as w1:
        for i in range(len(test_text_lines_no_other)):
            w0.write(test_text_lines_no_other[i])
            w1.write(test_tagged_lines_no_other[i])

with open(train_tagged_path, 'r') as r0:
    train_tagged_lines = r0.readlines()
with open(train_text_path, 'r') as r1:
    train_text_lines = r1.readlines()
train_tagged_lines_no_other = []
train_text_lines_no_other = []
for i, train_tagged in enumerate(train_tagged_lines):
    data = json.loads(train_tagged)[0]
    if data.get('sty', None) == 'Other':
        continue
    train_tagged_lines_no_other.append(train_tagged)
    train_text_lines_no_other.append(train_text_lines[i])
print('train tagged no other ', len(train_tagged_lines_no_other))
print('train text no other ', len(train_text_lines_no_other))
with open('no_other_train_text.txt', 'w') as w0:
    with open('no_other_train_tagged.txt', 'w') as w1:
        for i in range(len(train_text_lines_no_other)):
            w0.write(train_text_lines_no_other[i])
            w1.write(train_tagged_lines_no_other[i])


print('over')

