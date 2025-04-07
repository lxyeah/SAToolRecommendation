import os
import src.configure as c
import shutil


def project_clean():
    data_info_path = c.data_info + '/projects'
    total = 0
    unzip_total = 0
    for i in os.listdir(data_info_path):
        zip_pro_path = data_info_path + '/' + i + '/zip_repos'
        unzip_pro_path = data_info_path + '/' + i + '/unzip_repos'
        if len(os.listdir(zip_pro_path)) == 0:
            shutil.rmtree(data_info_path + '/' + i)
        else:
            total += len(os.listdir(zip_pro_path))
            # print(len(os.listdir(zip_pro_path)), i)

        if os.path.exists(unzip_pro_path):
            if len(os.listdir(unzip_pro_path)) <= 1:
                shutil.rmtree(data_info_path + '/' + i)
            else:
                unzip_total += len(os.listdir(unzip_pro_path))
                print(len(os.listdir(unzip_pro_path)), i)

    print(unzip_total)



if __name__ == '__main__':
    project_clean()