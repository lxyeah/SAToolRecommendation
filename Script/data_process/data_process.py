import src.utils.write_to_xls as wtx
import close_warning as cw
import  csv
import  os
from sklearn.metrics import fbeta_score

def filter_unknown(file_path):
    res = []
    lines = wtx.read_csv(file_path)
    for line in lines:
        if line[-1] == 'unknown':
            continue
        else:
            res.append(line)
    return res


def get_all_warnings(findbugs_path, pmd_path, sonarqube_path):
    findbugs_res = filter_unknown(findbugs_path)
    pmd_res = filter_unknown(pmd_path)
    sonarqube_res = filter_unknown(sonarqube_path)

    total_dic = {}
    for i in findbugs_res:
        path = i[3].split('.')[-1].split('$')[0]
        start = i[6]

        key = path + ':' + start
        if key not in total_dic.keys():
            total_dic[key] = {}
            total_dic[key]['findbugs'] = [i]
            total_dic[key]['pmd'] = []
            total_dic[key]['sonarqube'] = []
        else:
            total_dic[key]['findbugs'].append(i)

    for i in pmd_res:
        path = i[2].split('\\')[-1].split('.java')[0]
        start = i[4]

        key = path + ':' + start
        if key not in total_dic.keys():
            total_dic[key] = {}
            total_dic[key]['pmd'] = [i]
            total_dic[key]['findbugs'] = []
            total_dic[key]['sonarqube'] = []
        else:
            total_dic[key]['pmd'].append(i)

    for i in sonarqube_res:
        path = i[1].split('/')[-1].split('.java')[0]
        start = i[2]

        key = path + ':' + start
        if key not in total_dic.keys():
            total_dic[key] = {}
            total_dic[key]['sonarqube'] = [i]
            total_dic[key]['pmd'] = []
            total_dic[key]['findbugs'] = []
        else:
            total_dic[key]['sonarqube'].append(i)

    return total_dic


def get_precision(FP, TP):
    precision = 0
    if FP != 0 or TP != 0:
        precision = TP / (FP + TP)
    return precision


def get_recall(FN, TP):
    recall = 0
    if FN != 0 or TP != 0:
        recall = TP / (TP + FN)
    return recall


def get_accuracy(FN, FP, TN, TP):
    accuracy = 0
    if FN != 0 or TN != 0 or FP != 0 or TP != 0:
        accuracy = (TP + TN) / (TP + FP + TN + FN)
    return accuracy


def get_f1(precision, recall, beta=1.0):
    f1 = 0
    if precision != 0 or recall != 0:
        f1 = ((1 + beta ** 2) * precision * recall) / ((beta ** 2) * precision + recall)
    return f1



def update_confusion_matrices(tool_states, flags, matrices):
    open_flag, close_flag = flags
    for index, state in enumerate(tool_states):
        if open_flag:
            matrices[index][1] += 1
            matrices[index][2] += 0
        if close_flag:
            matrices[index][0] += 1
            matrices[index][3] += 0


# def process_warnings(total_res):
#     # num_tools = len(c.tools)
#     confusion_matrices = [[0, 0, 0, 0] for _ in range(num_tools)]
#     under_review_warnings = []
#
#     for key, tool_dic in total_res.items():
#         tool_warnings = {tool: len(tool_dic.get(tool, [])) > 0 for tool in c.tools}
#         labels = [warning[-1] for tool in tool_dic for warning in tool_dic.get(tool, [])]
#
#         flags = ('close' in labels, 'open' in labels)
#         under_review = flags[0] and flags[1]
#         tool_states = [tool_warnings[tool] for tool in c.tools]
#
#         if under_review:
#             under_review_warnings.append((key, {tool: tool_dic.get(tool, []) for tool in c.tools}))
#
#         update_confusion_matrices(tool_states, flags, confusion_matrices)
#
#     c.csv_writer('under_review.csv', under_review_warnings)


    # return confusion_matrices

    


