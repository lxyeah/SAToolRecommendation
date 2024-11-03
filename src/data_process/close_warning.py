import os
import csv
import re


def get_code_similarity(before_code_line, after_code_line):
    pat = '[a-zA-Z]+'
    before_code_tokens = re.findall(pat, before_code_line)
    after_code_tokens = re.findall(pat, after_code_line)

    union_set = list(set(before_code_tokens) | set(after_code_tokens))
    intersection_set = list(set(before_code_tokens) & set(after_code_tokens))

    if len(union_set) == 0:
        return -1

    code_similarity = len(intersection_set) / len(union_set)
    return code_similarity


def write_csv(file_path, res):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(res)
    f.close()


def read_csv(file_path):
    res = []
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            res.append(i)
    f.close()
    return res


def read_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            res = f.readlines()
        f.close()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='gbk') as f:
                res = f.readlines()
            f.close()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='iso-8859-1') as f:
                res = f.readlines()
            f.close()
        except Exception as e:
            return None
    return res


def find_file_in_folder(target_file, root_path, res, package):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file == target_file:
                text_lines = read_text(os.path.abspath(os.path.join(root, file)))
                if text_lines is None:
                    return False
                package_line = ''
                for i in text_lines:
                    if i.strip().startswith('package'):
                        package_line = i
                        break
                if package_line == '':
                    return False
                if package_line.split(' ')[1].split(';')[0] in package:
                    res.append(os.path.abspath(os.path.join(root, file)))
                    return True
    return False


def findbugs_find_target_file(target_file, root_path, res, package):

    if not os.path.isdir(root_path):
        return False
    else:
        flag = False
        try:
            file_list = os.listdir(root_path)
        except Exception as e:
            return False

        for file in file_list:
            if not os.path.isdir(root_path + '/' + file):
                if target_file == file:
                    # print(root_path + '/' + file)
                    text_lines = read_text(root_path + '/' + file)
                    if text_lines is None:
                        return False
                    package_line = ''
                    for i in text_lines:
                        if i.strip().startswith('package'):
                            package_line = i
                            break
                    if package_line == '':
                        return False
                    if package_line.split(' ')[1].split(';')[0] in package:
                        res.append(root_path + '/' + file)
                        return True
                    else:
                        flag = flag or False
                else:
                    flag = flag or False
            else:
                flag = flag or findbugs_find_target_file(target_file, root_path + '/' + file, res, package)
        return flag


def pmd_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path):
    before_lines = read_csv(before_revision)
    after_lines = read_csv(after_revision)

    res_labels = []
    for before_line in before_lines:
        before_path = before_line[2].replace('\\', '/')
        temp_before_path = before_line[2].replace('\\', '/').split(before_revision_path)[1]
        before_rank = before_line[3]
        before_start = before_line[4]
        before_description = before_line[5]
        before_category = before_line[6]
        before_vtype = before_line[7]

        no_line_flag = False
        if int(before_start) != -1:
            before_text_lines = read_text(before_path)
            if int(before_start) >= len(before_text_lines):
                continue
            before_code_line = before_text_lines[int(before_start) - 1].strip()
        else:
            no_line_flag = True

        target_file = after_revision_path + temp_before_path
        res = False
        if os.path.exists(target_file):
            res = True

        if res:

            flag = False
            code_info_list = []
            for after_line in after_lines:
                after_path = after_line[2].replace('\\', '/')
                temp_after_path = after_line[2].replace('\\', '/').split(after_revision_path)[1]
                after_rank = after_line[3]
                after_start = after_line[4]
                after_description = after_line[5]
                after_category = after_line[6]
                after_vtype = after_line[7]

                if target_file.replace('\\', '/') == after_path.replace('\\', '/'):
                    code_similarity = 0
                    if not no_line_flag:
                        after_text_lines = read_text(after_path)
                        after_code_line = after_text_lines[int(after_start) - 1].strip()

                        code_similarity = get_code_similarity(before_code_line, after_code_line)
                        code_similarity_flag = code_similarity == -1 or code_similarity > 0.5

                    if temp_before_path == temp_after_path and before_category == after_category and before_vtype == after_vtype and before_rank == after_rank:
                        if no_line_flag:
                            if before_start == after_start and before_description == after_description:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append('')
                                code_info_list.append('')
                                code_info_list.append('1')
                                flag = True
                                break
                        else:
                            if before_description == after_description:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append(before_code_line)
                                code_info_list.append(after_code_line)
                                code_info_list.append('1')
                                flag = True
                                break
                            if code_similarity_flag:
                                if len(code_info_list) == 0:
                                    code_info_list += before_line
                                    code_info_list.append(before_code_line)
                                    code_info_list.append(after_code_line)
                                    code_info_list.append(code_similarity)
                                else:
                                    if float(code_similarity) > float(code_info_list[-1]):
                                        code_info_list = []
                                        code_info_list += before_line
                                        code_info_list.append(before_code_line)
                                        code_info_list.append(after_code_line)
                                        code_info_list.append(code_similarity)
                                    # res_labels.append(before_line)
                                flag = True

            if flag:
                code_info_list = code_info_list[:-1]
                code_info_list.append('open')
                res_labels.append(code_info_list)
            if not flag:
                if not no_line_flag:
                    before_line.append(before_code_line)
                else:
                    before_line.append('')
                before_line.append(before_code_line)
                before_line.append('')
                before_line.append('close')
                res_labels.append(before_line)


        else:
            before_line.append('')
            before_line.append('')
            before_line.append('unknown')
            res_labels.append(before_line)

    return res_labels


