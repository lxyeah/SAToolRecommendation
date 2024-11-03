import os
import src.utils.write_to_xls as wtx
import src.utils.getcodes as gc
import src.configure as c
import sys
import threading

# cmd = [pmd.bat path] output_path -f xml -R [rule path] -r filepath

pmd_path = c.pmd_path


# 制作结果文件
def init_folder():
    res_path = c.res_path + c.pro_name + c.pmd_res_path
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    if not os.path.exists(res_path + c.xml_res):
        os.mkdir(res_path + c.xml_res)
    if not os.path.exists(res_path + c.csv_res):
        os.mkdir(res_path + c.csv_res)


# 使用pmd语句分析项目
def pmd_analysis_project(repo_path, res_path):
    output_format = 'csv'
    # repo_path = c.repo_path + c.pro_name + '/'
    # res_path = c.res_path + c.pro_name + c.pmd_csv_res_path + c.pro_name + '.' + output_format
    cmd = "pmd.bat check" ' -f ' + output_format + ' -d ' + repo_path + ' -R ' + c.pmd_rule_xml_path + ' -r ' + res_path
    print(cmd)
    os.system(cmd)


def get_pmd_res_main_func(repo_path, res_path):
    # init_folder()
    pmd_analysis_project(repo_path, res_path)


def pmd_analysis_thread(repo_list):
    for repo in repo_list:
        if repo in repo_dic.keys():
            tags = repo_dic[repo]
            for tag in tags:
                tag_path = repo_path + repo + '/unzip_repos/' + tag + '/'
                real_repo = os.listdir(tag_path)[0]
                final_repo_path = tag_path + real_repo + '/'
                final_res_path = reports_path + repo + '/' + tag + '_pmd.csv'
                get_pmd_res_main_func(final_repo_path, final_res_path.replace('\\', '/'))

                os.chdir(final_repo_path)
                os.system('mvn sonar:sonar -Dsonar.projectKey={} -Dsonar.projectName={} -Dsonar.scm.disabled=true -Dsonar.language=java -Dsonar.login=6503a88998cf677847ef85dfd7d6e35653f22f82'.format(tag, tag))


if __name__ == "__main__":
    reports_path = "C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/"
    repo_path = c.projects

    repo_dic = {}
    with open('C:/Users/lxyeah/Desktop/SAToolRecommendation/Bug-Assessment-Tool/src/available.list', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            token_list = line.split(':')
            pro_name = token_list[0]
            tag_list = token_list[1].split(',')
            repo_dic[pro_name] = tag_list
    f.close()

    repo_list = os.listdir(repo_path)
    repo_length = len(repo_list)
    step = int(repo_length / 4)

    print(repo_list[:step])

    threads = []
    t1 = threading.Thread(target=pmd_analysis_thread, args=(repo_list[:step], ))
    t2 = threading.Thread(target=pmd_analysis_thread, args=(repo_list[step:step*2], ))
    t3 = threading.Thread(target=pmd_analysis_thread, args=(repo_list[step*2:step*3], ))
    t4 = threading.Thread(target=pmd_analysis_thread, args=(repo_list[step*3:], ))
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)

    for t in threads:
        # t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
    print('主线程运行结束')