def data_process(findbugs_path, pmd_path, sonarqube_path):
    total_res = get_all_warnings(findbugs_path, pmd_path, sonarqube_path)

    print('Total warning num: ' + str(len(total_res.keys())))
    total_num = 0
    under_review_count = 0
    TP = 0
    FP = 1
    TN = 2
    FN = 3
    findbugs_confuse_matrix = [0, 0, 0, 0]
    pmd_confuse_matrix = [0, 0, 0, 0]
    sonarqube_confuse_matrix = [0, 0, 0, 0]
    findbugs_pmd_confuse_matrix = [0, 0, 0, 0]
    findbugs_sonarqube_confuse_matrix = [0, 0, 0, 0]
    pmd_sonarqube_confuse_matrix = [0, 0, 0, 0]


    under_review_list = []
    for i in total_res.keys():
        tool_dic = total_res[i]

        findbugs_warning = tool_dic['findbugs']
        pmd_warning = tool_dic['pmd']
        sonarqube_warning = tool_dic['sonarqube']

        findbugs_num = len(findbugs_warning)
        pmd_num = len(pmd_warning)
        sonarqube_num = len(sonarqube_warning)

        label_list = []
        for j in findbugs_warning:
            label_list.append(j[-1])
        for j in pmd_warning:
            label_list.append(j[-1])
        for j in sonarqube_warning:
            label_list.append(j[-1])

        close_flag = False
        open_flag = False

        if 'close' in label_list:
            close_flag= True
        if 'open' in label_list:
            open_flag = True

        under_review_flag = close_flag and open_flag

        if under_review_flag:
            under_review_count += 1
            under_review_list.append(tool_dic)
        else:
            if findbugs_num != 0 and pmd_num == 0 and sonarqube_num == 0:
                if open_flag:
                    findbugs_confuse_matrix[FP] += 1
                    pmd_confuse_matrix[TN] += 1
                    sonarqube_confuse_matrix[TN] += 1

                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    findbugs_pmd_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[TN] += 1
                if close_flag:
                    findbugs_confuse_matrix[TP] += 1
                    pmd_confuse_matrix[FN] += 1
                    sonarqube_confuse_matrix[FN] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    pmd_sonarqube_confuse_matrix[FN] += 1
            elif findbugs_num == 0 and pmd_num != 0 and sonarqube_num == 0:
                if open_flag:
                    findbugs_confuse_matrix[TN] += 1
                    pmd_confuse_matrix[FP] += 1
                    sonarqube_confuse_matrix[TN] += 1

                    findbugs_pmd_confuse_matrix[FP] += 1
                    findbugs_sonarqube_confuse_matrix[TN] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                if close_flag:
                    findbugs_confuse_matrix[FN] += 1
                    pmd_confuse_matrix[TP] += 1
                    sonarqube_confuse_matrix[FN] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[FN] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1
            elif findbugs_num == 0 and pmd_num == 0 and sonarqube_num != 0:
                if open_flag:
                    findbugs_confuse_matrix[TN] += 1
                    pmd_confuse_matrix[TN] += 1
                    sonarqube_confuse_matrix[FP] += 1

                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                    findbugs_pmd_confuse_matrix[TN] += 1
                if close_flag:
                    findbugs_confuse_matrix[FN] += 1
                    pmd_confuse_matrix[FN] += 1
                    sonarqube_confuse_matrix[TP] += 1

                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    findbugs_pmd_confuse_matrix[FN] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1
            elif findbugs_num != 0 and pmd_num != 0 and sonarqube_num == 0:
                if open_flag:
                    findbugs_confuse_matrix[FP] += 1
                    pmd_confuse_matrix[FP] += 1
                    sonarqube_confuse_matrix[TN] += 1

                    findbugs_pmd_confuse_matrix[FP] += 1
                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                if close_flag:
                    findbugs_confuse_matrix[TP] += 1
                    pmd_confuse_matrix[TP] += 1
                    sonarqube_confuse_matrix[FN] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1
            elif findbugs_num != 0 and pmd_num == 0 and sonarqube_num != 0:
                if open_flag:
                    findbugs_confuse_matrix[FP] += 1
                    pmd_confuse_matrix[TN] += 1
                    sonarqube_confuse_matrix[FP] += 1

                    findbugs_pmd_confuse_matrix[FP] += 1
                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                if close_flag:
                    findbugs_confuse_matrix[TP] += 1
                    pmd_confuse_matrix[FN] += 1
                    sonarqube_confuse_matrix[TP] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1
            elif findbugs_num == 0 and pmd_num != 0 and sonarqube_num != 0:
                if open_flag:
                    findbugs_confuse_matrix[TN] += 1
                    pmd_confuse_matrix[FP] += 1
                    sonarqube_confuse_matrix[FP] += 1

                    findbugs_pmd_confuse_matrix[FP] += 1
                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                if close_flag:
                    findbugs_confuse_matrix[FN] += 1
                    pmd_confuse_matrix[TP] += 1
                    sonarqube_confuse_matrix[TP] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1
            elif findbugs_num != 0 and pmd_num != 0 and sonarqube_num != 0:
                if open_flag:
                    findbugs_confuse_matrix[FP] += 1
                    pmd_confuse_matrix[FP] += 1
                    sonarqube_confuse_matrix[FP] += 1

                    findbugs_pmd_confuse_matrix[FP] += 1
                    findbugs_sonarqube_confuse_matrix[FP] += 1
                    pmd_sonarqube_confuse_matrix[FP] += 1
                if close_flag:
                    findbugs_confuse_matrix[TP] += 1
                    pmd_confuse_matrix[TP] += 1
                    sonarqube_confuse_matrix[TP] += 1

                    findbugs_pmd_confuse_matrix[TP] += 1
                    findbugs_sonarqube_confuse_matrix[TP] += 1
                    pmd_sonarqube_confuse_matrix[TP] += 1


    print('Under review num: ' + str(under_review_count))
    print(findbugs_confuse_matrix)
    print(pmd_confuse_matrix)
    print(sonarqube_confuse_matrix)

    print(findbugs_pmd_confuse_matrix)
    print(findbugs_sonarqube_confuse_matrix)
    print(pmd_sonarqube_confuse_matrix)

    print('---------------------------------------------------------------')
    findbugs_precision = get_precision(findbugs_confuse_matrix[FP], findbugs_confuse_matrix[TP])
    findbugs_accuracy = get_accuracy(findbugs_confuse_matrix[FN], findbugs_confuse_matrix[FP], findbugs_confuse_matrix[TN], findbugs_confuse_matrix[TP])
    findbugs_recall = get_recall(findbugs_confuse_matrix[FN], findbugs_confuse_matrix[TP])
    findbugs_f1_score = get_f1(findbugs_precision, findbugs_recall, beta=10)
    print('Findbugs Precision: {}'.format(findbugs_precision))
    print('Findbugs Accuracy: {}'.format(findbugs_accuracy))
    print('Findbugs Recall: {}'.format(findbugs_recall))
    print('Findbugs F1_Score: {}'.format(findbugs_f1_score))
    print('---------------------------------------------------------------')
    pmd_precision = get_precision(pmd_confuse_matrix[FP], pmd_confuse_matrix[TP])
    pmd_accuracy = get_accuracy(pmd_confuse_matrix[FN], pmd_confuse_matrix[FP], pmd_confuse_matrix[TN], pmd_confuse_matrix[TP])
    pmd_recall = get_recall(pmd_confuse_matrix[FN], pmd_confuse_matrix[TP])
    pmd_f1_score = get_f1(pmd_precision, pmd_recall, beta=10)
    print('PMD Precision: {}'.format(pmd_precision))
    print('PMD Accuracy: {}'.format(pmd_accuracy))
    print('PMD Recall: {}'.format(pmd_recall))
    print('PMD F1_Score: {}'.format(pmd_f1_score))
    print('---------------------------------------------------------------')
    sonarqube_precision = get_precision(sonarqube_confuse_matrix[FP], sonarqube_confuse_matrix[TP])
    sonarqube_accuracy = get_accuracy(sonarqube_confuse_matrix[FN], sonarqube_confuse_matrix[FP], sonarqube_confuse_matrix[TN], sonarqube_confuse_matrix[TP])
    sonarqube_recall = get_recall(sonarqube_confuse_matrix[FN], sonarqube_confuse_matrix[TP])
    sonarqube_f1_score = get_f1(sonarqube_precision, sonarqube_recall, beta=10)
    print('Sonarqube Precision: {}'.format(sonarqube_precision))
    print('Sonarqube Accuracy: {}'.format(sonarqube_accuracy))
    print('Sonarqube Recall: {}'.format(sonarqube_recall))
    print('Sonarqube F1_Score: {}'.format(sonarqube_f1_score))
    print('---------------------------------------------------------------')
    findbugs_pmd_precision = get_precision(findbugs_pmd_confuse_matrix[FP], findbugs_pmd_confuse_matrix[TP])
    findbugs_pmd_accuracy = get_accuracy(findbugs_pmd_confuse_matrix[FN], findbugs_pmd_confuse_matrix[FP], findbugs_pmd_confuse_matrix[TN], findbugs_pmd_confuse_matrix[TP])
    findbugs_pmd_recall = get_recall(findbugs_pmd_confuse_matrix[FN], findbugs_pmd_confuse_matrix[TP])
    findbugs_pmd_f1_score = get_f1(findbugs_pmd_precision, findbugs_pmd_recall, beta=10)
    print('Findbugs_PMD Precision: {}'.format(findbugs_pmd_precision))
    print('Findbugs_PMD Accuracy: {}'.format(findbugs_pmd_accuracy))
    print('Findbugs_PMD Recall: {}'.format(findbugs_pmd_recall))
    print('Findbugs_PMD F1_Score: {}'.format(findbugs_pmd_f1_score))
    print('---------------------------------------------------------------')
    findbugs_sonarqube_precision = get_precision(findbugs_sonarqube_confuse_matrix[FP], findbugs_sonarqube_confuse_matrix[TP])
    findbugs_sonarqube_accuracy = get_accuracy(findbugs_sonarqube_confuse_matrix[FN], findbugs_sonarqube_confuse_matrix[FP], findbugs_sonarqube_confuse_matrix[TN], findbugs_sonarqube_confuse_matrix[TP])
    findbugs_sonarqube_recall = get_recall(findbugs_sonarqube_confuse_matrix[FN], findbugs_sonarqube_confuse_matrix[TP])
    findbugs_sonarqube_f1_score = get_f1(findbugs_sonarqube_precision, findbugs_sonarqube_recall, beta=10)
    print('Findbugs_Sonarqube Precision: {}'.format(findbugs_sonarqube_precision))
    print('Findbugs_Sonarqube Accuracy: {}'.format(findbugs_sonarqube_accuracy))
    print('Findbugs_Sonarqube Recall: {}'.format(findbugs_sonarqube_recall))
    print('Findbugs_Sonarqube F1_Score: {}'.format(findbugs_sonarqube_f1_score))
    print('---------------------------------------------------------------')
    pmd_sonarqube_precision = get_precision(pmd_sonarqube_confuse_matrix[FP], pmd_sonarqube_confuse_matrix[TP])
    pmd_sonarqube_accuracy = get_accuracy(pmd_sonarqube_confuse_matrix[FN], pmd_sonarqube_confuse_matrix[FP], pmd_sonarqube_confuse_matrix[TN], pmd_sonarqube_confuse_matrix[TP])
    pmd_sonarqube_recall = get_recall(pmd_sonarqube_confuse_matrix[FN], pmd_sonarqube_confuse_matrix[TP])
    pmd_sonarqube_f1_score = get_f1(pmd_sonarqube_precision, pmd_sonarqube_recall, beta=10)
    print('PMD_Sonarqube Precision: {}'.format(pmd_sonarqube_precision))
    print('PMD_Sonarqube Accuracy: {}'.format(pmd_sonarqube_accuracy))
    print('PMD_Sonarqube Recall: {}'.format(pmd_sonarqube_recall))
    print('PMD_Sonarqube F1_Score: {}'.format(pmd_sonarqube_f1_score))
    print('---------------------------------------------------------------')

    res = []
    res.append(['tool', 'TP', 'FP', 'TN', 'FN', 'PRECISION', 'ACCURACY', 'RECALL', 'F1'])
    res.append(['findbugs'] + findbugs_confuse_matrix + [findbugs_precision, findbugs_accuracy, findbugs_accuracy, findbugs_f1_score])
    res.append(['pmd'] + pmd_confuse_matrix + [pmd_precision, pmd_accuracy, pmd_accuracy, pmd_f1_score])
    res.append(['sonarqube'] + sonarqube_confuse_matrix + [sonarqube_precision, sonarqube_accuracy, sonarqube_accuracy, sonarqube_f1_score])
    # res.append(['findbugs&pmd'] + findbugs_pmd_confuse_matrix + [findbugs_pmd_precision, findbugs_pmd_accuracy, findbugs_pmd_accuracy, findbugs_pmd_f1_score])
    # res.append(['findbugs&sonarqube'] + findbugs_sonarqube_confuse_matrix + [findbugs_sonarqube_precision, findbugs_sonarqube_accuracy, findbugs_sonarqube_accuracy, findbugs_sonarqube_f1_score])
    # res.append(['pmd&sonarqube'] + pmd_sonarqube_confuse_matrix + [pmd_sonarqube_precision, pmd_sonarqube_accuracy, pmd_sonarqube_accuracy, pmd_sonarqube_f1_score])

    return res