def findbugs_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path):
    before_lines = read_csv(before_revision)
    after_lines = read_csv(after_revision)

    res_labels = []
    for before_line in before_lines:
        before_priority = before_line[0]
        before_category = before_line[1]
        before_vtype = before_line[2]
        before_path = before_line[3]
        before_field = before_line[4]
        before_method = before_line[5]
        before_start = before_line[6]
        before_end = before_line[7]

        if len(before_line) == 11:
            close_flag = before_line[10]
            if close_flag == 'close':
                res_labels.append(before_line)
                continue

        target_file = before_path.split('.')[-1].split('$')[0] + '.java'
        before_res_list = []
        before_res = find_file_in_folder(target_file, before_revision_path, before_res_list, before_path)
        if len(before_res_list) == 0:
            continue

        before_res_path = before_res_list[0]

        no_line_flag = False
        if int(before_start) != -1:
            before_text_lines = read_text(before_res_path)
            if int(before_start) >= len(before_text_lines):
                continue
            before_code_line = before_text_lines[int(before_start) - 1].strip()
        else:
            no_line_flag = True

        after_res_list = []
        after_res = find_file_in_folder(target_file, after_revision_path, after_res_list, before_path)

        if after_res:

            flag = False
            code_info_list = []
            for after_line in after_lines:
                after_priority = after_line[0]
                after_category = after_line[1]
                after_vtype = after_line[2]
                after_path = after_line[3]
                after_field = after_line[4]
                after_method = after_line[5]
                after_start = after_line[6]
                after_end = after_line[7]



                if after_path == before_path:
                    after_res_path = after_res_list[0]
                    after_text_lines = read_text(after_res_path)
                    if int(after_start) >= len(after_text_lines):
                        continue

                    code_similarity = 0
                    if not no_line_flag:
                        after_code_line = after_text_lines[int(after_start) - 1].strip()

                        code_similarity = get_code_similarity(before_code_line, after_code_line)
                        code_similarity_flag = code_similarity == -1 or code_similarity > 0.5

                    if before_priority == after_priority and before_category == after_category and before_vtype == after_vtype and before_path == after_path and before_field == after_field:
                        if no_line_flag:
                            if before_start == after_start and before_method == after_method:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append('')
                                code_info_list.append('')
                                code_info_list.append('1')
                                flag = True
                                break
                        else:
                            if before_start == after_start and before_method == after_method:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append(before_code_line)
                                code_info_list.append(after_code_line)
                                code_info_list.append('1')
                                flag = True
                                break
                            if code_similarity_flag:
                                if len(code_info_list) == 0:
                                    code_info_list += before_line
                                    code_info_list.append(before_code_line)
                                    code_info_list.append(after_code_line)
                                    code_info_list.append(code_similarity)
                                else:
                                    if float(code_similarity) > float(code_info_list[-1]):
                                        code_info_list = []
                                        code_info_list += before_line
                                        code_info_list.append(before_code_line)
                                        code_info_list.append(after_code_line)
                                        code_info_list.append(code_similarity)
                                    # res_labels.append(before_line)
                                flag = True

            if flag:
                code_info_list = code_info_list[:-1]
                code_info_list.append('open')
                res_labels.append(code_info_list)
            if not flag:
                if no_line_flag:
                    before_line.append('')
                else:
                    before_line.append(before_code_line)
                before_line.append('')
                before_line.append('close')
                res_labels.append(before_line)

        else:
            before_line.append('')
            before_line.append('')
            before_line.append('unknown')
            res_labels.append(before_line)

    return res_labels


