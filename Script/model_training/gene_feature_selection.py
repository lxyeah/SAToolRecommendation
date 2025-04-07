import csv

import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier  # 使用KNN作为示例分类器
from deap import base, creator, tools, algorithms

X_list = []
y_list = []
with open('total_labeled_data_1.csv', 'r') as f:
    reader = csv.reader(f)
    for i in reader:
        X_list.append(i[:-3])
        y_list.append(i[-2])

# 创建 LabelEncoder 实例
label_encoder = LabelEncoder()

# 使用 LabelEncoder 对标签数据进行编码
encoded_labels = label_encoder.fit_transform(y_list)

# 加载数据
X = np.array(X_list)  # 特征数据，形状为(419, 302)
y = np.array(encoded_labels)  # 标签数据，形状为(400,)，包含5个不同类别

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用SMOTE进行过采样
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_scaled, y)

# 定义适应度函数
def evalFeatureSubset(individual, max_features=30):
    # 选择个体中标记为1的特征
    mask = np.array(individual).astype(bool)
    # 对于没有选择任何特征或特征数量超限的个体给予极大的惩罚
    if not np.any(mask):
        return (0,)  # 使用一个大的负数作为惩罚


    # 使用逻辑回归模型
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42)  # 增加迭代次数以确保收敛
    # 使用准确率作为性能指标
    scores = cross_val_score(model, X_subset, y_resampled, cv=5, scoring='accuracy')
    accuracy = np.mean(scores)
    # print(accuracy)
    num_features = sum(mask)
    # 加大特征数量的惩罚权重
    penalty = num_features * 0.01  # 可调整此权重以找到最佳平衡
    return (accuracy - penalty,)


# 设置DEAP框架的基础结构
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 0, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=X_resampled.shape[1])
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalFeatureSubset,  max_features=30)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

# 运行遗传算法
population = toolbox.population(n=50)
NGEN = 40
best_ind = None
# for gen in range(NGEN):
#     print(gen)
#     offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
#     fits = toolbox.map(toolbox.evaluate, offspring)
#     for fit, ind in zip(fits, offspring):
#         ind.fitness.values = fit
#     population = toolbox.select(offspring, k=len(population))
#     top1 = tools.selBest(population, 1)[0]
#     if best_ind is None or top1.fitness.values > best_ind.fitness.values:
#         best_ind = top1
#
# print("Best individual is:", best_ind)
# print("Number of selected features:", sum(best_ind))
# print("With accuracy of:", best_ind.fitness.values)

if __name__ == '__main__':
    mask = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0]
    X_subset = X_resampled[:, mask]
    # 使用逻辑回归模型
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42)  # 增加迭代次数以确保收敛
    # 使用准确率作为性能指标
    cross_val_precision_scores = cross_val_score(model, X_subset, y_resampled, cv=5, scoring='precision_weighted')
    print(cross_val_precision_scores)