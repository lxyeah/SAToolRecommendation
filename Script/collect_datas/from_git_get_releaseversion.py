import os
import src.utils.write_to_xls as wtx
import src.utils.cmd_tool as ct
import src.configure as c
import src.utils.time_operator as to
import logging


def get_all_tag_name(path, filter=0):
    os.chdir(path)
    cmd = 'git tag --sort=taggerdate'
    run_res = os.popen(cmd).readlines()
    tags = []
    for i in run_res:
        if  filter == 1 and (i.find('alpha') > 0 or i.find('beta') > 0 or i.find(c.pro_name+'-') < 0 or len(i.split('.')) == 1) :
            continue
        print(i)
        tags.append(i.replace('\n',''))
    print('all tags is :')
    print(tags)
    return tags


def get_all_tag_with_commitid(pro_name):
    if os.path.exists(c.init_data + pro_name + '_tags.csv'):
        logging.info('GET_ALL_TAG: {} EXIST.'.format(pro_name))
        return

    path = c.data_repo + pro_name
    res = []
    times = []
    headers = ['release version', 'commit id', 'commit time']
    tags = get_all_tag_name(path)
    for i in tags:
        cmd = 'cd '+path + " && git show "+i
        print(cmd)
        run_res = ct.run_command(cmd)
        comid = ''
        date = ''
        for line in run_res:
            if line[:7] == 'commit ':
                comid = line.split('commit ')[1].replace('\n', '').strip()
            if line[:6] == 'Date: ':
                date = line.split('Date: ')[1].replace('\n', '').strip()
            if comid != '' and date != '':
                res.append([i, comid, date])
                times.append(date)
                break
    # print(len(res))
    res = sort_by_time(res, -1, times)
    # print(len(res))
    res.reverse()
    print(res)
    wtx.save_as_csv(headers, res, c.init_data + pro_name + '_tags.csv')
    logging.info('GET_ALL_TAG: {} DONE.'.format(pro_name))
    return tags


def sort_by_time(list, index, date):
    # print(date)
    date_list = to.get_sort_res(date)
    res = []
    tag = [0 for i in range(len(list))]
    for i in date_list:
        for j in list:
            if j[index] == i and tag[list.index(j)] != 1:
                res.append(j)
                tag[list.index(j)] = 1
                break
    return res


if __name__ == "__main__":
    get_all_tag_with_commitid('aesh')