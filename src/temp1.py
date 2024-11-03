import os
import csv

res_path = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/'

repo_dir = os.listdir(res_path)
for repo in repo_dir:
    repo_path = res_path + '/' + repo + '/'
    file_list = os.listdir(repo_path)
    for file in file_list:
        if file.endswith('pmd.csv'):
            res = []
            lines = []
            file_path = repo_path + file
            with open(file_path, 'r', errors='ignore') as f:
                reader = csv.reader(f)
                for i in reader:
                    lines.append(i)
            f.close()

            if len(lines) == 0:
                continue

            first_line = lines[0]
            if first_line[0] == 'Problem':
                lines = lines[1:]

            for line in lines:
                line_path = line[2]
                if 'target\\' in line_path:
                    continue
                if 'trash\\' in line_path:
                    print(repo + ' ' + file)
                    continue
                if 'src\\test\\' in line_path:
                    print(repo + '--' + file)
                    continue
                token_main_list = line_path.split('main')
                if len(token_main_list) != 1:
                    res.append(line)
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(res)
            f.close()
        if file.endswith('sonarqube.csv'):
            res = []
            lines = []
            file_path = repo_path + file
            with open(file_path, 'r', errors='ignore') as f:
                reader = csv.reader(f)
                for i in reader:
                    lines.append(i)
            f.close()

            for line in lines:
                line_path = line[1]
                if 'trash/' in line_path:
                    print(repo + ' ' + file)
                    continue
                if 'src/test/' in line_path:
                    print(repo + '--' + file)
                    continue
                token_main_list = line_path.split('main')
                if len(token_main_list) != 1:
                    res.append(line)
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(res)
            f.close()
        if file.endswith('findbugs.csv'):
            res = []
            lines = []
            file_path = repo_path + file
            with open(file_path, 'r', errors='ignore') as f:
                reader = csv.reader(f)
                for i in reader:
                    lines.append(i)
            f.close()

            for line in lines:
                line_path = line[3]
                if '.test.' in line_path:
                    print(repo + '--' + file)
                    continue
                res.append(line)
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(res)
            f.close()