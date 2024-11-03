import src.get_revision.download_release_version_from_github as drvfg
import src.collect_datas.from_git_get_releaseversion as fggr
import os
import src.configure as c
import src.utils.write_to_xls as wtx
import src.utils.time_operator as to
import logging


def init_folder():
    if not os.path.exists(c.data_info):
        os.mkdir(c.data_info)
        os.mkdir(c.init_data)


def choose_tag_list(pro_name):
    tag_info_list_path = c.init_data + '{}_tags.csv'.format(pro_name)
    tag_info_list = wtx.get_from_csv(tag_info_list_path)[1:]
    length = len(tag_info_list)
    if length < 5:
        logging.warning('CHOOSE_TAG_LIST: ' + pro_name + ' tags less ' + str(c.tag_num) + ', is ' + str(length))
        print(pro_name + ' tags less ' + str(c.tag_num) + ', is ' + str(length))
        return []

    tag_list = []
    for i in range(length):
        tag_info = tag_info_list[length - i - 1]
        time = tag_info[-1]
        if to.compare_time(c.start_revision, time):
            temp_revision = tag_info
            tag_list.append(tag_info[0])
            j = i
            while j < length:
                tag_info = tag_info_list[length - j - 1]
                time = tag_info[-1]
                if to.time_minus(time, temp_revision[-1]) > c.revision_interval:
                    temp_revision = tag_info
                    tag_list.append(tag_info[0])
                if len(tag_list) == c.tag_num:
                    break
                j += 1
            break
    if len(tag_list) < 5:
        logging.warning('CHOOSE_TAG_LIST: ' + pro_name + ' tags less ' + str(c.tag_num) + ', is ' + str(len(tag_list)))
        print(pro_name + ' tags less ' + str(c.tag_num) + ', is ' + str(len(tag_list)))
        return []
    logging.info('CHOOSE_TAG_LIST: ' + pro_name + ' DONE')
    return tag_list


def get_all_atg_list(pro_name):
    tag_info_list_path = c.init_data + '{}_tags.csv'.format(pro_name)
    tag_info_list = wtx.get_from_csv(tag_info_list_path)[1:]
    return tag_info_list


def get_revision_main(pro_name, repo_tag_url):
    # 获取release版本信息
    fggr.get_all_tag_with_commitid(pro_name)
    tag_list = choose_tag_list(pro_name)

    if len(tag_list) < 2:
        return False
    else:
        # 下载zip包并解压编译获取classes
        return drvfg.get_tags_project_main_func(pro_name, tag_list, repo_tag_url)

    # return drvfg.get_tags_project_main_func(pro_name, tag_list, repo_tag_url)


if __name__ == "__main__":
    # init_folder()
    # get_revision_main()
    tag_list = choose_tag_list('aesh')
    print(tag_list)

