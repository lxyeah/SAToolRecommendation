import os
import shutil
import random

res_path = 'E:/SAToolRecommendation/reports/'

total = 0
total_number = 0
count = 0
l = []
dic = {}
res = []
for i in os.listdir(res_path):
    report_path = res_path + '/' + i
    os.chdir(report_path)

    p_count = 0
    dic[i] = 0
    for j in os.listdir(report_path):
        token = j.split('_')[0]
        if token not in l:
            l.append(token)
            dic[i] += 1
            p_count += 1
    if p_count > 5:
        res.append(i + ' ' + str(p_count))

    count += p_count

print(count)

random_elements = random.sample(res, 10)

print(random_elements)