"""Build RadQNLI and the difficulty-controlled test sets from the output of radqa2qnli.py.

Ported from the 2023 Colab notebook that wrote the CSV files used in the paper. That notebook
also held restricted data, so it is no longer in the repository; the steps below keep its
behaviour: the same header-fragment filter, ROUGE-1 F1 between question and sentence
(rouge_score with the Porter stemmer, as the Hugging Face `rouge` metric computed it), the same
thresholds and the same random_state=42 sampling.

    python3 build_radqnli.py --tsv-dir . --out-dir ../data

Input: radqa_{train,dev,test}.tsv written by radqa2qnli.py. On RadQA 1.0.0 this gives
7,911 / 950 / 977 RadQNLI pairs (9,838 in all) and test sets of 460 entailment pairs with
1,681 / 1,327 / 517 / 193 negatives: the same pairs as the 2023 files (Random_sample1 also in
the same row order; R1 and Random_sample2 in another order, because ties in the ROUGE-1 sort
fall differently).

Output (all of it contains report text and is git-ignored):

    radqa_{split}.csv                         cleaned question / sentence / label pairs
    radqa_{split}_rouge02.csv                 RadQNLI: every entailment pair plus the
                                              not_entailment pairs with ROUGE-1 >= 0.2
    R1/radqa_test_0{0,1,2,3}.csv              test set, negatives with ROUGE-1 > 0, >= 0.1,
                                              >= 0.2, >= 0.3 (more word overlap)
    Random_sample1/radqa_test_rand_0k.csv     same number of negatives, drawn at random
    Random_sample2/radqa_test_rand_0k.csv     same number of negatives per question, drawn at
                                              random from that question's negatives
"""
import argparse
import os

import pandas as pd
from rouge_score import rouge_scorer

SPLITS = ["train", "dev", "test"]
# report section headers and list numbers that sentence splitting leaves as "sentences"
HEADER_FRAGMENTS = ["Evaluation", "IMPRESSION", "IMPRESSION: 1.", "IMPRESSION:  1.",
                    "2.", "3.", "4.", "5.", "6."]
THRESHOLDS = [("00", lambda r: r > 0), ("01", lambda r: r >= 0.1),
              ("02", lambda r: r >= 0.2), ("03", lambda r: r >= 0.3)]
COLS = ["question", "sentence", "label"]
SEED = 42


def clean(tsv_file, csv_file):
    """radqa_{split}.tsv -> radqa_{split}.csv without header fragments."""
    data = pd.read_csv(tsv_file, sep="\t", on_bad_lines="skip")
    data = data.drop("index", axis=1)
    data = data[~data["sentence"].isin(HEADER_FRAGMENTS)]
    data.to_csv(csv_file, index=False)
    return pd.read_csv(csv_file)


def add_rouge1(df):
    """ROUGE-1 F1 between each question (prediction) and its sentence (reference)."""
    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)
    df = df.copy()
    df["R1"] = [scorer.score(str(s), str(q))["rouge1"].fmeasure
                for q, s in zip(df["question"], df["sentence"])]
    return df


def combine(pos, neg, path):
    out = pd.concat([pos, neg], axis=0, ignore_index=True).sample(frac=1, random_state=SEED)
    out[COLS].to_csv(path, index=False)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tsv-dir", default=".", help="folder with radqa_{train,dev,test}.tsv")
    ap.add_argument("--out-dir", default="../data", help="where the CSV files go")
    ap.add_argument("--splits", nargs="+", default=SPLITS, choices=SPLITS)
    args = ap.parse_args()
    for sub in ["", "R1", "Random_sample1", "Random_sample2"]:
        os.makedirs(os.path.join(args.out_dir, sub), exist_ok=True)

    for split in args.splits:
        data = clean(os.path.join(args.tsv_dir, f"radqa_{split}.tsv"),
                     os.path.join(args.out_dir, f"radqa_{split}.csv"))
        pos = data[data["label"] == "entailment"]
        neg = add_rouge1(data[data["label"] == "not_entailment"])
        out = combine(pos, neg[neg["R1"] >= 0.2],
                      os.path.join(args.out_dir, f"radqa_{split}_rouge02.csv"))
        print(f"{split}: {len(data)} pairs after cleaning; RadQNLI {len(out)} "
              f"({len(pos)} entailment + {len(out) - len(pos)} not_entailment with ROUGE-1 >= 0.2)")
        if split != "test":
            continue

        neg_sorted = neg.sort_values(by="R1", ascending=False)
        for k, keep in THRESHOLDS:
            # R1: negatives that share more words with the question are harder
            hard = neg_sorted[keep(neg_sorted["R1"])]
            r1_path = os.path.join(args.out_dir, "R1", f"radqa_test_{k}.csv")
            combine(pos, hard, r1_path)
            n = len(hard)

            # Random_sample1: the same number of negatives, ignoring ROUGE-1
            combine(pos, neg.sample(n, random_state=SEED),
                    os.path.join(args.out_dir, "Random_sample1", f"radqa_test_rand_{k}.csv"))

            # Random_sample2: per question, as many random negatives as the R1 set has
            r1 = pd.read_csv(r1_path)
            r1_pos = r1[r1["label"] == "entailment"]
            r1_neg = r1[r1["label"] == "not_entailment"]
            counts = r1_neg["question"].value_counts()
            rows = [neg[neg["question"] == q].sample(counts[q], random_state=SEED)
                    for q in r1_neg["question"].unique()]
            combine(r1_pos, pd.concat(rows),
                    os.path.join(args.out_dir, "Random_sample2", f"radqa_test_rand_{k}.csv"))
            print(f"  test_{k}: {len(pos)} entailment + {n} not_entailment")


if __name__ == "__main__":
    main()
