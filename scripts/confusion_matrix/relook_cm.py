cm_path = 'confusion_matrix.txt'
eval_res_path = 'eval_result.csv'

sty2metrics = dict()
with open(eval_res_path, 'r') as r:
    _ = r.readline()
    for line in r:
        sty, cnt, p, r, f1 = line.strip().split('\t')
        sty2metrics.setdefault(sty, [cnt, p, r, f1])

with open(cm_path, 'r') as r:
    lines = r.readlines()
    titles = lines[0].strip().split('\t')
    values = lines[1:]

    with open('relook_cm.txt', 'w') as w:
        for i, title in enumerate(titles):
            w.write('=====' + title + "=====\n")
            cnt, p, r, f1 = sty2metrics.get(title)
            w.write('cnt:' + cnt + '\tp:' + p + '\tr:' + r + '\tf1:' + f1 + '\n')
            numbers = values[i].strip().split('\t')
            for j, num in enumerate(numbers):
                if int(num):
                    w.write(titles[j] + ':\t' + num + '\n')

            w.write('\n')

