#  将准备好的negative样例加入train test数据集
import json
import random

nega_train_path = '../../other_sty/negative_samples_for_train.txt'
nega_test_path = '../../other_sty/negative_samples_for_test.txt'

train_path = '../train_text.txt'
train_tagged_path = '../train_text_tagged.txt'
test_path = '../test_text.txt'
test_tagged_path = '../test_text_tagged.txt'


def extract_nega(nega_path):
    docs = []
    entities = []
    with open(nega_path, 'r') as r:
        for line in r:
            doc, entity = json.loads(line)
            docs.append(doc)
            entities.append(entity)
    print('负样本： ', nega_path)
    print('docs: ', len(docs))
    return docs, entities


def read_data(text_path, tagged_path):
    docs = []
    entities = []
    with open(text_path, 'r') as rt:
        with open(tagged_path, 'r') as ra:
            text_lines = rt.readlines()
            tagged_lines = ra.readlines()

            for i in range(len(text_lines)):
                doc = text_lines[i]
                entity = json.loads(tagged_lines[i])
                docs.append(doc)
                entities.append([entity])  # 转成list，符合数据格式

    return docs, entities


# train
nega_docs, nega_entities = extract_nega(nega_train_path)
docs, entities = read_data(train_path, train_tagged_path)

nega_docs = nega_docs[:int(0.1 * len(docs))]
nega_entities = nega_entities[:int(0.1 * len(docs))]
print(f'train 负样本个数: {len(nega_docs)}, 正样本个数: {len(docs)}')

docs.extend(nega_docs)
entities.extend(nega_entities)

tuple_data = list(zip(docs, entities))
random.shuffle(tuple_data)

with open('final_train_text.txt', 'w') as w0:
    with open('final_train_text_tagged.txt', 'w') as w1:
        for doc, entity in tuple_data:
            w0.write(doc)
            w1.write(json.dumps(entity) + '\n')

print('add train ok, ', len(docs))

# test
nega_docs, nega_entities = extract_nega(nega_test_path)
docs, entities = read_data(test_path, test_tagged_path)

nega_docs = nega_docs[:int(0.1 * len(docs))]  # 保持测试集的Other比例和训练集相近
nega_entities = nega_entities[:int(0.1 * len(docs))]
print(f'test 负样本个数: {len(nega_docs)}, 正样本个数: {len(docs)}')

docs.extend(nega_docs)
entities.extend(nega_entities)

tuple_data = list(zip(docs, entities))
random.shuffle(tuple_data)

with open('final_train_text.txt', 'a+') as w0:
    with open('final_train_text_tagged.txt', 'a+') as w1:
        for doc, entity in tuple_data:
            w0.write(doc)
            w1.write(json.dumps(entity) + '\n')

print('append test to train ok, ', len(docs))

