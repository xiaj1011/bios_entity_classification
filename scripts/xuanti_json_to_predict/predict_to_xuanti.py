# 将predict预测结果 写回到选题json中
import json

xuanti_predict_path = '/platform_tech/aigraph/entity_classification/predict/output_xuanti_v5_model_v2.1/xuanti_sentences_annotated.txt'

xuanti_path = '/platform_tech/aigraph/keyanzhushou/entity_fixer/multi_parse/matched_topic_info_v5_with_entities_position.txt'

with open(xuanti_path, 'r') as r:
    xuanti_lines = r.readlines()

with open(xuanti_predict_path, 'r') as r:
    with open('matched_topic_info_v5_with_entities_sty_0329.txt', 'w') as w:
        for i, tagged_line in enumerate(r):
            if i > 10:
                break
            entity_info = json.loads(tagged_line)
            entity_info.pop('legal_type')
            entity_info.pop('label_type')
            entity_info.pop('label_sgr')
            entity_info.pop('Type')
            entity_info.pop('Group')
            entity_info['entity'] = entity_info.pop('phrase')

            xuanti_line = xuanti_lines[i]
            xuanti_json = json.loads(xuanti_line)
            xuanti_json.update({'entities_with_sty': entity_info})

            w.write(json.dumps(xuanti_json) + '\n')

print('over')