def sonarqube_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path):
    before_lines = read_csv(before_revision)
    after_lines = read_csv(after_revision)

    res_labels = []
    for before_line in before_lines:
        before_path = before_revision_path + '/' + before_line[1].replace('\\', '/').split(':')[1]
        before_start = before_line[2]
        before_category = before_line[4]
        before_severity = before_line[5]
        before_tag = before_line[6]
        before_description = before_line[7]

        no_line_flag = False

        if int(before_start) != -1:
            before_text_lines = read_text(before_path)
            if int(before_start) >= len(before_text_lines):
                continue
            before_code_line = before_text_lines[int(before_start) - 1].strip()
        else:
            no_line_flag = True

        target_file = after_revision_path + '/' + before_line[1].replace('\\', '/').split(':')[1]
        res = False
        if os.path.exists(target_file):
            res = True

        if res:

            flag = False
            code_info_list = []
            for after_line in after_lines:
                after_path = after_revision_path + '/' + after_line[1].replace('\\', '/').split(':')[1]
                after_start = after_line[2]
                after_category = after_line[4]
                after_severity = after_line[5]
                after_tag = after_line[6]
                after_description = after_line[7]

                if after_path == target_file:
                    code_similarity = 0
                    if not no_line_flag:
                        after_text_lines = read_text(after_path)
                        after_code_line = after_text_lines[int(after_start) - 1].strip()

                        code_similarity = get_code_similarity(before_code_line, after_code_line)
                        code_similarity_flag = code_similarity == -1 or code_similarity > 0.5

                    if before_line[1].split(':')[1] == after_line[1].split(':')[1] and before_category == after_category and before_severity == after_severity and before_tag == after_tag:
                        if no_line_flag:
                            if before_start == after_start and before_description == after_description:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append('')
                                code_info_list.append('')
                                code_info_list.append('1')
                                flag = True
                                break
                        else:
                            if before_start == after_start and before_description == after_description:
                                code_info_list = []
                                code_info_list += before_line
                                code_info_list.append(before_code_line)
                                code_info_list.append(after_code_line)
                                code_info_list.append('1')
                                flag = True
                                break
                            if code_similarity_flag:
                                if len(code_info_list) == 0:
                                    code_info_list += before_line
                                    code_info_list.append(before_code_line)
                                    code_info_list.append(after_code_line)
                                    code_info_list.append(code_similarity)
                                else:
                                    if float(code_similarity) > float(code_info_list[-1]):
                                        code_info_list = []
                                        code_info_list += before_line
                                        code_info_list.append(before_code_line)
                                        code_info_list.append(after_code_line)
                                        code_info_list.append(code_similarity)
                                    # res_labels.append(before_line)
                                flag = True

            if flag:
                code_info_list = code_info_list[:-1]
                code_info_list.append('open')
                res_labels.append(code_info_list)
            if not flag:
                if not no_line_flag:
                    before_line.append(before_code_line)
                else:
                    before_line.append('')
                before_line.append('')
                before_line.append('close')
                res_labels.append(before_line)

        else:
            before_line.append('')
            before_line.append('')
            before_line.append('unknown')
            res_labels.append(before_line)
    return res_labels


if __name__ == '__main__':
    before_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-D_findbugs.csv'
    after_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-E_findbugs.csv'
    before_revision_path = 'E:/data_info/projects/Achilles/unzip_repos/Achilles-D/Achilles-achilles-2.0.9/'
    after_revision_path = 'E:/data_info/projects/Achilles/unzip_repos/Achilles-E/Achilles-achilles-2.0.10-dse/'
    res = findbugs_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path)
    write_csv('findbugs_labeled.csv', res)

    before_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-D_pmd.csv'
    after_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-E_pmd.csv'
    res = pmd_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path)
    write_csv('pmd_labeled.csv', res)

    before_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-D_sonarqube.csv'
    after_revision = 'C:/Users/lxyeah/Desktop/SAToolRecommendation/reports/Achilles/Achilles-E_sonarqube.csv'
    res = sonarqube_close_warning_label(before_revision, before_revision_path, after_revision, after_revision_path)
    write_csv('sonarqube_labeled.csv', res)