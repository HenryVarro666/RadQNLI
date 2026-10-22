<div align="center">

# RadQNLI

**English** · [简体中文](README.zh-CN.md)

**Does a sentence from a radiology report answer the clinician's question? A benchmark for weighing one generic LLM against models fine-tuned on the task.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--3.5--turbo-412991)
![data](https://img.shields.io/badge/data-RadQA%20·%20PhysioNet%20credentialed%20(not%20included)-6E7781)
[![arXiv](https://img.shields.io/badge/arXiv-2304.09138-B31B1B)](https://arxiv.org/abs/2304.09138)
[![IEEE TBD](https://img.shields.io/badge/IEEE%20TBD-10.1109%2FTBDATA.2025.3536928-00629B)](https://doi.org/10.1109/TBDATA.2025.3536928)
[![homepage](https://img.shields.io/badge/homepage-ccao2679.com-555555)](https://www.ccao2679.com/research/#radqnli)

<img src="docs/figures/overview.png" alt="Overview poster: RadQA reports become question–sentence pairs, a ROUGE-1 filter keeps 9,838 of them, ChatGPT is prompted 3-shot on four difficulty levels; GPT-4 0.8420 vs fine-tuned BERT 0.8467 in the paper, and random controls fall almost as far as the ROUGE-filtered sets" width="100%">

</div>

<!-- problem-framing:start -->

## Problem and evidence

> **Does a question-inference model retain its ability to distinguish answer-supporting radiology text when negative examples are made harder without changing evaluation prevalence?**

**Why it matters:** A model can appear stronger because its test set contains easier negatives or a different class balance. Reliable comparison requires separating reasoning difficulty from sampling effects.

**Central tension:** Lexically similar negatives may test useful distinctions, but changing their selection can also alter topic, prevalence and annotation ambiguity.

[Full problem and verification plan](PROBLEM.md) · [中文](PROBLEM.zh.md)

<!-- problem-framing:end -->

## Highlights

- **A radiology NLI benchmark you can rebuild.** RadQA pairs clinicians' questions with MIMIC-III radiology reports (3,074 question–report pairs, 1,009 reports). RadQNLI splits each report into sentences and pairs every question with every sentence: `entailment` if the sentence holds the answer, `not_entailment` otherwise. Keeping all entailment pairs and the negatives that share words with the question (ROUGE-1 ≥ 0.2) gives **9,838 pairs** (4,391 entailment, 5,447 not): 7,911 train, 950 dev, 977 test. [`build_radqnli.py`](Preprocessing/build_radqnli.py) rebuilds exactly these pairs from RadQA 1.0.0.
- **The paper's answer: one generic model comes close.** In the IEEE Transactions on Big Data paper, GPT-4 with few-shot prompting plus IRSA (instruction-response semantic alignment) reached **0.8420** accuracy, against **0.8467** on average for BERT-family models fine-tuned on the full training data; trained on 10 samples, those models averaged 0.5181. The GPT-4, chain-of-thought, IRSA, open-LLM and fine-tuning code is not in this repository.
- **What this repository runs: ChatGPT against four difficulty levels.** gpt-3.5-turbo with three in-context examples, five runs per test set. Accuracy falls from **0.8100 to 0.6186** as the negatives share more words with the question (ROUGE-1 > 0 up to ≥ 0.3), the curve in the paper's Table 4.
- **The random controls explain most of that drop.** With the same number of negatives drawn at random, accuracy falls almost as far (**0.8297 → 0.6430**). Recall on entailment pairs stays at 0.52–0.53 on every set, so the decline mostly follows the rising share of entailment pairs (21% → 70%); word-overlap negatives cost 2–4 accuracy points against random ones of the same count. Separating the two is the question [PROBLEM.md](PROBLEM.md) sets up.
- **No report text in this repository.** RadQA and everything derived from it were removed from the whole history; [`examples/`](examples/) runs the pipeline on two invented reports.

## Results

ChatGPT (gpt-3.5-turbo), three in-context examples, mean of five runs; accuracy / F1 with `entailment` as the positive class. Every set holds the 460 entailment pairs of the RadQA test split.

| Test set | Negatives | Pairs (entailment + not) | Entailment share | ROUGE-filtered negatives (`R1/`) | Random negatives, same count (`Random_sample1/`) | Random, same count per question (`Random_sample2/`) |
|---|---|---|---:|---:|---:|---:|
| `test_00` | ROUGE-1 > 0 | 460 + 1,681 | 21% | 0.8100 / 0.5462 | 0.8297 / 0.5743 | 0.8268 / 0.5666 |
| `test_01` | ROUGE-1 ≥ 0.1 | 460 + 1,327 | 26% | 0.7934 / 0.5685 | 0.8121 / 0.5941 | 0.8108 / 0.5872 |
| `test_02` | ROUGE-1 ≥ 0.2 | 460 + 517 | 47% | 0.6986 / 0.6224 | 0.7339 / 0.6461 | 0.7247 / 0.6402 |
| `test_03` | ROUGE-1 ≥ 0.3 | 460 + 193 | 70% | 0.6186 / 0.6594 | 0.6430 / 0.6762 | 0.6389 / 0.6731 |

Recall stays between 0.5234 and 0.5321 in all twelve cells; precision rises with the entailment share (0.56 → 0.89 on the ROUGE-filtered sets). Per-run tables are in the original README below.

**How far to trust the averages.** These are the averages recorded in 2023 (the ROUGE-filtered column is the paper's Table 4). The 40 output files of the `R1/` and `Random_sample1/` runs were removed with the data because they quote the report sentences; before that, their confusion counts and metrics were recomputed and saved in [`results/chatgpt_3shot_runs.csv`](results/chatgpt_3shot_runs.csv), scored with each evaluation notebook's own rule. The recomputed means agree with the table to within 0.0022 accuracy and 0.0069 F1, but not exactly, and the ± values in the 2023 tables do not match the spread of the five runs listed above them. The `Random_sample2/` outputs were never saved, so that column cannot be checked.

**In-context examples.** The three demonstrations in the prompt are question–sentence pairs from reports in the RadQA *test* split, and they are also items of the test sets: three per set, except two in `test_03` and in the `Random_sample1/` sets. That is at most 3 of 653 items (0.5%). Their text is replaced by placeholders in the notebooks.

## How it works

| Step | What happens | Code |
|---|---|---|
| 1. Pair | Each RadQA paragraph (the impression, then the full report) is split into sentences with NLTK, and every question is paired with every sentence: the sentence that contains the answer start is `entailment`, the others `not_entailment`; for an unanswerable question every pair is `not_entailment` | [`Preprocessing/radqa2qnli.py`](Preprocessing/radqa2qnli.py) |
| 2. Clean | Header fragments that sentence splitting leaves behind (`IMPRESSION`, `IMPRESSION: 1.`, `2.` … `6.`, `Evaluation`) are dropped | [`Preprocessing/build_radqnli.py`](Preprocessing/build_radqnli.py) |
| 3. Filter | ROUGE-1 F1 (stemmed) between question and sentence for every negative. RadQNLI keeps all entailment pairs and the negatives with ROUGE-1 ≥ 0.2 (`radqa_{split}_rouge02.csv`) | `build_radqnli.py` |
| 4. Test sets | From the test split: all 460 entailment pairs plus the negatives with ROUGE-1 > 0, ≥ 0.1, ≥ 0.2 or ≥ 0.3 (`R1/`); controls with the same number of random negatives (`Random_sample1/`) or the same number per question (`Random_sample2/`); `random_state=42` throughout | `build_radqnli.py` |
| 5. Prompt | `openai.ChatCompletion` with gpt-3.5-turbo: a system prompt ("You are a radiologist…"), three demonstrations, then the pair; the reply should be `entailment` or `not entailment` and is rewritten to `not_entailment`. Five runs per set; the output CSV gains a `predict` column | [`R1/ChatGPT_Test.ipynb`](R1/ChatGPT_Test.ipynb), [`Random_sample1/ChatGPT_Test2.ipynb`](Random_sample1/ChatGPT_Test2.ipynb) |
| 6. Score | Any reply other than the two labels counts as `not_entailment`; accuracy, precision, recall and F1 with Hugging Face `evaluate` | [`R1/Evaluation_R1.ipynb`](R1/Evaluation_R1.ipynb), [`Random_sample1/Evaluation_RandomSample.ipynb`](Random_sample1/Evaluation_RandomSample.ipynb) |

ROUGE-1 counts every word, function words included, so a negative can reach the hardest set on *is* and *the* alone; [`examples/`](examples/README.md#what-the-rouge-filter-keeps) shows a case.

## Quick start

1. **Get RadQA.** It is a credentialed PhysioNet dataset: create a PhysioNet account, complete credentialing and the CITI "Data or Specimens Only Research" course, sign the data use agreement on the [RadQA 1.0.0 page](https://physionet.org/content/radqa/1.0.0/), then put `train.json`, `dev.json` and `test.json` in `raw_RadQA/` at the repository root (git-ignored).
2. **Install** the dependencies and the NLTK sentence splitter:

   ```bash
   pip install -r requirements.txt
   python3 -m nltk.downloader punkt_tab      # nltk < 3.8.2: punkt
   ```
3. **Build RadQNLI and the test sets** into `data/` (git-ignored):

   ```bash
   cd Preprocessing
   python3 radqa2qnli.py                     # ../raw_RadQA/*.json -> radqa_{train,dev,test}.tsv
   python3 build_radqnli.py                  # -> ../data/radqa_*_rouge02.csv, ../data/R1/, ../data/Random_sample{1,2}/
   ```

   It prints 7,911 / 950 / 977 RadQNLI pairs and test sets of 460 entailment pairs with 1,681 / 1,327 / 517 / 193 negatives.
4. **Run a model.** The notebooks are the 2023 Google Colab versions: they read `/content/drive/MyDrive/GPT_Data/…`, use the `openai<1.0` client and take the key from `OPENAI_API_KEY`. Point `input_file` and `output_file` at your copies, then score the outputs with the evaluation notebooks. Read [Data access and privacy](#data-access-and-privacy) before sending RadQNLI to any online service.

No credentials? [`examples/`](examples/) runs both scripts of step 3 on two invented reports and shows the file format of step 4.

## Data access and privacy

This repository holds **no RadQA text**. RadQA is derived from MIMIC-III and distributed by PhysioNet under the PhysioNet Credentialed Health Data License 1.5.0; the data use agreement forbids sharing the data, so bring your own credentialed copy. In October 2026 the RadQA archives, the converted pairs, every RadQNLI and test-set file, the ChatGPT output files and a scratch notebook were removed from the whole git history, and the few notebook passages that quoted reports (the three in-context demonstrations and some model explanations) were replaced by placeholders such as `[RadQA demonstration sentence 1, redacted]`. `.gitignore` keeps such files out; [`results/`](results/) holds metrics only.

Sending RadQNLI to an online model counts as sharing it with a third party under the agreement. PhysioNet's [guidance on LLMs and online services](https://physionet.org/news/post/llm-responsible-use/) recommends local models and allows a cloud API only with verified zero data retention, no training on the data and no human review.

## Repository layout

| Path | Purpose |
|---|---|
| `Preprocessing/radqa2qnli.py` | RadQA JSON → question–sentence pairs (`radqa_{split}.tsv`) |
| `Preprocessing/build_radqnli.py` | Header-fragment filter, ROUGE-1, RadQNLI splits, the four test sets and the random controls |
| `R1/` | ChatGPT run and evaluation notebooks for the ROUGE-filtered test sets |
| `Random_sample1/` | The same for the random controls (`Random_sample2/` used the same notebooks) |
| `Random_sample2/Error_outputs.md` | Off-format ChatGPT replies seen in the `Random_sample2/` runs, with that run's table |
| `Tools/` | Small helpers: relabel a TSV to `Yes.` / `No.`, and count the Yes/No ratio of an answer file |
| `results/chatgpt_3shot_runs.csv` | Per-run confusion counts and metrics of the 40 saved `R1/` and `Random_sample1/` runs |
| `examples/` | Two invented reports in the RadQA layout and the files the scripts make from them |
| `docs/figures/` | The overview poster |
| `PROBLEM.md` | The research question and the evaluation that would settle it ([中文](PROBLEM.zh.md)) |

## Citation

Z. Wu\*, L. Zhang\*, **C. Cao**\*, X. Yu, Z. Liu, L. Zhao, Y. Li, H. Dai, C. Ma, G. Li, W. Liu, Q. Li, D. Shen, X. Li, D. Zhu, T. Liu. *Exploring the Trade-Offs: Unified Large Language Models vs Local Fine-Tuned Models for Highly-Specific Radiology NLI Task.* IEEE Transactions on Big Data 11(3), 1027–1041, 2025. \*Equal contribution.

```bibtex
@article{wu2025tradeoffs,
  title         = {Exploring the Trade-Offs: Unified Large Language Models vs Local Fine-Tuned Models for Highly-Specific Radiology {NLI} Task},
  author        = {Wu, Zihao and Zhang, Lu and Cao, Chao and Yu, Xiaowei and Liu, Zhengliang and Zhao, Lin and Li, Yiwei and Dai, Haixing and Ma, Chong and Li, Gang and Liu, Wei and Li, Quanzheng and Shen, Dinggang and Li, Xiang and Zhu, Dajiang and Liu, Tianming},
  journal       = {IEEE Transactions on Big Data},
  volume        = {11},
  number        = {3},
  pages         = {1027--1041},
  year          = {2025},
  doi           = {10.1109/TBDATA.2025.3536928},
  eprint        = {2304.09138},
  archivePrefix = {arXiv}
}
```

RadQA: S. Soni, M. Gudala, A. Pajouhi, K. Roberts. *RadQA: A Question Answering Dataset to Improve Comprehension of Radiology Reports.* LREC 2022, 6250–6259; data on PhysioNet, [doi:10.13026/ckkp-6y19](https://doi.org/10.13026/ckkp-6y19).

<details>
<summary>2023 notes (original README)</summary>

The data and output files these tables were computed from are no longer in the repository.

Different codes for RadQNLI


# Results
## Random Sample

||radqa_test_rand_00 (Random: 460+1681)|radqa_test_rand_01 (Random: 460+1327)|radqa_test_rand_02(Random: 460+517)|radqa_test_rand_03(Random: 460+193)|
|--|--|--|--|--|
|1|ACC: 0.8305 P: 0.6240 R: 0.5304 F1: 0.5734|ACC: 0.8159 P: 0.6825 R: 0.5326 F1: 0.5983|ACC: 0.7318 P: 0.8390 R: 0.5326 F1: 0.6516|ACC: 0.6417 P: 0.9380 R: 0.5261 F1: 0.6741|
|2|ACC: 0.8277 P: 0.6140 R: 0.5326 F1: 0.5704|ACC: 0.8125 P: 0.6751 R: 0.5239 F1: 0.5900|ACC: 0.7288 P: 0.8397 R: 0.5239 F1: 0.6452|ACC: 0.6478 P: 0.9492 R: 0.5283 F1: 0.6788|
|3|ACC: 0.8295 P: 0.6234 R: 0.5217 F1: 0.5680|ACC: 0.8109 P: 0.6743 R: 0.5130 F1: 0.5827|ACC: 0.7349 P: 0.8478 R: 0.5326 F1: 0.6542|ACC: 0.6386 P: 0.9444 R: 0.5174 F1: 0.6685|
|4|ACC: 0.8328 P: 0.6288 R: 0.5413 F1: 0.5818|ACC: 0.8165 P: 0.6864 R: 0.5283 F1: 0.5971|ACC: 0.7329 P: 0.8443 R: 0.5304 F1: 0.6515|ACC: 0.6462 P: 0.9421 R: 0.5304 F1: 0.6787|
|5|ACC: 0.8281 P: 0.6173 R: 0.5261 F1: 0.5681|ACC: 0.8086 P: 0.6648 R: 0.5174 F1: 0.5819|ACC: 0.7410 P: 0.8581 R: 0.5391 F1: 0.6622|ACC: 0.6447 P: 0.9488 R: 0.5239 F1: 0.6751|
|**Average**|ACC: 0.8297±0.0019 P: 0.6215±0.0054 R: 0.5304±0.0064 F1: 0.5743±0.0056|ACC: 0.8121±0.0030 P: 0.6766±0.0077 R: 0.5234±0.0076 F1: 0.5941±0.0056|ACC: 0.7339±0.0051P: 0.8458±0.0073 R: 0.5313±0.0075 F1: 0.6461±0.0057|ACC: 0.6430±0.0035 P: 0.9445±0.0030 R: 0.5252±0.0050 F1: 0.6762±0.0028|

## R1

||radqa_test_00 (R1 > 0.0: 460+1681)|radqa_test_01 (R1 >= 0.1: 460+1327)|radqa_test_02(R1 >= 0.2: 460+517)|radqa_test_03(R1 >= 0.3: 460+193)|
|--|--|--|--|--|
|1|ACC: 0.8094 P: 0.5602 R: 0.5261 F1: 0.5426|ACC: 0.7885 P: 0.6051 R: 0.5130 F1: 0.5553|ACC: 0.7001 P: 0.7634 R: 0.5261 F1: 0.6229|ACC: 0.6233 P: 0.8905 R: 0.5304 F1: 0.6649|
|2|ACC: 0.8090 P: 0.5581 R: 0.5326 F1: 0.5451|ACC: 0.7929 P: 0.6119 R: 0.5348 F1: 0.5708|ACC: 0.6909 P: 0.7500 R: 0.5152 F1: 0.6108|ACC: 0.6156 P: 0.8885 R: 0.5196 F1: 0.6557|
|3|ACC: 0.8094 P: 0.5586 R: 0.5391 F1: 0.5487|ACC: 0.7957 P: 0.6203 R: 0.5326 F1: 0.5731|ACC: 0.7083 P: 0.7676 R: 0.5457 F1: 0.6379|ACC: 0.6110 P: 0.8843 R: 0.5152 F1: 0.6511|
|4|ACC: 0.8122 P: 0.5674 R: 0.5304 F1: 0.5483|ACC: 0.7963 P: 0.6212 R: 0.5348 F1: 0.5748|ACC: 0.6950 P: 0.7531 R: 0.5239 F1: 0.6179|ACC: 0.6233 P: 0.8877 R: 0.5326 F1: 0.6658|
|5|ACC: 0.8104 P: 0.5631 R: 0.5239 F1: 0.5428|ACC: 0.7963 P: 0.6200 R: 0.5391 F1: 0.5767|ACC: 0.7032 P: 0.7623 R: 0.5370 F1: 0.6301|ACC: 0.6309 P: 0.8869 R: 0.5457 F1: 0.6756|
|**Average**|ACC: 0.8100±0.0023 P: 0.5611±0.0047 R: 0.5321±0.0068 F1: 0.5462±0.0094|ACC: 0.7934±0.0044 P: 0.6146±0.0097 R: 0.5288±0.0066 F1: 0.5685±0.0069|ACC: 0.6986±0.0066 P: 0.7585±0.0052 R: 0.5277±0.0102 F1: 0.6224±0.0066|ACC: 0.6186±0.0054 P: 0.8878±0.0029 R: 0.5244±0.0105 F1: 0.6594±0.0105|

---
## Random_sample2


||radqa_test_rand_00|radqa_test_rand_01|radqa_test_rand_02|radqa_test_rand_03|
|--|--|--|--|--|
|1|ACC: 0.8277 P: 0.6152 R: 0.5283 F1: 0.5684|ACC: 0.8081 P: 0.6639 R: 0.5152 F1: 0.5802|ACC: 0.7288 P: 0.8328 R: 0.5304 F1: 0.6481|ACC: 0.6401 P: 0.9377 R: 0.5239 F1: 0.6722|
|2|ACC: 0.8272 P: 0.6142 R: 0.5261 F1: 0.5667|ACC: 0.8103 P: 0.6676 R: 0.5239 F1: 0.5871|ACC: 0.7175 P: 0.8172 R: 0.5152 F1: 0.6320|ACC: 0.6417 P: 0.9380 R: 0.5261 F1: 0.6741|
|3|ACC: 0.8267 P: 0.6099 R: 0.5370 F1: 0.5711|ACC: 0.8170 P: 0.6802 R: 0.5457 F1: 0.6055|ACC: 0.7247 P: 0.8304 R: 0.5217 F1: 0.6409|ACC: 0.6432 P: 0.9416 R: 0.5261 F1: 0.6750|
|4|ACC: 0.8267 P: 0.6121 R: 0.5283 F1: 0.5671|ACC: 0.8109 P: 0.6694 R: 0.5239 F1: 0.5878|ACC: 0.7236 P: 0.8276 R: 0.5217 F1: 0.6400|ACC: 0.6279 P: 0.9289 R: 0.5109 F1: 0.6592|
|5|ACC: 0.8258 P: 0.6124 R: 0.5152 F1: 0.5596|ACC: 0.8075 P: 0.6611 R: 0.5174 F1: 0.5805|ACC: 0.7288 P: 0.8283 R: 0.5348 F1: 0.6499|ACC: 0.6417 P: 0.9380 R: 0.5261 F1: 0.6741|
|**Average**|ACC: 0.8268±0.0005 P: 0.6127±0.0012 R: 0.5270±0.0070 F1: 0.5666±0.0042|ACC: 0.8108±0.0020 P: 0.6684±0.0070 R: 0.5248±0.0113 F1: 0.5872±0.0060|ACC: 0.7247±0.0042 P: 0.8273±0.0069 R: 0.5248±0.0070 F1: 0.6402±0.0057|ACC: 0.6389±0.0046 P: 0.9365±0.0050 R: 0.5248±0.0070 F1: 0.6731±0.0036|

</details>
