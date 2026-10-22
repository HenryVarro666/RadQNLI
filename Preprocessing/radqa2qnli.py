import json
import os
from nltk import tokenize

def convert_to_qnli(radqa_file, qnli_file):
    with open(radqa_file, 'r', encoding='utf-8') as f:
        radqa_data = json.load(f)['data']

    if os.path.exists(qnli_file):
        os.remove(qnli_file)

    with open(qnli_file, 'w', encoding='utf-8') as f:
        f.write("index\tquestion\tsentence\tlabel\n")
        index = 0
        for item in radqa_data:
            for paragraph in item['paragraphs']:
                context = paragraph['context'].replace('\n', ' ')
                sentences = tokenize.sent_tokenize(context)
                for qa in paragraph['qas']:
                    question = qa['question']
                    if qa['is_impossible']:
                        label = 'not_entailment'
                        ans = ''
                    elif len(qa['answers']) == 0:
                        label = 'not_entailment'
                        ans = ''
                    else:
                        label = 'entailment'
                        ans = qa['answers'][0]['text']
                        answer_start = qa['answers'][0]['answer_start']
                        sentence_index = None
                        for i, sentence in enumerate(sentences):
                            if answer_start >= context.index(sentence) and answer_start < context.index(sentence) + len(sentence):
                                sentence_index = i
                                break
                        if sentence_index is not None:
                            for i, sentence in enumerate(sentences):
                                if i == sentence_index:
                                    label = 'entailment'
                                else:
                                    label = 'not_entailment'
                                sample = f"{index}\t{question}\t{sentence}\t{label}"
                                f.write(f"{sample}\n")
                                index += 1
                    if not ans:
                        for i, sentence in enumerate(sentences):
                            label = 'not_entailment'
                            sample = f"{index}\t{question}\t{sentence}\t{label}"
                            f.write(f"{sample}\n")
                            index += 1
                index += 1

if __name__ == '__main__':
    # RadQA {split}.json -> radqa_{split}.tsv (index, question, sentence, label) for each split.
    # The defaults reproduce the 2023 layout: raw_RadQA/ at the repository root, output here.
    import argparse
    ap = argparse.ArgumentParser(description='Convert RadQA (SQuAD-style JSON) to QNLI-style sentence pairs.')
    ap.add_argument('--radqa-dir', default='../raw_RadQA', help='folder with train.json, dev.json, test.json')
    ap.add_argument('--out-dir', default='.', help='where radqa_{split}.tsv is written')
    ap.add_argument('--splits', nargs='+', default=['train', 'dev', 'test'])
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    for split in args.splits:
        convert_to_qnli(os.path.join(args.radqa_dir, f'{split}.json'),
                        os.path.join(args.out_dir, f'radqa_{split}.tsv'))
        print('wrote', os.path.join(args.out_dir, f'radqa_{split}.tsv'))
