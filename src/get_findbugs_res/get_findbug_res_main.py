import xml.dom.minidom as dom
import src.utils.write_to_xls as wtx
import src.utils.file_operator as fo
import src.configure as c
import os
import logging

# 初始化文件夹
def init_folder(pro_name):
    res_path = c.res_path + pro_name + c.findbugs_res_path
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    if not os.path.exists(res_path + c.xml_res):
        os.mkdir(res_path + c.xml_res)
    if not os.path.exists(res_path + c.csv_res):
        os.mkdir(res_path + c.csv_res)
    if not os.path.exists(res_path + c.classes_repo):
        os.mkdir(res_path + c.classes_repo)

# 使用mvn对项目进行编译
def mvn_compile(pro_name, tag):
    repo_path = c.projects + '/' + pro_name + c.unzip_repo + '/' + pro_name + '-' + tag

    if not os.path.exists(repo_path):
        return False

    tag_pro_name = os.listdir(repo_path)[0]
    mvn_path = repo_path + '/' + tag_pro_name
    os.chdir(mvn_path)
    exit_code = os.system('mvn -T 12 clean install -U -DskipTests=true -Dmaven.javadoc.skip=true -Dmaven.site.skip=true -Drat.skip=true -Dgpg.skip -Dmaven.repo.local=E:\maven_temp_repo')
    if exit_code == 0:
        classes_path = mvn_path + '/target/classes/'
        if not os.path.exists(classes_path):
            logging.warning('MVN_COMPILE: {} FAILED (NO CLASSES)'.format(pro_name + '-' + tag))
            return True
        else:
            logging.info('MVN_COMPILE: {} DONE'.format(pro_name + '-' + tag))
            return True
    else:
        logging.warning('MVN_COMPILE: {} FAILED (BUILD FAILED)'.format(pro_name + '-' + tag))
        return False


def get_findbugs_xml(pro_name, tag):
    res_path = c.res_path + pro_name + c.findbugs_res_path
    xml_path = res_path + c.xml_res
    classes_repo_path = res_path + c.classes_repo

    if os.path.exists(xml_path + pro_name + '-' + tag + '.xml'):
        logging.warning('GET_FINDBUGS_XML: {} EXIST'.format(pro_name + '-' + tag))
        return True

    # findbugs.bat -textui -progress -high -xml -output
    # E:/projects/py/shiwanhuoji/Fx_is_pig//projs/archiva/findbugs_res/xml/archiva-2.2.5.xml
    # E:/projects/py/shiwanhuoji/Fx_is_pig//projs/archiva/classes_repos/archiva-archiva-2.2.5
    cmdline = 'findbugs.bat -textui -low -progress -xml -output ' \
              + xml_path + pro_name + '-' + tag + '.xml ' \
              + classes_repo_path
    print("now run command is : " + cmdline)
    exit_code = os.system(cmdline)
    if exit_code == 0:
        logging.info('GET_FINDBUGS_XML: {} DONE'.format(pro_name + '-' + tag))
    else:
        logging.warning('GET_FINDBUGS_XML: {} FAILED'.format(pro_name + '-' + tag))

    del_cmd = 'RD /S /Q ' + classes_repo_path.replace('/', '\\')
    os.system(del_cmd)
    os.mkdir(classes_repo_path)

    return True


# 根据xml获取csv文件
def get_csv(pro_name, tag):
    csv_path = c.res_path + pro_name + c.findbugs_csv_res_path
    xml_path = c.res_path + pro_name + c.findbugs_xml_res_path
    print(csv_path)
    if not os.path.exists(csv_path):
        os.mkdir(csv_path)

    heads = ["method_name", "method_sig", "file_path", "class_name", "lstart", "lend", "priority", "catogeray", "codes"]
    res = []
    filename = pro_name + '-' + tag + '.xml'
    tree = dom.parse(xml_path + filename)
    root = tree.documentElement
    print("filename _ " + filename)

    bugs = root.getElementsByTagName("BugInstance")

    for bug in bugs:
        desc = bug.getAttribute("type")
        priority = bug.getAttribute("priority")
        if bug.getElementsByTagName("Method"):
            croot = bug.getElementsByTagName("Method")[0]
            classname = croot.getAttribute("classname")
            signature = croot.getAttribute("signature")
            method_name = croot.getAttribute("name")
            root2 = croot.getElementsByTagName("SourceLine")[0]
            sourcepath = root2.getAttribute("sourcepath")
            if 'test' in sourcepath or 'Test' in sourcepath:
                continue
            start = root2.getAttribute("start")
            end = root2.getAttribute("end")
            res.append([method_name, signature, sourcepath, classname, start, end, priority, desc])
    wtx.save_as_csv(heads, res, csv_path + '/' + pro_name + '-' + tag + '.csv')


def get_findbugs_res_main(pro_name):
    # 初始化文件夹
    init_folder(pro_name)

    count = 0
    for i in range(c.tag_num):
        tag = chr(c.start_label + i)

        # 进行编译
        compile_flag = mvn_compile(pro_name, tag)
        if compile_flag:
            count += 1

        if not compile_flag:
            continue

        # # 拷贝编译的类文件
        copy_flag = fo.copy_classes_to_target_path(pro_name, tag)
        #
        if not copy_flag:
            continue
        #
        # 扫描classes获取xml文件
        get_findbugs_xml(pro_name, tag)
        # 转为csv
        get_csv(pro_name, tag)

    if count >= 2:
        with open('E:/SAToolRecommendation/Bug-Assessment-Tool/src/compile_success.list', 'a') as f:
            f.write(pro_name + '\n')
        f.close()


if __name__ == "__main__":
    pro_name = 'aesh'
    pro_path = c.res_path + '/' + pro_name + '/'
    if not os.path.exists(pro_path):
        os.mkdir(pro_path)
    get_findbugs_res_main(pro_name)
