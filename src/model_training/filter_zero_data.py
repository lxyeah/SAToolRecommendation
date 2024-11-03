import pandas as pd

# 读取CSV文件，假设没有header，并且数据分隔符为逗号
df = pd.read_csv('data_f10.csv', header=None)

# 检查最后一列中值为0的行，并移除这些行
df = df[df.iloc[:, -1] != 0.0]

# 保存到新的CSV文件，不包含索引，也没有header
df.to_csv('new_data_f10.csv', index=False, header=None)
