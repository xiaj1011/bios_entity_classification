import json

def get_entity_type_from_train_file(cleanterms_path):
    sty_set = set()
    sty2sgr = {}
    with open(cleanterms_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]
    for line in lines:
        stys = line.split("\t")[2]
        sty_set.update(stys.split("|"))
        sgr = line.split("\t")[3]
        for sty in stys.split("|"):
            sty2sgr[sty] = sgr
    sty_list = list(sty_set)
    sty_list.sort()
    sty2id = {sty:idx for idx, sty in enumerate(sty_list)}
    with open("../example/cleanterms/entity_type.json", "w", encoding="utf-8") as f:
        json.dump(sty2id, f)
    with open("../example/cleanterms/entity_group.json", "w", encoding="utf-8") as f:
        json.dump(sty2sgr, f)


def get_entity_type_from_json():
    with open("../example/cleanterms/entity_type.json", "r", encoding="utf-8") as f:
        sty2id = json.loads(f.readline())
    with open("../example/cleanterms/entity_group.json", "r", encoding="utf-8") as f:
        sty2sgr = json.loads(f.readline())
    return sty2id, sty2sgr


def check_entity_type(cleanterms_path):
    sty_set = set()
    sty2sgr = {}
    with open(cleanterms_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]
    for line in lines:
        stys = line.split("\t")[2]
        sty_set.update(stys.split("|"))
        sgr = line.split("\t")[3]
        for sty in stys.split("|"):
            if not sty in sty2sgr:
                sty2sgr[sty] = set()
            sty2sgr[sty].update([sgr])
    print(sty2sgr)

if __name__ == "__main__":
    cleanterms_path = "../example/cleanterms/cleanterms5.txt"
    
    get_entity_type_from_train_file(cleanterms_path)
    
    check_entity_type(cleanterms_path)

