# 不包含other
# 1。 隔离： 测试集：把term_test_tagged.txt的other去掉；训练集：把term_train_tagged_v2.1.txt的other去掉
# 2. 不隔离：把上述去掉other的测试集和训练集混合打乱，拆成1。中相等数量的测试集和训练集
import json
import random

test_text_path = '../term_test.txt'
test_tagged_path = '../term_test_tagged.txt'
train_text_path = '../term_train_v5.1.txt'
train_tagged_path = '../term_train_tagged_v5.1.txt'

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

#  隔离测试集
with open('geli_test_tagged_no_other.txt', 'w') as w0:
    with open('geli_test_text_no_other.txt', 'w') as w1:
        with open('geli_train_tagged_no_other.txt', 'w') as w3:
            with open('geli_train_text_no_other.txt', 'w') as w4:
                for i in range(len(test_text_lines_no_other)):
                    w0.write(test_tagged_lines_no_other[i])
                    w1.write(test_text_lines_no_other[i])
                for i in range(len(train_text_lines_no_other)):
                    w3.write(train_tagged_lines_no_other[i])
                    w4.write(train_text_lines_no_other[i])

test_size = len(test_text_lines_no_other)

# 不隔离测试集
train_text_lines_no_other.extend(test_text_lines_no_other)
train_tagged_lines_no_other.extend(test_tagged_lines_no_other)

dataset = list(zip(train_text_lines_no_other, train_tagged_lines_no_other))

random.shuffle(dataset)

with open('bugeli_test_tagged_no_other.txt', 'w') as w0:
    with open('bugeli_test_text_no_other.txt', 'w') as w1:
        with open('bugeli_train_tagged_no_other.txt', 'w') as w3:
            with open('bugeli_train_text_no_other.txt', 'w') as w4:
                for i in range(len(dataset)):
                    text_line, tagged_line = dataset[i]
                    if i < test_size:
                        w0.write(tagged_line)
                        w1.write(text_line)
                    else:
                        w3.write(tagged_line)
                        w4.write(text_line)

print('over')