def get_all_report_warning(findbugs_path, pmd_path, sonarqube_path, dirname):
    total_res = get_all_warnings(findbugs_path, pmd_path, sonarqube_path)

    res = []
    for i in total_res.keys():
        tool_dic = total_res[i]

        findbugs_warning = tool_dic['findbugs']
        pmd_warning = tool_dic['pmd']
        sonarqube_warning = tool_dic['sonarqube']

        findbugs_num = len(findbugs_warning)
        pmd_num = len(pmd_warning)
        sonarqube_num = len(sonarqube_warning)

        line = []
        if (findbugs_num != 0 and pmd_num != 0 and sonarqube_num == 0) or (findbugs_num == 0 and pmd_num != 0 and sonarqube_num != 0) or (findbugs_num != 0 and pmd_num == 0 and sonarqube_num != 0):
            if findbugs_num == 0:
                for j in range(11):
                    line.append('')
            else:
                for j in findbugs_warning[0]:
                    line.append(j)
            if pmd_num == 0:
                for j in range(11):
                    line.append('')
            else:
                for j in pmd_warning[0]:
                    line.append(j)
            if sonarqube_num == 0:
                for j in range(11):
                    line.append('')
            else:
                for j in sonarqube_warning[0]:
                    line.append(j)
            res.append(line)

    if len(res) != 0:
        with open(dirname + '_same_warnings.csv', 'w', encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)

            csv_writer.writerows(res)

        f.close()


def process_project_folders(data_directory):
    for root, dirs, files in os.walk(data_directory):
        for dir_name in dirs:
            project_path = os.path.join(root, dir_name)
            labeled_files = [f for f in os.listdir(project_path) if '_labeled.csv' in f]

            findbugs_file = next((f for f in labeled_files if 'findbugs' in f), None)
            pmd_file = next((f for f in labeled_files if 'pmd' in f), None)
            sonarqube_file = next((f for f in labeled_files if 'sonarqube' in f), None)

            if findbugs_file and pmd_file and sonarqube_file:
                get_all_report_warning(os.path.join(project_path, findbugs_file),
                                       os.path.join(project_path, pmd_file),
                                       os.path.join(project_path, sonarqube_file), dir_name)

# Replace 'path_to_data_folder' with the actual path to your data folder
# process_project_folders('path_to_data_folder')


if __name__ == '__main__':
    # findbugs_path = 'findbugs_labeled.csv'
    # pmd_path = 'pmd_labeled.csv'
    # sonarqube_path = 'sonarqube_labeled.csv'
    # data_process(findbugs_path, pmd_path, sonarqube_path)

    process_project_folders('E:\SAToolRecommendation\Bug-Assessment-Tool\data')