import csv
import os
import random
import statistics
import src.utils.javaparser_tool as jt
import src.utils.find_file
import numpy as np
import feature_clustering as fc
import src.configure as c
from src.get_revision.get_revision_main import choose_tag_list
from src.utils.GitRepository import GitRepository
import matplotlib.pyplot as plt


class FeatureExtractor(object):

    # def __init__(self, pro_name, local_path, remote_path):
        # self.pro_name = pro_name
        # self.path = local_path
        # self.gitRepo = GitRepository(local_path, remote_path)
        # self.project_feature = {}
        # self.warning_feature = {}

    # 获取该tag的项目开发时长
    # def project_lifetime_feature_extract(self, tag):
    #     # 获取指定的tag
    #     try:
    #         tag_commit = self.gitRepo.get_tag_commit_hash(tag)
    #     except IndexError:
    #         print(f"Tag '{tag}' not found.")
    #         return None
    #
    #     # 获取第一个commit
    #     first_commit = self.gitRepo.get_commit_hash_by_index(-1)
    #
    #     # 计算两个commit之间的时间
    #     duration = tag_commit.committed_datetime - first_commit.committed_datetime
    #
    #     return duration.days

    # 获取该tag的commit索引
    # def project_commit_number_feature_extract(self, tag):
    #     # 获取指定的tag
    #     try:
    #         tag_commit = self.gitRepo.get_tag_commit_hash(tag)
    #     except IndexError:
    #         print(f"Tag '{tag}' not found.")
    #         return None
    #
    #     index = self.gitRepo.get_commit_index(tag_commit.hexsha)
    #
    #     return index

    def get_findbugs_warning_num(self, findbugs_warnings):
        return len(findbugs_warnings)

    def get_pmd_warning_num(self, pmd_warnings):
        return len(pmd_warnings)

    def get_sonarqube_warning_num(self, sonarqube_warnings):
        return len(sonarqube_warnings)

    def get_warning_num_in_same_method_by_findbugs(self, findbugs_warnings):


        method_dic = {}
        for i in findbugs_warnings:
            package = i[3]
            method = i[5]

            if method == 'NO_METHOD':
                continue

            if package + '_' + method not in method_dic:
                method_dic[package + '_' + method] = 1
            else:
                method_dic[package + '_' + method] += 1

        value_list = list(method_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_warning_num_in_same_method_by_pmd(self, pmd_warnings):

        method_dic = {}
        for i in pmd_warnings:
            file = str(i[2])

            if not file.endswith('.java'):
                continue

            location = i[4]

            method = jt.find_method_of_line(file, location)

            if method is None:
                continue

            if file.split('\\')[-1] + '_' + method not in method_dic:
                method_dic[file.split('\\')[-1] + '_' + method] = 1
            else:
                method_dic[file.split('\\')[-1] + '_' + method] += 1

        value_list = list(method_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_warning_num_in_same_method_by_sonarqube(self, sonarqube_warnings, repo_dir):

        method_dic = {}
        for i in sonarqube_warnings:
            file = str(i[1])

            if not file.endswith('.java'):
                continue

            file = repo_dir + '//' + file.split(':')[1]
            location = i[2]

            method = jt.find_method_of_line(file, location)

            if method is None:
                continue

            if file.split('\\')[-1] + '_' + method not in method_dic:
                method_dic[file.split('\\')[-1] + '_' + method] = 1
            else:
                method_dic[file.split('\\')[-1] + '_' + method] += 1

        value_list = list(method_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_warning_num_in_same_file_by_findbugs(self, findbugs_warnings):

        package_dic = {}
        for i in findbugs_warnings:
            package = i[3]

            if package not in package_dic:
                package_dic[package] = 1
            else:
                package_dic[package] += 1

        value_list = list(package_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_warning_num_in_same_file_by_pmd(self, pmd_warnings):

        package_dic = {}
        for i in pmd_warnings:
            file = str(i[2])

            if file.split('\\')[-1] not in package_dic:
                package_dic[file.split('\\')[-1]] = 1
            else:
                package_dic[file.split('\\')[-1]] += 1

        value_list = list(package_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_warning_num_in_same_file_by_sonarqube(self, sonarqube_warnings):

        package_dic = {}
        for i in sonarqube_warnings:
            file = str(i[1])

            if file.split('\\')[-1] not in package_dic:
                package_dic[file.split('\\')[-1]] = 1
            else:
                package_dic[file.split('\\')[-1]] += 1

        value_list = list(package_dic.values())

        if len(value_list) == 0:
            return [0, 0, 0]

        # 先排序再取中位数
        value_list.sort()

        # statistics包实现
        medianValue = statistics.median(value_list)

        # stattistics包实现
        meanValue = statistics.mean(value_list)

        # 可以直接利用函数max()实现
        maxValue = max(value_list)

        return [maxValue, meanValue, medianValue]

    def get_findbugs_category_ratio(self, findbugs_warnings):
        if len(findbugs_warnings) == 0:
            return [0] * len(c.findbugs_category_list)

        category_dic = {}
        category_list = c.findbugs_category_list
        for i in category_list:
            category_dic[i] = 0
        for i in findbugs_warnings:
            category_dic[i[1]] += 1
        res = []
        for i in category_dic.keys():
            res.append(category_dic[i] / len(findbugs_warnings))
        return res

    def get_findbugs_type_ratio(self, findbugs_warnings):
        if len(findbugs_warnings) == 0:
            return [0] * len(c.findbugs_vtype_list)

        type_dic = {}
        type_list = c.findbugs_vtype_list
        for i in type_list:
            type_dic[i] = 0
        for i in findbugs_warnings:
            if i[2] in type_dic.keys():
                type_dic[i[2]] += 1
        res = []
        for i in type_dic.keys():
            res.append(type_dic[i] / len(findbugs_warnings))
        return res

    def get_pmd_category_ratio(self, pmd_warnings):
        if len(pmd_warnings) == 0:
            return [0] * len(c.pmd_category_list)

        category_dic = {}
        category_list = c.pmd_category_list
        for i in category_list:
            category_dic[i] = 0
        for i in pmd_warnings:
            category_dic[i[6]] += 1
        res = []
        for i in category_dic.keys():
            res.append(category_dic[i] / len(pmd_warnings))
        return res

    def get_pmd_type_ratio(self, pmd_warnings):
        if len(pmd_warnings) == 0:
            return [0] * len(c.pmd_vtype_list)

        type_dic = {}
        type_list = c.pmd_vtype_list
        for i in type_list:
            type_dic[i] = 0
        for i in pmd_warnings:
            type_dic[i[7]] += 1
        res = []
        for i in type_dic.keys():
            res.append(type_dic[i] / len(pmd_warnings))
        return res

    def get_sonarqube_category_ratio(self, sonarqube_warnings):
        if len(sonarqube_warnings) == 0:
            return [0] * len(c.sonarqube_category_list)

        category_dic = {}
        category_list = c.sonarqube_category_list
        for i in category_list:
            category_dic[i] = 0
        for i in sonarqube_warnings:
            category_dic[i[4]] += 1
        res = []
        for i in category_dic.keys():
            res.append(category_dic[i] / len(sonarqube_warnings))
        return res


    def print_cluster_result(self, warning_features, pro_list):
        # 假设你有一个包含多个特征的numpy数组 X
        X = np.array(warning_features)
        res = fc.KMeans_method(X, 10)

        cluster_dic = {}
        for i in range(len(res)):
            if res[i] not in cluster_dic.keys():
                cluster_dic[res[i]] = [(pro_list[i], X[i])]
            else:
                cluster_dic[res[i]].append((pro_list[i], X[i]))

        for i in cluster_dic.keys():
            print('-----------------------cluster ' + str(i) + '-----------------------------------')
            for j in cluster_dic[i]:
                print(j)

        cluster_new_dic = {}
        for i in cluster_dic.keys():
            pro_dic = {}
            cluster_list = cluster_dic[i]
            for j in cluster_list:
                pro_name = j[0]
                pro = pro_name.split('_')[0][:-2]
                if pro not in pro_dic.keys():
                    pro_dic[pro] = [j]
                else:
                    pro_dic[pro].append(j)
            cluster_new_dic[i] = pro_dic

        return cluster_new_dic


    def get_warning_features_and_pro(self, tool, feature_method):
        data_dir = c.data_dir
        data_list = os.listdir(data_dir)
        warning_features = []
        pro_list = []
        for i in data_list:
            for j in os.listdir(data_dir + '\\' + i):
                if j.endswith('{}_labeled.csv'.format(tool)):
                    pro_name = j.split('_{}_labeled.csv'.format(tool))[0]
                    pro_list.append(pro_name)

                    warnings = []
                    with open(data_dir + '\\' + i + '\\' + j, 'r', errors='ignore') as f:
                        reader = csv.reader(f)
                        for k in reader:
                            warnings.append(k)


                    res = feature_method(warnings)

                    warning_features.append(res)
                    print(pro_name + ': ', end='')
                    print(res)

        return warning_features, pro_list


    def draw_plot(self, data, x_heading, save_path):
        # 假设你有一个列表，如下所示
        data = data

        # 为每个数据创建一个索引，这将作为x轴
        indexes = range(len(data))

        # 创建一个新的图形
        plt.figure()

        # 使用bar()函数创建柱状图
        plt.bar(indexes, data)

        # 设置x轴的标签
        plt.xticks(indexes, x_heading)

        # 保存图片
        plt.savefig(save_path)


        # 显示图形
        # plt.show()



if __name__ == '__main__':
    extractor = FeatureExtractor()
    # findbugs_category_warning_features, findbugs_pro_list = extractor.get_warning_features_and_pro('findbugs', extractor.get_findbugs_category_ratio)
    # findbugs_vtype_warning_features, findbugs_pro_list = extractor.get_warning_features_and_pro('findbugs', extractor.get_findbugs_type_ratio)
    # pmd_category_warning_features, pmd_pro_list = extractor.get_warning_features_and_pro('pmd', extractor.get_pmd_category_ratio)
    # pmd_vtype_warning_features, pmd_pro_list = extractor.get_warning_features_and_pro('pmd', extractor.get_pmd_type_ratio)
    # sonarqube_warning_features, sonarqube_pro_list = extractor.get_warning_features_and_pro('sonarqube', extractor.get_sonarqube_category_ratio)

    # features = []
    # for i in range(len(findbugs_pro_list)):
    #     feature = findbugs_category_warning_features[i] + findbugs_vtype_warning_features[i] + pmd_category_warning_features[i] + pmd_vtype_warning_features[i]
    #     features.append(feature)
    #
    # X = np.array(features)

    # fc.K_distance_method(X, 10)
    # labels = fc.DBSCAN_method(X)
    #
    # cluster_dic = {}
    # for i in range(len(labels)):
    #     if labels[i] != -1:
    #         if labels[i] not in cluster_dic.keys():
    #             cluster_dic[labels[i]] = [findbugs_pro_list[i]]
    #         else:
    #             cluster_dic[labels[i]].append(findbugs_pro_list[i])
    #
    # for i in cluster_dic.keys():
    #     print('-------------' + str(i) + '------------')
    #     for j in cluster_dic[i]:
    #         print(j)

    # 提取警告相关特征
    findbugs_warning_features = extractor.get_warning_features_and_pro('findbugs', extractor.get_warning_num_in_same_method_by_findbugs)
    pmd_category_warning_features = extractor.get_warning_features_and_pro('pmd', extractor.get_warning_num_in_same_method_by_pmd)
    sonarqube_warning_features = extractor.get_warning_features_and_pro('sonarqube', extractor.get_warning_num_in_same_method_by_sonarqube())





    # # 生成聚类信息
    # cluster_new_dic = extractor.print_cluster_result(findbugs_category_warning_features, findbugs_pro_list)
    # res = ''
    # for i in cluster_new_dic.keys():
    #     res = res + '--------------' + str(i) + '--------------\n'
    #     for j in cluster_new_dic[i].keys():
    #         c_list = cluster_new_dic[i][j]
    #         res += j + ': '
    #         for m in c_list:
    #             res += m[0] + ' '
    #         res += '\n'
    #
    # with open('findbugs_category_cluster.txt', 'w') as f:
    #     f.write(res)
    # f.close()

    # 生成分布图
    # for i in range(len(findbugs_pro_list)):
    #     # extractor.draw_plot(findbugs_category_warning_features[i], c.findbugs_category_list, r'C:\Users\lxyeah\Desktop\SAToolRecommendation\Bug-Assessment-Tool\resources\category\findbugs\\' + findbugs_pro_list[i] + '.png')
    #     # extractor.draw_plot(findbugs_vtype_warning_features[i], c.findbugs_vtype_list, r'C:\Users\lxyeah\Desktop\SAToolRecommendation\Bug-Assessment-Tool\resources\vtype\findbugs\\' + findbugs_pro_list[i] + '.png')
    #     # extractor.draw_plot(pmd_category_warning_features[i], c.pmd_category_list, r'C:\Users\lxyeah\Desktop\SAToolRecommendation\Bug-Assessment-Tool\resources\category\pmd\\' + findbugs_pro_list[i] + '.png')
    #     extractor.draw_plot(pmd_vtype_warning_features[i], c.pmd_vtype_list, r'C:\Users\lxyeah\Desktop\SAToolRecommendation\Bug-Assessment-Tool\resources\vtype\pmd\\' + findbugs_pro_list[i] + '.png')





    # # 测试liftime计算
    # tag_list = ['achilles-1.0-beta', 'achilles-1.7.1', 'achilles-2.0.2', 'achilles-2.0.9', 'achilles-2.0.10-dse', 'achilles-3.0.4', 'achilles-3.0.7', 'achilles-3.1.4', 'achilles-3.0.20', 'achilles-4.0.0', 'achilles-4.1.0', 'achilles-4.2.1', 'achilles-5.1.3', 'achilles-5.2.1', 'achilles-5.3.0']
    # extractor = FeatureExtractor('Achilles', 'E:\\data_repo\\Achilles', 'https://github.com/doanduyhai/Achilles.git', tag_list)
    # lifetime = extractor.project_lifetime_feature_extract('achilles-1.0-beta')
    # index = extractor.project_commit_number_feature_extract('achilles-1.0-beta')
    # print(lifetime)
    # print(index)
