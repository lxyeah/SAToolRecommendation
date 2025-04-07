import threading

import src.get_revision.get_revision_main as grm
import src.get_findbugs_res.get_findbug_res_main as gfrm
import os
import configure as c
import logging


def flush():
    finished_list = []
    with open('finished.list', 'r') as f:
        for j in f.readlines():
            finished_list.append(j.strip())
    f.close()

    with open('repo_tag.list', 'r') as f:
        repo_tag_list = f.readlines()
    f.close()

    res = []
    for repo_tag in repo_tag_list:
        repo_tag = repo_tag.strip()
        if repo_tag.split(',')[0] in finished_list:
            token_list = repo_tag.split(',')
            repo_tag = token_list[0] + ',' + token_list[1] + ',' + '1'
            res.append(repo_tag + '\n')
        else:
            res.append(repo_tag + '\n')

    with open('repo_tag.list', 'w') as f:
        f.writelines(res)
    f.close()

    del_cmd = 'del finished.list'
    os.system(del_cmd)
    with open('finished.list', 'w') as f:
        f.close()


def init():
    flush()

    repo_dic = {}

    with open('repo_tag.list', 'r') as f:
        for line in f.readlines():
            token_list = line.strip().split(',')
            pro_name = token_list[0]
            url = token_list[1]
            finished = token_list[2]
            repo_dic[pro_name] = [url, finished]
    f.close()
    return repo_dic


def write_back(pro_name):
    with open('C:/Users/lxyeah/Desktop/SAToolRecommendation/Bug-Assessment-Tool/src/finished.list', 'a') as f:
        f.write(pro_name + '\n')
    f.close()


def main_process(repos: list):
    logging.basicConfig(filename="run_time.log", filemode="a", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.INFO)
    logging.info('#################################### RUNNING START #########################################')

    # repo_dic = init()
    flag3 = False
    index = 0
    for i in repos:

        if not os.path.exists(c.data_info + '/projects/' + i):
            continue

        pro_name = i


        # if pro_name == 'uima-uimaj':
        #     flag3 = True
        #
        # if not flag3:
        #     continue


        token_list = repo_dic[pro_name]
        url = token_list[0]
        finished = token_list[1]

        # if int(finished) == 1:
        #     index += 1
        #     continue

        logging.info('-------------------------------- ' + i + ' START ------------------------------')

        repo_url = url

        flag1 = grm.get_revision_main(pro_name, repo_url)
        # if not flag1:
        #     index += 1
        #     write_back(pro_name)
        #     continue

        # pro_path = c.res_path + '/' + pro_name + '/'
        # if not os.path.exists(pro_path):
        #     os.mkdir(pro_path)
        gfrm.get_findbugs_res_main(pro_name)

        index += 1
        # write_back(pro_name)
        logging.info('-------------------------------- ' + i + ' END ------------------------------')


if __name__ == '__main__':
    repo_dic = init()

    repo_list = ['spring-boot', 'DependencyCheck', 'languagetool']
    repo_length = len(repo_list)
    threads = []
    thread_num = 3

    step = int(repo_length / thread_num)
    print(repo_list[:step])

    for i in range(thread_num - 1):
        # arg_list =
        t = threading.Thread(target=main_process, args=(repo_list[step * i: step * (i + 1)],))
        threads.append(t)
    t_end = threading.Thread(target=main_process, args=(repo_list[step * (thread_num - 1):],) )
    threads.append(t_end)

    for t in threads:
        # t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()
    print('主线程运行结束')