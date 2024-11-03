import os
import csv
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib_venn import venn3

tool = ['findbugs', 'pmd', 'sonarqube']

res = {
    'findbugs': {
        'TP': 0,
        'FP': 0,
        'same': {
            'pmd': {
                'TP': 0,
                'FP': 0
            },
            'sonarqube': {
                'TP': 0,
                'FP': 0
            },
            'pmd&sonarqube': {
                'TP': 0,
                'FP': 0
            },
        }
    },
    'pmd': {
        'TP': 0,
        'FP': 0,
        'same': {
            'findbugs': {
                'TP': 0,
                'FP': 0
            },
            'sonarqube': {
                'TP': 0,
                'FP': 0
            },
            'findbugs&sonarqube': {
                'TP': 0,
                'FP': 0
            }
        }
    },
    'sonarqube': {
        'TP': 0,
        'FP': 0,
        'same': {
            'findbugs': {
                'TP': 0,
                'FP': 0
            },
            'pmd': {
                'TP': 0,
                'FP': 0
            },
            'findbugs&pmd': {
                'TP': 0,
                'FP': 0
            }
        }
    }
}


def read_evaluations(eval_file):
    # 读取 CSV 文件
    df = pd.read_csv(eval_file)

    for index, row in df[:3].iterrows():
        tool = row[0]
        TP = row[1]
        FP = row[2]
        res[tool]['TP'] += TP
        res[tool]['FP'] += FP


def read_same(same_file):
    df = pd.read_csv(same_file, na_values='')

    for index, row in df.iterrows():
        tools_row = [row[:11], row[11:22], row[22:33]]

        if tools_row[0][-1] != '' and tools_row[1][-1] != '' and pd.isna(tools_row[2][-1]):
            if tools_row[0][-1] == 'open' and tools_row[1][-1] == 'open':
                res['findbugs']['same']['pmd']['FP'] += 1
                res['pmd']['same']['findbugs']['FP'] += 1
            if tools_row[0][-1] == 'close' and tools_row[1][-1] == 'close':
                res['findbugs']['same']['pmd']['TP'] += 1
                res['pmd']['same']['findbugs']['TP'] += 1
        if tools_row[0][-1] != '' and pd.isna(tools_row[1][-1]) and tools_row[2][-1] != '':
            if tools_row[0][-1] == 'open' and tools_row[2][-1] == 'open':
                res['findbugs']['same']['sonarqube']['FP'] += 1
                res['sonarqube']['same']['findbugs']['FP'] += 1
            if tools_row[0][-1] == 'close' and tools_row[2][-1] == 'close':
                res['findbugs']['same']['sonarqube']['TP'] += 1
                res['sonarqube']['same']['findbugs']['TP'] += 1
        if pd.isna(tools_row[0][-1]) and tools_row[1][-1] != '' and tools_row[2][-1] != '':
            if tools_row[1][-1] == 'open' and tools_row[2][-1] == 'open':
                res['pmd']['same']['sonarqube']['FP'] += 1
                res['sonarqube']['same']['pmd']['FP'] += 1
            if tools_row[1][-1] == 'close' and tools_row[2][-1] == 'close':
                res['pmd']['same']['sonarqube']['TP'] += 1
                res['sonarqube']['same']['pmd']['TP'] += 1
        if tools_row[0][-1] != '' and tools_row[1][-1] != '' and tools_row[2][-1] != '':
            if tools_row[0][-1] == 'open' and tools_row[1][-1] == 'open' and tools_row[2][-1] == 'open':
                res['findbugs']['same']['pmd&sonarqube']['FP'] += 1
                res['pmd']['same']['findbugs&sonarqube']['FP'] += 1
                res['sonarqube']['same']['findbugs&pmd']['FP'] += 1
            if tools_row[0][-1] == 'close' and tools_row[1][-1] == 'close' and tools_row[2][-1] == 'close':
                res['findbugs']['same']['pmd&sonarqube']['TP'] += 1
                res['pmd']['same']['findbugs&sonarqube']['TP'] += 1
                res['sonarqube']['same']['findbugs&pmd']['TP'] += 1


if __name__ == '__main__':
    eval_dir = 'E:\\SAToolRecommendation\\Bug-Assessment-Tool\\tool_evaluation_result\\'
    same_dir = 'E:\\SAToolRecommendation\\Bug-Assessment-Tool\\src\\data_process\\'

    df = pd.read_csv('E:\SAToolRecommendation\Bug-Assessment-Tool\src\model_training\\new_data.csv')
    pro_list = df.iloc[:, -3]
    for pro in pro_list:
        eval_file = eval_dir + pro + '_tool_evaluation.csv'
        read_evaluations(eval_file)

        pro = pro.split('-')[0]
        same_file = same_dir + pro + '_same_warnings.csv'
        if os.path.exists(same_file):
            read_same(same_file)

    with open('res.json', 'w') as json_file:
        json.dump(res, json_file, indent=4)
    print(res)

    # 定义每个区域的数量
    venn_data = {
        '100': res['findbugs']['TP']  -
               (res['findbugs']['same']['pmd']['TP'] ) -
               (res['findbugs']['same']['sonarqube']['TP'] ),  # 只有 Set 1
        '010': res['pmd']['TP']  -
               (res['pmd']['same']['findbugs']['TP'] ) -
               (res['pmd']['same']['sonarqube']['TP'] ),  # 只有 Set 2
        '001': res['sonarqube']['TP']  -
               (res['sonarqube']['same']['findbugs']['TP'] ) -
               (res['sonarqube']['same']['findbugs']['TP'] ),  # 只有 Set 3
        '110': res['findbugs']['same']['pmd']['TP'] ,  # Set 1 和 Set 2
        '101': res['findbugs']['same']['sonarqube']['TP'] ,  # Set 1 和 Set 3
        '011': res['pmd']['same']['sonarqube']['TP'] ,  # Set 2 和 Set 3
        '111': 0  # Set 1, Set 2 和 Set 3
    }
    venn_data1 = {
        '100':  res['findbugs']['FP'] -
               ( res['findbugs']['same']['pmd']['FP']) -
               (res['findbugs']['same']['sonarqube']['FP']),  # 只有 Set 1
        '010': res['pmd']['FP'] -
               (res['pmd']['same']['findbugs']['FP']) -
               (res['pmd']['same']['sonarqube']['FP']),  # 只有 Set 2
        '001':  res['sonarqube']['FP'] -
               (res['sonarqube']['same']['pmd']['FP']) -
               (res['sonarqube']['same']['pmd']['FP']),  # 只有 Set 3
        '110': res['findbugs']['same']['pmd']['FP'],  # Set 1 和 Set 2
        '101': res['findbugs']['same']['sonarqube']['FP'],  # Set 1 和 Set 3
        '011': res['pmd']['same']['sonarqube']['FP'],  # Set 2 和 Set 3
        '111': 0  # Set 1, Set 2 和 Set 3
    }

    # 绘制韦恩图
    venn = venn3(subsets=venn_data1, set_labels=('SpotBugs', 'PMD', 'SonarQube'))

    # 标注每个区域的数量
    for subset, label in venn_data1.items():
        label_obj = venn.get_label_by_id(subset)
        if label_obj is not None:
            label_obj.set_text(label)

    # 显示图形
    plt.show()

