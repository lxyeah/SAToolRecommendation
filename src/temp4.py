import os
from itertools import groupby


def read_and_sort_files(folder_path):
    # 获取所有文件
    files = os.listdir(folder_path)

    # 分解文件名并排序
    sorted_files = sorted(files, key=lambda x: (x.split('-')[0], x.split('-')[1].split('_')[0]))

    # 按项目名分组
    grouped_files = groupby(sorted_files, key=lambda x: x.split('-')[0])

    # 从每组中选出第一个文件
    first_files = [next(group) for _, group in grouped_files]

    os.chdir(proj_evaluation_path)
    for file in first_files:
        cmd1 = 'XCOPY {} {}'.format(os.path.join(res_path, file), proj_evaluation_path)
        cmd2 = 'REN {} {}'.format(file, file.split('-')[0] + '.csv')
        os.system(cmd1)
        os.system(cmd2)

    return first_files

# 示例使用
res_path = 'E:\\SAToolRecommendation\\Bug-Assessment-Tool\\tool_evaluation_result'
proj_evaluation_path = 'E:\\SAToolRecommendation\\Bug-Assessment-Tool\\evaluation'
if not os.path.exists(proj_evaluation_path):
    os.mkdir(proj_evaluation_path)
selected_files = read_and_sort_files(res_path)
print(selected_files)
print(len(selected_files))
