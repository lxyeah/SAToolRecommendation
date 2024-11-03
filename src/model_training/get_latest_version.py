import pandas as pd
import os
import glob

column_names = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'label']

# 读取CSV文件
file_path = 'total_labeled_data.csv'
df = pd.read_csv(file_path)

# 提取项目名称和版本号
df[['Project', 'Version']] = df['Pro'].str.extract(r'^(.*?)-([A-Za-z]+)$')

# 将版本号转换为字母在字母表中的位置，以便进行比较
df['Version'] = df['Version'].apply(lambda x: ord(x.lower()) - ord('a') + 1)

# 对每个项目进行分组，并找出每个项目的最大版本号
max_version_df = df.loc[df.groupby('Project')['Version'].idxmax()]


# 创建字典来存储每种工具的结果
data_frames = {'findbugs': [], 'pmd': [], 'sonarqube': []}

# 创建存储每个工具结果的DataFrame列表
tool_data = {
    'findbugs': [],
    'pmd': [],
    'sonarqube': []
}

# 基础文件路径
base_path = "E:\\SAToolRecommendation\\Bug-Assessment-Tool\\data\\"

evaluation_path = "E:\\SAToolRecommendation\\Bug-Assessment-Tool\\tool_evaluation_result\\"

# 遍历每个项目，找到对应的CSV文件，并读取内容
for index, row in max_version_df.iterrows():
    project = row['Project']
    pro = row['Pro']
    folder_path = os.path.join(base_path, project, f'{pro}_*_labeled.csv')
    # 构建文件路径
    file_path = os.path.join(evaluation_path, f"{pro}_tool_evaluation.csv")

    # 检查文件是否存在
    if os.path.exists(file_path):
        # 读取CSV文件
        eval_df = pd.read_csv(file_path)

        # 为每个工具提取相应的行，并添加到列表中
        for tool in tool_data.keys():
            tool_row = eval_df[eval_df['tool'].str.match(f'^{tool}$')].copy()  # 使用正则表达式精确匹配
            if not tool_row.empty:
                tool_row['Project'] = project
                tool_data[tool].append(tool_row)
    else:
        print(f"File not found: {file_path}")



    # 查找该项目对应的所有静态分析工具结果文件
    for file in glob.glob(folder_path):
        # 检查文件是否为空
        if os.stat(file).st_size == 0:
            print(f"Skipping empty file: {file}")
            continue

        try:
            df = pd.read_csv(file, header=None, names=column_names, )
        except UnicodeDecodeError:
            try:
                # 尝试使用ISO-8859-1编码读取
                df = pd.read_csv(file, header=None, names=column_names, encoding='ISO-8859-1')
            except UnicodeDecodeError:
                # 尝试使用Windows特定的cp1252编码
                df = pd.read_csv(file, header=None, names=column_names, encoding='cp1252')

        # 检查DataFrame是否为空
        if df.empty:
            print(f"Loaded empty DataFrame from file: {file}")
            continue

        df = df.drop(['col9', 'col10'], axis=1)

        # 排除标签为'unknown'的行
        df = df[df['label'] != 'unknown']

        # 添加 'Pro' 列
        df['Pro'] = pro

        if 'findbugs' in file:
            data_frames['findbugs'].append(df)
        elif 'pmd' in file:
            data_frames['pmd'].append(df)
        elif 'sonarqube' in file:
            data_frames['sonarqube'].append(df)

# 对每个工具的数据进行合并，并存储为CSV文件
for tool, data_list in tool_data.items():
    if data_list:
        combined_df = pd.concat(data_list, ignore_index=True)
        combined_df.to_csv(os.path.join(base_path, f"{tool}_evaluation_results.csv"), index=False)
    else:
        print(f"No data found for {tool}")

# 对每个工具的结果进行合并，并存储为CSV文件
for tool, dfs in data_frames.items():
    if dfs:  # 确保列表不为空
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.to_csv(f'{tool}_results.csv', index=False)
