import os
import src.configure as c
import sys
import xml.dom.minidom as dom
import src.utils.write_to_xls as wtx
import src.utils.getcodes as gc


def init_folder():
    res_path = c.res_path + c.pro_name + c.checkstyle_res_path
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    if not os.path.exists(res_path + c.xml_res):
        os.mkdir(res_path + c.xml_res)
    if not os.path.exists(res_path + c.csv_res):
        os.mkdir(res_path + c.csv_res)


# 使用checkstyle分析项目获取xml文件
def get_checkstyle_init_data():
    repo_path = c.repo_path + c.pro_name + '/'
    res_path = c.res_path + c.pro_name + c.checkstyle_xml_res_path
    cmd = 'java -jar ' + c.jar_path + ' -c ' + c.sun_checks_path + ' ' + repo_path + ' -f xml -o ' + res_path + '/'\
          + c.pro_name + '.xml'
    print(cmd)
    os.system(cmd)


def isTargetorTest(s):
    return '/target/' in s or '/target/' in s or 'Test' in s or 'test' in s


# 根据xml获取csv文件
def from_checkstyle_xml_to_csv():
    pro_path = c.res_path + c.pro_name
    xml_path = pro_path + c.checkstyle_xml_res_path
    xml_files = os.listdir(xml_path)
    csv_path = pro_path + c.checkstyle_csv_res_path
    headers = ['file', 'line', 'severity', 'message', 'source']
    for filename in xml_files:
        old = []
        res = []
        try:
            tree = dom.parse(xml_path + filename)
        except Exception:
            continue
        root = tree.documentElement
        print('now get csv from checkstyle file : '+filename)
        files = root.getElementsByTagName("file")
        for f in files:
            error_file_name = f.getAttribute('name').replace('/','/')
            if isTargetorTest(error_file_name):
                continue
            # print(filename[-4:] + " "+ filename[-9:-5])
            if error_file_name[-4:] != 'java' or error_file_name[-9:-5] == 'Test':
                continue
            errors = f.getElementsByTagName('error')
            for e in errors:
                line = e.getAttribute('line')
                severity = e.getAttribute('severity')
                message = e.getAttribute('message')
                source = e.getAttribute('source')
                if old != [error_file_name, line]:
                    old = [error_file_name, line]
                else:
                    continue
                res.append([error_file_name, line, severity, message, source])
        wtx.save_as_csv(headers, res, csv_path + filename.split('.xml')[0]+'.csv')


# 根据csv获取对应的代码
def get_code_from_csv():
    cs_path = c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/'
    csv_path = cs_path+'/csv_res/'
    xml_files = os.listdir(csv_path)
    for i in xml_files:
        print('now get checkstyle res code from xml is :' + i)
        data = wtx.get_from_csv(csv_path+i)
        headers = data[0]+['code'] if len(data[0]) == 5 else data[0]
        data = data[1:]
        for line in data:
            sys.stdout.write("\r" + ";   now position is :"+str(data.index(line))+'/'+str(len(data)))
            sys.stdout.flush()
            if len(line) == 6:
                continue
            try:
                code = gc.get_one_line(line[headers.index('file')],int(line[headers.index('line')]))
            except Exception:
                code = ''
            data[data.index(line)] = line+[code]
        wtx.save_as_csv(headers,data,csv_path+i)


# diff标记，用后一个版本标记前一个版本
def use_self_remark_checkstyle_res(rewrite = False):
    csv_res = c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/csv_res/'
    file_type = os.listdir(csv_res)[0].split('.')[-1]
    release_path = c.res_path+'/init_data/git_release_version_with_commitid.xls'
    release_data = wtx.get_from_xls(release_path)
    for i in range(3,len(release_data)-1):
        if (not rewrite) and os.path.exists(c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/diff_res/'+release_data[i][0]+'.'+file_type):
            print(c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/diff_res/'+release_data[i][0]+'.'+file_type+ " is already exist !!! ")
            continue
        print("loc is "+str(i)+"/"+str(len(release_data))+"  checkstyle: now diff use version is : "+release_data[i][0]+'.'+file_type)
        try:
            old_data = wtx.get_from_file(csv_res+release_data[i][0]+'.'+file_type,file_type)
            new_data = wtx.get_from_file(csv_res+release_data[i+1][0]+'.'+file_type,file_type,1)
        except FileNotFoundError as e:
            print("checkstyle res not found")
            continue
        if old_data[0][-1] != 'diff_status':
            headers = old_data[0] + ['diff_status']
        else:
            headers = old_data[0]
        file_index = headers.index('file')
        code_index = headers.index('code')
        for n in range(len(new_data)):
            sys.stdout.write("\r" + "now analyse checkstyle diff position is :"+str(n)+'/'+str(len(new_data)))
            sys.stdout.flush()
            for j in range(len(old_data)):
                if new_data[n][file_index].split('src')[-1] == old_data[j][file_index].split('src')[-1] \
                        and new_data[n][code_index].strip() == old_data[j][code_index].strip():
                    if len(new_data[n])+1 != len(headers):
                        new_data[n] = new_data[n]+['', 'true']
                    else:
                        new_data[n] = new_data[n]+['true']
                    break
        wtx.save_as_csv(headers, new_data, c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/diff_res/' + release_data[i][0]+'.'+file_type)


# 主流程函数
def get_checkstyle_data_main_func():
    init_folder()
    get_checkstyle_init_data()
    from_checkstyle_xml_to_csv()
    # get_code_from_csv()
    # mcr.mark_cs_res_by_git()
    # use_self_remark_checkstyle_res()


if __name__ == "__main__":
    get_checkstyle_data_main_func()