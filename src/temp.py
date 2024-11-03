import os
import shutil

res_path = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/'

if os.path.exists(res_path):
    res = {}
    repo_list = os.listdir(res_path)
    for i in repo_list:
        repo_path = res_path + '/' + i
        tag_list = os.listdir(repo_path)
        if len(tag_list) < 2:
            shutil.rmtree(repo_path)
        else:
            res[i] = []
            for tag in tag_list:
                pro_name = tag.split('.csv')[0]
                if pro_name.endswith('findbugs'):
                    res[i].append(pro_name.split('_findbugs')[0])

    with open('available.list', 'w') as f:
        for i in res.keys():
            tag_list = res[i]
            row = '' + i + ':'
            for j in range(len(tag_list) - 1):
                row = row + tag_list[j] + ','
            row = row + tag_list[len(tag_list) - 1]
            f.write(row + '\n')
    f.close()

