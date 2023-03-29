import pandas as pd

# 读取.tsv文件
df = pd.read_csv('../radqa_test_raw.tsv', sep='\t')

# print(df)

# 将label列中的not_entailment替换为no，entailment替换为yes
df['label'] = df['label'].replace({'not_entailment': 'No.', 'entailment': 'Yes.'})

# 保存修改后的.tsv文件
df.to_csv('./radqa_test2.tsv', sep='\t', index=False)
