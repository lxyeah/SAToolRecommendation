import os
import threading

import close_warning
import src.utils.write_to_xls as wtx
import src.configure as c
import data_process as dp


def get_labeled_res(proname, tag_list, tool_name, labeled_method, pro_path):
    for j in range(len(tag_list) - 1):
        res = []

        for k in range(j+1, len(tag_list)):
            before_revision = pro_path + '/' + tag_list[j] + '_{}.csv'.format(tool_name)
            after_revision = pro_path + '/' + tag_list[k] + '_{}.csv'.format(tool_name)
            before_revision_dir = repo_dir + proname + '/unzip_repos/' + tag_list[j]
            before_revision_path = before_revision_dir + '/' + os.listdir(before_revision_dir)[0]
            after_revision_dir = repo_dir + proname + '/unzip_repos/' + tag_list[k]
            after_revision_path = after_revision_dir + '/' + os.listdir(after_revision_dir)[0]

            res = labeled_method(before_revision, before_revision_path, after_revision,
                                    after_revision_path)

        if not os.path.exists(c.data_dir + '/' + proname):
            os.mkdir(c.data_dir + '/' + proname)

        print('PROCESS ' + tag_list[j] + ' ' + tool_name + ' DONE')
        wtx.write_csv(os.path.join(c.data_dir, proname, tag_list[j] + '_{}_labeled.csv'.format(tool_name)), res)


def close_warning_thread(repos, reports_dir):
    for i in repos:

        if not os.path.exists(c.projects + '/' + i):
            continue
        # if os.path.exists(c.data_dir + '/' + i):
        #     continue
        print('--------------------PROCESS ' + i + '--------------------')
        pro_path = reports_dir + '/' + i
        findbugs = []
        pmd = []
        sonarqube = []

        if not os.path.exists(pro_path):
            continue

        for j in os.listdir(pro_path):
            # if j.endswith('findbugs.csv'):
            #     findbugs.append(j.split('_findbugs.csv')[0])
            # if j.endswith('pmd.csv'):
            #     pmd.append(j.split('_pmd.csv')[0])
            if j.endswith('sonarqube.csv'):
                sonarqube.append(j.split('_sonarqube.csv')[0])

        # get_labeled_res(i, findbugs, 'findbugs', close_warning.findbugs_close_warning_label, pro_path)
        # get_labeled_res(i, pmd, 'pmd', close_warning.pmd_close_warning_label, pro_path)
        get_labeled_res(i, sonarqube, 'sonarqube', close_warning.sonarqube_close_warning_label, pro_path)
        print('--------------------PROCESS ' + i + ' DONE--------------------')


if __name__ == '__main__':
    # project_dir = r'C:\Users\lxyeah\Desktop\SAToolRecommendation\Bug-Assessment-Tool\temp'
    reports_dir = c.report_path
    repo_dir = c.projects
    data_dir = c.data_dir
    tool_evaluation_path = c.tool_evaluation_path

    # repo_list = os.listdir(c.report_path)
    # repo_length = len(repo_list)
    #
    # threads = []
    # thread_num = 8
    #
    # step = int(repo_length / thread_num)
    # print(repo_list[:step])

    # for i in range(thread_num - 1):
    #     t = threading.Thread(target=close_warning_thread, args=(repo_list[step * i: step * (i+1)], reports_dir))
    #     threads.append(t)
    # t_end = threading.Thread(target=close_warning_thread, args=(repo_list[step * (thread_num - 1):], reports_dir))
    # threads.append(t_end)

    # repos = repo_list[step * 5: step * 6]
    # index = 0
    # for i in range(len(repos)):
    #     if repos[i] == 'mule-common':
    #         index = i + 1
    #         break
    # repos = repos[index:]
    #
    # t = threading.Thread(target=close_warning_thread, args=(repos, reports_dir))
    # threads.append(t)
    #
    # for t in threads:
    #     # t.setDaemon(True)
    #     t.start()
    #
    # for t in threads:
    #     t.join()
    # print('主线程运行结束')

    for i in os.listdir(data_dir):
        print('--------------------PROCESS ' + i + '--------------------')
        data_path = c.data_dir + '/' + i

        tag_list = []
        for j in os.listdir(data_path):
            tag = j.split(i + '-')[1][0:1]
            if tag not in tag_list:
                tag_list.append(tag)

        for j in tag_list:
            if os.path.exists(data_path + '/' + i + '-' + j + '_findbugs_labeled.csv') and os.path.exists(data_path + '/' + i + '-' + j + '_pmd_labeled.csv') and os.path.exists(data_path + '/' + i + '-' + j + '_sonarqube_labeled.csv'):
                print('-------------------- ' + i + ' ' + j + ' ---------------------')
                res = dp.data_process(data_path + '/' + i + '-' + j + '_findbugs_labeled.csv',
                                      data_path + '/' + i + '-' + j + '_pmd_labeled.csv',
                                      data_path + '/' + i + '-' + j + '_sonarqube_labeled.csv')
                wtx.write_csv(tool_evaluation_path + '/' + i + '-' + j + '_tool_evaluation.csv', res)
        print('--------------------PROCESS ' + i + ' DONE--------------------')




