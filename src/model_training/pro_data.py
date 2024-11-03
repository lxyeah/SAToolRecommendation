import pandas as pd

# 读取CSV文件
file_path = 'total_labeled_data_f10.csv'
df = pd.read_csv(file_path)

# 临时提取项目名称和版本号进行处理，但不保留这些列
project_version = df['Pro'].str.extract(r'^(.*?)-([A-Za-z]+)$')
project_version[1] = project_version[1].apply(lambda x: ord(x.lower()) - ord('a') + 1)
df['Temp_Version'] = project_version[1]

# 对每个项目进行分组，并找出每个项目的最大版本号
max_version_idx = df.groupby(project_version[0])['Temp_Version'].idxmax()
max_version_df = df.loc[max_version_idx]

# 删除临时添加的版本号列
max_version_df = max_version_df.drop(columns=['Temp_Version'])

# 保存筛选出的记录到新的CSV文件中，不包括表头
max_version_df.to_csv('data_f10.csv', index=False, header=False)