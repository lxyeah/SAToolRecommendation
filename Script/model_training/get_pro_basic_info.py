import pandas as pd
from pathlib import Path
from git import Repo

# 读取CSV文件并提取项目名称
file_path = 'total_labeled_data.csv'
df = pd.read_csv(file_path)
df['Project'] = df['Pro'].str.extract(r'(^.*?)-')[0]
project_list = df['Project'].unique()  # 获取去重后的项目列表

# 指定包含Git项目的目录路径
projects_directory = Path('E:/data_repo/')

# 准备收集数据的字典
project_stats = []

# 遍历每个项目目录
for project_dir in projects_directory.iterdir():
    if project_dir.is_dir() and (project_dir / '.git').exists() and project_dir.name in project_list:
        # 读取项目的 tags CSV 文件
        tags_file_path = f'E:\\data_info\\init_data\\{project_dir.name}_tags.csv'
        if not Path(tags_file_path).exists():
            print(f"Tags file for project {project_dir.name} does not exist. Skipping...")
            continue

        # 检查文件是否为空
        if Path(tags_file_path).stat().st_size == 0:
            print(f"Tags file for project {project_dir.name} is empty. Skipping...")
            continue

        try:
            tags_df = pd.read_csv(tags_file_path)
        except pd.errors.EmptyDataError:
            print(f"Tags file for project {project_dir.name} has no columns to parse. Skipping...")
            continue

        if tags_df.empty:
            print(f"Tags file for project {project_dir.name} is empty after reading. Skipping...")
            continue

        repo = Repo(project_dir)

        # 获取项目的初始提交时间和最新提交时间
        commits = list(repo.iter_commits())
        start_time = commits[-1].committed_datetime
        end_time = commits[0].committed_datetime

        # 获取初始和最新代码行数（只统计Java文件）
        def count_java_lines(commit):
            count = 0
            for item in commit.tree.traverse():
                if item.type == 'blob' and item.name.endswith('.java'):
                    count += item.data_stream.read().count(b'\n')
            return count

        initial_lines = count_java_lines(commits[-1])
        current_lines = count_java_lines(commits[0])

        # 获取提交次数
        commit_count = len(commits)

        # 获取开发者人数
        developer_count = len(set(commit.author for commit in commits))

        # 获取项目的GitHub URL
        github_url = repo.remotes.origin.url if 'origin' in repo.remotes else 'N/A'

        # 提取最旧和最新的提交记录
        oldest_tag = tags_df.iloc[-1]
        newest_tag = tags_df.iloc[0]
        oldest_tag_version = oldest_tag['release version']
        newest_tag_version = newest_tag['release version']
        oldest_tag_commit_id = oldest_tag['commit id']
        newest_tag_commit_id = newest_tag['commit id']
        oldest_tag_commit_time = oldest_tag['commit time']
        newest_tag_commit_time = newest_tag['commit time']

        print('{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(
            project_dir.name, start_time, end_time, initial_lines, current_lines, commit_count, developer_count, github_url,
            oldest_tag_version, newest_tag_version, oldest_tag_commit_id, newest_tag_commit_id, oldest_tag_commit_time, newest_tag_commit_time
        ))

        # 将信息存储到字典中
        project_stats.append({
            'project': project_dir.name,
            'start_time': start_time,
            'end_time': end_time,
            'initial_lines': initial_lines,
            'current_lines': current_lines,
            'commit_count': commit_count,
            'developer_count': developer_count,
            'github_url': github_url,
            'oldest_tag_version': oldest_tag_version,
            'newest_tag_version': newest_tag_version,
            'oldest_tag_commit_id': oldest_tag_commit_id,
            'newest_tag_commit_id': newest_tag_commit_id,
            'oldest_tag_commit_time': oldest_tag_commit_time,
            'newest_tag_commit_time': newest_tag_commit_time,
        })

# 将收集到的数据转换为DataFrame
df_stats = pd.DataFrame(project_stats)

# 定义CSV文件名
output_csv_path = 'project_statistics.csv'

# 将DataFrame写入CSV文件，包括列标题
df_stats.to_csv(output_csv_path, index=False)

print(f"项目统计信息已保存到 '{output_csv_path}'。")