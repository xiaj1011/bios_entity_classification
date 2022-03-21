#  随机从other术语中挑选5w

import random

with open('otherterms_cleaned.txt', 'r') as r:
    cleanterms = r.readlines()
    select_cleanterms = random.sample(cleanterms[1:], 50000)

    with open('otherterms_cleaned_random_5w.txt', 'w') as w:
        w.write(cleanterms[0])
        w.writelines(select_cleanterms)

print('done')

with open('/platform_tech/aigraph/cleanterms/c5_4ex/cleanterms5_4ex02.core.txt', 'r') as r:
    lines = r.readlines()
    with open('merge_cleanterms.txt', 'w') as w:
        for line in lines:
            w.write(line)

        for line in select_cleanterms:
            w.write(line)
print('merge cleanterms and other terms done')