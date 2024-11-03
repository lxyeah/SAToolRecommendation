import os
import csv

root_path = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/'
findbugs_path = 'Achilles-C_findbugs.csv'
pmd_path = 'Achilles-C_pmd.csv'
sonarqube_path = 'Achilles-C_sonarqube.csv'

findbugs_lines = []
with open(root_path + findbugs_path, 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        findbugs_lines.append(i)
f.close()

pmd_lines = []
with open(root_path + pmd_path, 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        if i[6] == 'Documentation' or i[6] == 'Code Style':
            continue
        i[2] = i[2].split('D:/data_info/projects/Achilles/unzip_repos/Achilles-C/Achilles-achilles-2.0.2/')[1]
        pmd_lines.append(i)
f.close()

sonarqube_lines = []
with open(root_path + sonarqube_path, 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        i[1] = i[1].split('Achilles-C:')[1]
        sonarqube_lines.append(i)
f.close()

res_1 = []
for pmd_line in pmd_lines:
    pmd_path = pmd_line[2].replace('\\', '/')
    pmd_start = pmd_line[4]

    for sonarqube_line in sonarqube_lines:
        sonarqube_path = sonarqube_line[1]
        sonarqube_start = sonarqube_line[2]

        if pmd_path == sonarqube_path and pmd_start == sonarqube_start:
            res_1.append(pmd_line + sonarqube_line)

with open('pmd_join_sonarqube.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(res_1)
f.close()

res_2 = []
for findbugs_line in findbugs_lines:
    findbugs_path = findbugs_line[3].split('.')[-1]
    findbugs_start = findbugs_line[6]

    for pmd_line in pmd_lines:
        pmd_path = pmd_line[2].split('/')[-1].split('.java')[0]
        pmd_start = pmd_line[4]

        if pmd_path == findbugs_path and pmd_start == findbugs_start:
            res_2.append(findbugs_line + pmd_line)

with open('findbugs_join_pmd.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(res_2)
f.close()

res_3 = []
for findbugs_line in findbugs_lines:
    findbugs_path = findbugs_line[3].split('.')[-1]
    findbugs_start = findbugs_line[6]

    for sonarqube_line in sonarqube_lines:
        sonarqube_path = sonarqube_line[1].split('/')[-1].split('.java')[0]
        sonarqube_start = sonarqube_line[2]

        if findbugs_path == sonarqube_path and findbugs_start == sonarqube_start:
            res_3.append(findbugs_line + sonarqube_line)

with open('findbugs_sonarqube.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(res_3)
f.close()

res_4 = []
for findbugs_line in res_2:
    findbugs_path = findbugs_line[3].split('.')[-1]
    findbugs_start = findbugs_line[6]
    pmd_path = findbugs_line[10].split('/')[-1].split('.java')[0]
    pmd_start = findbugs_line[12]

    for sonarqube_line in sonarqube_lines:
        sonarqube_path = sonarqube_line[1].split('/')[-1].split('.java')[0]
        sonarqube_start = sonarqube_line[2]

        if findbugs_path == sonarqube_path and sonarqube_path == pmd_path and findbugs_start == sonarqube_start and sonarqube_start == pmd_start:
            res_4.append(findbugs_line + sonarqube_line)

with open('findbugs_join_pmd_join_sonarqube.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(res_4)
f.close()


