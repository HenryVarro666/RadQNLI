import pandas as pd

# 读取输出文本
# df = pd.read_csv("./radqa_test_generated2.tsv", sep="\t")
# df = pd.read_csv("./radqa_test_input.tsv", sep="\t")
df = pd.read_csv("./radqa_test_output.tsv", sep="\t")

# print(df["label"])
total_count = len(df)

# 计算 Yes 和 No 的数量
yes_count = (df["answer"] == "Yes.").sum()
no_count = (df["answer"] == "No.").sum()

# yes_count = (df["label"] == "Yes.").sum()
# no_count = (df["label"] == "No.").sum()

# 计算 Yes 和 No 的比例
total_count = len(df)
yes_ratio = yes_count / total_count
no_ratio = no_count / total_count

# 输出结果
print("Total count:", total_count)
print("Yes count:", yes_count)
print("No count:", no_count)
print("Yes ratio:", yes_ratio)
print("No ratio:", no_ratio)




