# Worked example (synthetic)

**Everything in this folder is synthetic.** The two radiology reports, their questions and answers were invented for this repository. They are not from MIMIC-III or RadQA and describe no real patient. They use the RadQA 1.0.0 JSON layout, so the scripts read them exactly as they read the real data.

## The input

[`radqa/test.json`](radqa/test.json): two invented reports (a chest radiograph and an abdominal ultrasound) in the SQuAD 2.0 layout RadQA uses. Each report has two paragraphs, the impression (`…_I` question ids) and the full report (`…_O`), and three questions per paragraph. An answer is a span with a character offset (`answer_start`); a question the paragraph cannot answer has `is_impossible: true` and no answers.

## Run the pipeline on it

```bash
pip install pandas nltk rouge_score
python3 -m nltk.downloader punkt_tab
python3 Preprocessing/radqa2qnli.py --radqa-dir examples/radqa --out-dir examples/out --splits test
python3 Preprocessing/build_radqnli.py --tsv-dir examples/out --out-dir examples/out --splits test
```

```
wrote examples/out/radqa_test.tsv
test: 54 pairs after cleaning; RadQNLI 14 (7 entailment + 7 not_entailment with ROUGE-1 >= 0.2)
  test_00: 7 entailment + 17 not_entailment
  test_01: 7 entailment + 16 not_entailment
  test_02: 7 entailment + 7 not_entailment
  test_03: 7 entailment + 4 not_entailment
```

`examples/out/` is git-ignored; three of its files are kept in [`expected/`](expected/) for comparison.

| Step | File | What it shows |
|---|---|---|
| 1. Pair every question with every sentence of its paragraph | [`expected/radqa_test.tsv`](expected/radqa_test.tsv) | `index`, `question`, `sentence`, `label`. The sentence that contains the answer start is `entailment`, all others `not_entailment`; every sentence is `not_entailment` for an unanswerable question. 60 pairs |
| 2. Drop header fragments, keep negatives with ROUGE-1 ≥ 0.2 | [`expected/radqa_test_rouge02.csv`](expected/radqa_test_rouge02.csv) | The RadQNLI format: `question`, `sentence`, `label`. Sentence splitting leaves `IMPRESSION: 1.` and `2.` as "sentences"; they are removed (60 → 54 pairs), then 7 of the 47 negatives pass the threshold |
| 3. Hardest test set (negatives with ROUGE-1 ≥ 0.3) | [`expected/R1/radqa_test_03.csv`](expected/R1/radqa_test_03.csv) | The file the ChatGPT notebooks read; they add a `predict` column with the model's answer |

## What the ROUGE filter keeps

ROUGE-1 F1 between the question and each sentence of its paragraph, for one question:

| Question | Sentence | Label | ROUGE-1 |
|---|---|---|---:|
| Is the bile duct dilated? | The bile duct keeps a normal calibre. | entailment | 0.500 |
| | The bile duct is 4 mm wide on this invented scan. | entailment | 0.500 |
| | The liver texture is even throughout. | not_entailment | **0.364** |
| | FINDINGS: Several mobile bright stones sit in the gallbladder, and its wall is thin. | not_entailment | 0.211 |
| | EXAMINATION: Ultrasound of the right upper abdomen. | not_entailment | 0.167 |
| | IMPRESSION: Gallstones without signs of inflammation in this invented example. | not_entailment | 0.000 |

Entailment pairs are always kept; the threshold only selects negatives. ROUGE-1 counts every word, so *The liver texture is even throughout.* reaches the hardest set (≥ 0.3) on *is* and *the* alone. Read the four difficulty levels as "more word overlap with the question", which is not always the same as "harder to reason about".

## The output format of a model run

The notebooks write the input CSV back with one more column, `predict`. Anything other than `entailment` or `not_entailment` (for example `Not entailment`, or a label followed by an explanation) is counted as `not_entailment` by the evaluation notebooks:

```
question,sentence,label,predict
Is the bile duct dilated?,The liver texture is even throughout.,not_entailment,not_entailment
Are there gallstones?,IMPRESSION: Gallstones without signs of inflammation in this invented example.,entailment,entailment
```

These two rows are written by hand to show the format; they are not model outputs.
