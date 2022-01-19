import sys
sys.path.extend(["..", "../utils"])

from model import EntityTypeClassification
from transformers import AdamW, get_linear_schedule_with_warmup
from evaluation import model_eval
from data_util import Entity_Dataset, my_collate_fn
from tqdm import tqdm, trange
import torch
from torch import nn
import time
import os
import numpy as np
import argparse
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader
from load_cleanterms import CLEANTERMS
from label_util import get_entity_type_from_json
import json

def run(args):
    sty2id, sty2sgr = get_entity_type_from_json()
    sgr2sty_id = {}
    for value in sty2sgr.values():
        sgr2sty_id[value] = [0] * len(sty2id)
    for sty in sty2sgr.keys():
        sgr = sty2sgr[sty]
        sgr2sty_id[sgr][sty2id[sty]] = 1
    for value in sty2sgr.values():
        sgr2sty_id[value] = np.array(sgr2sty_id[value])

    id2sty = {id:sty for sty, id in sty2id.items()}
    cleanterms = CLEANTERMS(args.clean_term_path)
    predict_control_dict = {}
   # predict_control_dict = {'no_short_upper':True}
    #predict_control_dict = {'no_short_upper':True, 'min_entity_word_count':2}
    #predict_control_dict = {'no_short_upper':True, 'max_entity_word_count':1}

    predict_dataset = Entity_Dataset(args.predict_text_file, args.predict_match_file, cleanterms, args.model_name_or_path, mask_ratio=0.0, control_dict=predict_control_dict, debug=args.debug, lines=args.lines)
    predict_dataloader = DataLoader(predict_dataset, batch_size=args.train_batch_size, shuffle=False, collate_fn=my_collate_fn, num_workers=args.num_workers)
    model = torch.load(os.path.join(args.save_model_folder, 'model', 'last.pth')).to(args.device)

    shift_id = []
    with open(args.predict_match_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    if args.lines >= 0:
        lines = lines[0:min(1000000, args.lines)]
    else:
        if args.debug:
            lines = lines[0:1000000]

    for idx, line in tqdm(enumerate(lines)):
        entities = json.loads(lines[idx])
        flag = False
        for entity in entities:
            if predict_dataset.filter_entity(entity):
                flag = True
        if not flag:
            shift_id.append(idx)

    output_basename = os.path.basename(args.predict_text_file)
    if output_basename.endswith('.txt'):
        output_basename = output_basename[:-4]
    if args.lines >= 0:
        output_basename = output_basename + f"_line{args.lines}"
    if 'min_entity_word_count' in predict_control_dict:
        output_basename = output_basename + f"_min_word{predict_control_dict['min_entity_word_count']}"
    if 'max_entity_word_count' in predict_control_dict:
        output_basename = output_basename + f"_max_word{predict_control_dict['max_entity_word_count']}"
    output_basename = output_basename + "_annotated.txt"

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    output_match_file = os.path.join(args.output, output_basename)
    try:
        os.system(f'rm -rf {output_match_file}')
    except BaseException:
        pass

    start_idx = 0
    model.eval()
    now_json = []
    last_sentence_id = 0
    origin_id = 0

    with torch.no_grad():
        for batch in tqdm(predict_dataloader):
            end_idx = start_idx + batch[0].shape[0]
            sentence = torch.LongTensor(batch[0]).to(args.device)
            entity_mark = torch.LongTensor(batch[1]).to(args.device)
            labels = batch[2]

            label_sty_list = []
            for i in range(labels.shape[0]):
                stys = torch.arange(labels.shape[1]).to(args.device)[labels[i] == 1]
                label_sty_list.append([id2sty[sty.item()] for sty in stys])
            label_grp_list = [set([sty2sgr[sty] for sty in label_sty]) for label_sty in label_sty_list]

            logits = model.predict(sentence, entity_mark)
            predict_idx = torch.max(logits, dim=1)[1].cpu().detach().numpy().tolist()
            predict_sty = [id2sty[sty] for sty in predict_idx]
            predict_grp = [sty2sgr[sty] for sty in predict_sty]

            for i in range(labels.shape[0]):
                now_sentence_id = predict_dataset.map[start_idx + i]
                now_entity = predict_dataset.entities[start_idx + i]
                ava = np.array([0] * len(sty2id))
                for sty in label_sty_list[i]:
                    ava[sty2id[sty]] = 1
                tensor_ava = torch.LongTensor(ava).bool().to(logits.device)
                logits[i] = logits[i].masked_fill(mask=~tensor_ava, value=-1e9)
                predict_sty_i = torch.max(logits[i], 0)[1].item()
                now_entity['predict_type'] = predict_sty[i]
                now_entity['predict_sgr'] = predict_grp[i]
                if predict_grp[i] in label_grp_list[i]:
                    now_entity['legal_type'] = id2sty[predict_sty_i]
                else:
                    now_entity['legal_type'] = ''
                now_entity['label_type'] = "|".join(label_sty_list[i])
                now_entity['label_sgr'] = "|".join(list(label_grp_list[i]))
                if not now_entity['predict_type'] in now_entity['label_type'].split('|'):
                    now_entity['Type'] = "Wrong"
                else:
                    now_entity['Type'] = "Correct"
                if now_entity['predict_sgr'] in now_entity['label_sgr'].split('|'):
                    now_entity['Group'] = "Correct"
                else:
                    now_entity['Group'] = "Wrong"
                if now_sentence_id == last_sentence_id:
                    now_json.append(now_entity)
                else:
                    while origin_id in shift_id:
                        with open(output_match_file, 'a+', encoding='utf-8') as f:
                            f.write('[]\n')
                        origin_id += 1
                    with open(output_match_file, 'a+', encoding='utf-8') as f:
                        output_line = json.dumps(now_json).strip()
                        f.write(output_line + "\n")
                    now_json = []
                    sentence = predict_dataset.sentences[predict_dataset.map[start_idx + i]]
                    #now_json.append(sentence)
                    last_sentence_id = now_sentence_id
                    origin_id += 1
                    now_json.append(now_entity)
 
            start_idx = end_idx
    
        with open(output_match_file, 'a+', encoding='utf-8') as f:
            output_line = json.dumps(now_json).strip()
            f.write(output_line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--predict_text_file', type=str, default='example/data/corpus.txt')
    parser.add_argument('--predict_match_file', type=str, default='example/data/corpus_tagged.txt')
    parser.add_argument('--clean_term_path', type=str, default="example/cleanterms/cleanterms.txt.example")

    parser.add_argument('--debug', action="store_true")
    parser.add_argument('--lines', default=-1, type=int)
    parser.add_argument('--model_name_or_path', type=str, default='../pretrain/pubmedbert_abs/')
    parser.add_argument(
        "--save_model_folder",
        type=str,
        default="./output/lr0.0001_mask0.5_debugAlphamin-word-count-2",
    )
    parser.add_argument(
        "--window_size",
        default=32,
        type=int,
        help="Window size",
    )
    parser.add_argument(
        "--train_batch_size", default=512, type=int, help="Batch size per GPU/CPU for training.",
    )
    parser.add_argument("--device", type=str, default='cuda:0', help="device")
    parser.add_argument("--num_workers", default=1, type=int,
                        help="Num workers for data loader, only 0 can be used for Windows")
    parser.add_argument("--output", type=str, default="output")

    args = parser.parse_args()

    run(args)
