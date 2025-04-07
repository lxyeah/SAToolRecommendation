import os.path
import src.configure as c
import src.utils.compare_file as cf
import src.utils.web_operator as wo
import wget
import logging


# 创建仓库
def mkdir_repos(pro_name):
    pro_save_path = c.data_info + "projects/"
    cf.my_mkdir(pro_save_path)
    pro_save_path = pro_save_path + pro_name + "/"
    cf.my_mkdir(pro_save_path)
    zip_mkdir = pro_save_path + "zip_repos/"
    cf.my_mkdir(zip_mkdir)
    unzip_mkdir = pro_save_path + "unzip_repos/"
    cf.my_mkdir(unzip_mkdir)
    return zip_mkdir


# 从github下载zip文件
def download_zip_from_github(pro_name, tag_list, zip_path, repo_tag_url):
    # ascii A
    start_ascii_label = c.start_label
    web_flag = True
    for i in range(len(tag_list)):
        if os.path.exists(zip_path + pro_name + '-' + chr(start_ascii_label + i) + '.zip'):
            print("existed : " + tag_list[i] + '.zip')
            continue
        # https://github.com/apache/archiva/archive/refs/tags/archiva-2.2.5.zip
        url = repo_tag_url + str(tag_list[i]) + '.zip'
        # url = 'https://codeload.github.com/apache/'+c.pro_name+'/archive/refs/tags/'+i[0]
        print(pro_name + '-' + str(tag_list[i]) + " waiting for download url : " + url)
        res_flag = get_zip_from_url(url, zip_path + pro_name + '-' + chr(start_ascii_label + i) + '.zip')
        # sleep(5)
        print(url)
        web_flag = web_flag and res_flag
    return web_flag


def get_zip_from_url(url, down_path):
    try:
        wget.download(url, down_path)
    except Exception as e:
        logging.error(repr(e))
        return False
    finally:
        return True


# 将zip文件解压到unzip_repos中
def unzip_files(zip_path):
    unzip_path = zip_path.split('zip_repos')[0] + "unzip_repos/"

    if os.path.exists(unzip_path):
        del_cmd = 'RD /S /Q ' + unzip_path.replace('/', '\\')
        os.system(del_cmd)
    try:
        os.mkdir(unzip_path)
    except FileExistsError:
        with open('errors_project.txt', 'a') as f:
            f.write(unzip_path + '\n')
        f.close()

    flag = unzip_all_zip_indict(zip_path, unzip_path, 'zip')
    return flag


def unzip_all_zip_indict(path, res_path, file_type):
    files = os.listdir(path)
    flag = True
    for i in files:
        this_res_name = res_path+'/'+i.split('.zip')[0]
        if i.find('zip') < 0:
            continue
        if not os.path.exists(this_res_name):
            os.mkdir(this_res_name)
        cmdline = '7z x -o' + this_res_name + ' ' + path + i
        print("unzip file : "+path+i)
        print(cmdline)
        exit_code = os.system(cmdline)
        if exit_code == 0:
            logging.info('UNZIP: ' + i + ' DONE')
            # flag = flag and True
        else:
            logging.warning('UNZIP: ' + i + 'FAILED')
            del_cmd = 'RD /S /Q ' + this_res_name.replace('/', '\\')
            os.system(del_cmd)
            # flag = flag and False
    return flag
        # zip_ref = zipfile.ZipFile(path+i)
        # zip_ref.extractall(res_path+i.split('.'+file_type)[0])
        # zip_ref.close()


# 从github下载到解压
def download_and_unzip_from_github_main(pro_name, tag_list, repo_tag_url):
    # 建立目录
    zip_path = mkdir_repos(pro_name)
    # 下载zip包
    web_flag = download_zip_from_github(pro_name, tag_list, zip_path, repo_tag_url)

    if not web_flag:
        return False

    # 解压zip包
    return unzip_files(zip_path)
    return True


def get_tags_project_main_func(pro_name, tag_list, repo_tag_url):
    # 下载解压zip包
    return download_and_unzip_from_github_main(pro_name, tag_list, repo_tag_url)


if __name__ == "__main__":
    # tag_list = ['0.28', '0.37', '0.40', '0.33', '0.50']
    # # get_tags_project_main_func('aesh', tag_list)
    # pro_save_path = c.data_info + "projects/"
    # zip_path = pro_save_path + "aesh/zip_repos/"
    # unzip_files(zip_path)
    exit_code = os.system('7z x -oD:/data_info/projects/acceptance-test-harness/unzip_repos//acceptance-test-harness-E D:/data_info/projects/acceptance-test-harness/zip_repos/acceptance-test-harness-E.zip')
    print(exit_code)

