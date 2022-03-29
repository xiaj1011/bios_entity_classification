# 选题json数据 转换成 predict格式数据
import json

xuanti_path = '/platform_tech/aigraph/keyanzhushou/entity_fixer/multi_parse/matched_topic_info_v5_with_entities_position.txt'

with open('xuanti_sentences.txt', 'w') as w0:
    with open('xuanti_sentences_tagged.txt', 'w') as w1:
        with open(xuanti_path, 'r') as r:
            for i, line in enumerate(r):
                if i > 10:
                    break
                data = json.loads(line)
                sent = data.get('topic_sentence')
                entities_with_sty = data.get('entities_with_sty')
                for entity in entities_with_sty:
                    entity['phrase'] = entity.pop('entity')

                w0.write(sent + '\n')
                w1.write(json.dumps(entities_with_sty) + '\n')

print('over')
