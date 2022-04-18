from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

test_path = "/platform_tech/aigraph/entity_classification/train/output_sty_map_with_Other_v1_4500_nega_for_test_ep18_lr0.0001_minwordcount-1_maxstyn-3/eval/test-9000.csv"

y_true = []
y_pred = []

with open(test_path, 'r') as r:
    with open('error_cases.txt', 'w') as w:
        w.write('term\tlabel\tprediction\n\n')
        for line in r:
            s, term, y_p, y_t = line.strip().split('\t')
            y_pred.append(y_p)
            y_true.append(y_t)
            if y_p != y_t:
                w.write(term + '\t' + y_t + '\t' + y_p + '\n' + s + '\n')
                w.write('\n')

print('len samples ', len(y_true))

labels = sorted(list(set(y_true)))

# 混淆矩阵，其第i行和第j列条目指示真实标签为第i类且预测标签为第j类的样本数。
m = confusion_matrix(y_true, y_pred, labels=labels)

with open('confusion_matrix.txt', 'w') as w:
    w.write('\t'.join(labels) + '\n')
    for rows in m:
        for row in rows:
            w.write(str(row) + '\t')
        w.write('\n')

p_class, r_class, f_class, support_micro = precision_recall_fscore_support(
    y_true=y_true, y_pred=y_pred, labels=labels, average=None)

print(p_class)
print(r_class)
print(f_class)
print(support_micro)

with open('eval_result.csv', 'w') as w:
    w.write('\t'.join(['sty', 'number', 'precision', 'recall', 'f1']) + '\n')
    for i in range(len(labels)):
        label = labels[i]
        cnt = support_micro[i]
        p = round(p_class[i], 5)
        r = round(r_class[i], 5)
        f = round(f_class[i], 5)
        w.write('\t'.join([str(x) for x in [label, cnt, p, r, f]]) + '\n')

