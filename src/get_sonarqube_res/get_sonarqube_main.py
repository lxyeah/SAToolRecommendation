import requests
import json
import csv
import src.utils.parse_pom as pp
import os
import src.configure as c


def get_csv(res_path, pro_name):
    # if os.path.exists(res_path + '/' + '{}_sonarqube.csv'.format(pro_name)):
    #     print(pro_name + ' is existed.')
    #     return

    url = "http://localhost:9000/api/issues/search?p={}&additionalFields=_all&componentKeys={}&types=BUG,CODE_SMELL,VULNERABILITY"

    response = requests.get(url.format(1, pro_name), auth=('admin', '112358'))
    json_text = json.loads(response.text)
    total = json_text['total']

    page_num = int(total / 100)
    if total % 100 != 0:
        page_num = page_num + 1

    res = []
    for i in range(page_num):
        response = requests.get(url.format(i + 1, pro_name), auth=('admin', '112358'))

        text = response.text

        json_text = json.loads(text)
        issues = json_text['issues']
        for j in range(len(issues)):
            project = issues[j]['project']
            severity = issues[j]['severity']
            path = issues[j]['component']
            start_line = -1
            end_line = -1
            if 'textRange' in issues[j].keys():
                start_line = issues[j]['textRange']['startLine']
                end_line = issues[j]['textRange']['endLine']
            message = issues[j]['message']
            tags = issues[j]['tags']
            type = issues[j]['type']
            res.append([project, path, start_line, end_line, type, severity, tags, message])

    print(pro_name + ' is done')
    with open(res_path + '/' + '{}_sonarqube.csv'.format(pro_name), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(res)
    f.close()


if __name__ == '__main__':
    reports_path = "C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/"
    repo_path = c.projects

    repo_dic = {}
    with open('C:/Users/lxyeah/Desktop/SAToolRecommendation/Bug-Assessment-Tool/src/available.list', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            token_list = line.split(':')
            pro_name = token_list[0]
            tag_list = token_list[1].split(',')
            repo_dic[pro_name] = tag_list
    f.close()


    repo_list = os.listdir(repo_path)

    # for repo in repo_list:
    #     if repo in repo_dic.keys():
    #         tags = repo_dic[repo]
    #         for tag in tags:
    #             tag_path = repo_path + repo + '/unzip_repos/' + tag + '/'
    #             real_repo = os.listdir(tag_path)[0]
    #             final_repo_path = tag_path + real_repo + '/'
    #             os.chdir(final_repo_path)
    #             os.system('mvn sonar:sonar -Dsonar.projectKey={} -Dsonar.projectName={} -Dsonar.scm.disabled=true -Dsonar.language=java -Dsonar.login=6503a88998cf677847ef85dfd7d6e35653f22f82'.format(tag, tag))

    reports_list = os.listdir(reports_path)
    for i in reports_list:
        res_path = reports_path + '/' + i
        repo_tags = repo_dic[i]
        for tag in repo_tags:
            get_csv(res_path, tag)