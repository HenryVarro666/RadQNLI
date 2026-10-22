# Research problem

> **Does a question-inference model retain its ability to distinguish answer-supporting radiology text when negative examples are made harder without changing evaluation prevalence?**

**Why it matters:** A model can appear stronger because its test set contains easier negatives or a different class balance. Reliable comparison requires separating reasoning difficulty from sampling effects.

**Central tension:** Lexically similar negatives may test useful distinctions, but changing their selection can also alter topic, prevalence and annotation ambiguity.

**Current evidence and gap:** [README.md](README.md) contains historical random-sampling and R1 result tables. Their different sample compositions cannot by themselves isolate the effect of negative difficulty. The repository supports an NLP research comparison, not a clinical performance claim.

**Decisive verification:** Freeze document-level train/development/test partitions before generating pairs. Compare random and similarity-based negative selection with matched class counts, model initialization, training budget and decision threshold selection. Evaluate both on the same untouched test set, reporting precision-recall behavior, class-specific errors and results across seeds. Blindly check ambiguous negatives. If differences disappear under a common test distribution, attribute the historical contrast to sampling rather than stronger inference.

This module proposes a controlled follow-up; existing result tables are unchanged.

中文版：[PROBLEM.zh.md](PROBLEM.zh.md)
