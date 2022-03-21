import json
import pymysql

import pandas as pd

cleanterm_sty_path = 'cleanterms5_4ex02_stys.txt'


def get_sty_from_cleanterms():
    path = '/Users/xiaj/data/cleanterms/cleanterms5_4ex/cleanterms5_4ex02.txt'

    cleanterms = pd.read_csv(path, encoding='utf-8', sep='\t')
    sty_list = cleanterms['sty'].tolist()
    sty_uniq = list(set([sty for stys in sty_list for sty in stys.split('|')]))

    with open(cleanterm_sty_path, 'w') as w:
        w.write('\n'.join(sty_uniq))


def select_terms_from_umls():
    db = pymysql.connect(host='localhost', user='umlsuser', password='umls0902', database='umls')
    cursor = db.cursor()
    cursor.execute("SELECT CUI,STR,SAB FROM MRCONSO WHERE LAT='ENG'")
    data = cursor.fetchall()

    with open('umls_eng_str.txt', 'w') as w:
        for line in data:
            w.write(str(line) + '\n')

    cursor.close()
    db.close()


def select_sty_from_cui():
    db = pymysql.connect(host='localhost', user='umlsuser', password='umls0902', database='umls')
    cursor = db.cursor()

    with open('umls_eng_str.txt', 'r') as r:
        cui2stys = []
        for line in r:
            turpl = eval(line)
            cui = turpl[0]
            cursor.execute(f"SELECT CUI,STY FROM MRSTY WHERE CUI='{cui}'")
            data = cursor.fetchall()
            for x in data:
                cui2stys.append(x)

        with open('all_eng_semtypes.txt', 'w') as w:
            for l in cui2stys:
                w.write(str(l) + '\n')

    cursor.close()
    db.close()


def generate_other_sty():
    with open(cleanterm_sty_path, 'r') as r:
        lines = r.readlines()
        cleanterms_stys = set([sty.rstrip() for sty in lines])

    # print(cleanterms_stys)
    cui2str = {}
    with open('umls_eng_str.txt', 'r') as r:
        for line in r:
            cui, str, sab = eval(line)
            if cui in cui2str:
                cui2str[cui] += [str]
            else:
                cui2str.setdefault(cui, [str])
    print('all cui2str ', len(cui2str))

    with open('all_eng_semtypes.txt', 'r') as r:
        for line in r:
            cui, sty = eval(line)
            if sty in cleanterms_stys and cui in cui2str:
                cui2str.pop(cui)
    print('other cui2str ', len(cui2str))

    with open('otherterms.txt', 'w') as w:
        w.write('cui     str.lower       sty     sgr     upper   short.upper     cui.n   sgr.n   str.n\n')
        for cui, strs in cui2str.items():
            for str in strs:
                w.write('\t'.join([cui, str.lower(), 'Other', 'Other', '0', '0', '1', '1', '1']) + '\n')

    print('done')


if __name__ == '__main__':
    # get_sty_from_cleanterms()

    # select_terms_from_umls()

    # select_sty_from_cui()

    generate_other_sty()
