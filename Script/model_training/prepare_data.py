import os
import src.configure as c
import csv


def prepare_label_data():
    data_dir = r'E:\SAToolRecommendation\Bug-Assessment-Tool\tool_evaluation_result'
    data_count = 0
    data = []
    for file in os.listdir(data_dir):
        if file.endswith('evaluation.csv'):
            data_count += 1
            lines = []
            with open(data_dir + '\\' + file, 'r') as f:
                reader = csv.reader(f)
                for i in reader:
                    lines.append(i)
            f.close()

            best_tool = []
            for line in lines[1:4]:
                tool = line[0]
                precision = line[-1]
                if len(best_tool) == 0:
                    best_tool = [tool, precision]
                else:
                    if precision < best_tool[1]:
                        continue
                    elif precision > best_tool[1]:
                        best_tool = [tool, precision]
                    else:
                        tool_num = len(tool.split('&'))
                        best_tool_num = len(best_tool[0].split('&'))
                        if tool_num < best_tool_num:
                            best_tool = [tool, precision]
                        else:
                            continue
            pro = file.split('_tool_evaluation.csv')[0]
            # labels = [pro]
            # for line in lines[1:4]:
            #     labels.append(line[-1])


            # if float(best_tool[1]) != 0:
            data.append([pro, best_tool[0], best_tool[1]])
            # data.append(labels)

    return data


def clean_feature(feature_file):
    feature_data = []
    res = []
    with open(feature_file, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            feature_data.append(line)
    f.close()

    for i in feature_data[1:]:
        print(feature_file)
        if 'test' in i[2]:
            continue
        else:
            res.append(i)

    with open(feature_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(res)
    f.close()


def clean_all_feature(data):
    feature_dir = c.feature_dir
    for data_info in data:
        pro = data_info[0]
        feature_file = feature_dir + '/' + pro + '/' + pro + '.csv'
        clean_feature(feature_file)


def prepare_feature_data(feature_file):
    header = []

    feature_data = []
    with open(feature_file, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            feature_data.append(i)
    f.close()

    feature_dic = {}
    for i in feature_data:
        kind = i[0]
        feature_type_dic = c.feature_type_dic
        feature_type = ''
        for j in feature_type_dic.keys():
            if kind in feature_type_dic[j]:
                feature_type = j
                break
        if feature_type == '':
            continue

        if feature_type not in feature_dic:
            feature_dic[feature_type] = [i[3:]]
        else:
            feature_dic[feature_type].append(i[3:])

    pro_feature_list = []
    for i in c.feature_type_dic.keys():
        total_file_feature = []
        average_file_feature = []

        if i not in feature_dic.keys():
            total_file_feature = [-1] * c.feature_type_num_dic[i]
            average_file_feature = [-1] * c.feature_type_num_dic[i]
        else:
            file_feature_list = feature_dic[i]
            temp_header = []
            count = 0
            for j in file_feature_list:

                index = 0
                idx = 0
                for k in j:
                    if k != '':
                        if count == 0:
                            temp_header.append(i + '_' + c.metrics_headers[3:][idx] + '_total')
                        if index == len(total_file_feature):
                            total_file_feature.append(float(k))
                        else:
                            total_file_feature[index] += float(k)
                        index += 1
                    idx += 1
                count += 1
            for j in range(len(total_file_feature)):
                tmp = temp_header[j].split('total')[0] + 'average'
                temp_header.append(tmp)
                average_file_feature.append(total_file_feature[j] / len(file_feature_list))

            print(i)
            print(len(total_file_feature))
            print(len(average_file_feature))
            header += temp_header
        pro_feature_list += total_file_feature
        pro_feature_list += average_file_feature

    return pro_feature_list, header


def prepare_all_feature_data(data):
    feature_data = []

    feature_dir = c.feature_dir
    for data_info in data:
        pro = data_info[0]
        feature_file = feature_dir + '/' + pro + '/' + pro + '.csv'
        pro_feature_list, header = prepare_feature_data(feature_file)
        pro_feature_list += data_info
        header += ['Pro', 'Tool', 'Recall']
        feature_data.append(pro_feature_list)

    return feature_data, header


def show_best_tool_distribution(data):
    findbugs = 0
    pmd = 0
    sonarqube = 0
    findbugs_pmd = 0
    findbugs_sonarqube = 0
    pmd_sonarqube = 0
    for i in data:
        print(i)
        if i[1] == 'findbugs':
            findbugs += 1
        if i[1] == 'pmd':
            pmd += 1
        if i[1] == 'sonarqube':
            sonarqube += 1
        if i[1] == 'findbugs&pmd':
            findbugs_pmd += 1
        if i[1] == 'findbugs&sonarqube':
            findbugs_sonarqube += 1
        if i[1] == 'pmd&sonarqube':
            pmd_sonarqube += 1

    print(findbugs)
    print(pmd)
    print(sonarqube)
    print(findbugs_pmd)
    print(findbugs_sonarqube)
    print(pmd_sonarqube)
    print(len(data))


if __name__ == '__main__':
    data = prepare_label_data()
    # show_best_tool_distribution(data)
    clean_all_feature(data)
    feature_data, header = prepare_all_feature_data(data)
    print(feature_data)
    for i in feature_data:
        print(len(i))

    with open('total_labeled_data_f10.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(feature_data)
    f.close()

