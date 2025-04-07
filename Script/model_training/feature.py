import pandas as pd
from sklearn.feature_selection import RFE
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.svm import SVR
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from imblearn.over_sampling import SMOTE

# 读取数据集
data = pd.read_csv('new_data.csv', header=None)

# 删除倒数第三列和倒数第一列
data = data.iloc[:, :-3].join(data.iloc[:, -2:-1])

# 分离特征和目标变量
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# 使用标签编码将目标变量转换为数值特征
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# 获取所有唯一编码的标签
unique_encoded_labels = np.unique(y)

# 将每个数值编码转换回其对应的文本标签
text_labels = label_encoder.inverse_transform(unique_encoded_labels)

# 将文本标签保存在一个列表中
text_labels_list = list(text_labels)

print("每个数值对应的文本标签:", text_labels_list)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化随机森林模型
rf = RandomForestClassifier(n_estimators=100, random_state=42)
lr = LogisticRegression(solver='liblinear', max_iter=2000, random_state=42)
# svr = SVR(kernel="linear")
dt = DecisionTreeClassifier(random_state=42)
knn = KNeighborsClassifier(n_neighbors=3)
mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=2000, random_state=42)

# 设置RFE（递归特征消除）, 选择保留的特征数目例如20
rfe = RFE(estimator=rf, n_features_to_select=100, step=1)

# 训练RFE模型
rfe.fit(X_train, y_train)

# 查看被选择的特征（返回布尔值数组）
selected_features = rfe.support_

# 初始化SMOTE
# smote = SMOTE(random_state=42)

# 对训练集应用SMOTE进行过采样
# X_train, y_train = smote.fit_resample(X_train, y_train)


# 使用RFE选定的特征进行训练
X_train_selected = X_train.loc[:, selected_features]
X_test_selected = X_test.loc[:, selected_features]


def compute(X_train_selected, X_test_selected, y_train, y_test, model):
    # 使用选定的特征重新训练随机森林模型
    model.fit(X_train_selected, y_train)

    # 使用随机森林模型进行预测
    y_pred = model.predict(X_test_selected)

    print(model)

    # 计算准确度
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)

    # 计算精确度
    precision = precision_score(y_test, y_pred, average='macro', zero_division=0)  # 使用'macro'平均计算方法
    print("Precision:", precision)

    # 计算召回率
    recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
    print("Recall:", recall)

    # 计算F1分数
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
    print("F1 Score:", f1)


compute(X_train_selected, X_test_selected, y_train, y_test, rf)
compute(X_train_selected, X_test_selected, y_train, y_test, lr)
compute(X_train_selected, X_test_selected, y_train, y_test, dt)
compute(X_train_selected, X_test_selected, y_train, y_test, mlp)

X_train_selected = np.ascontiguousarray(X_train_selected)
X_test_selected = np.ascontiguousarray(X_test_selected)
compute(X_train_selected, X_test_selected, y_train, y_test, knn)

# compute(X_train_selected, X_test_selected, y_train, y_test, svr)

# 定义 XGBoost 模型
# xgb_classifier = XGBClassifier()
#
# # 定义参数网格
# param_grid = {
#     'n_estimators': [100, 300] ,# 决策树数量
#     'max_depth': [3] # 决策树最大深度
# }
#
# # 定义网格搜索对象
# grid_search = GridSearchCV(xgb_classifier, param_grid, cv=5, scoring='accuracy')
#
# # 拟合模型
# grid_search.fit(X_train, y_train)
#
# # 输出最优参数
# print("最优参数:", grid_search.best_params_)
#
# # 获取最优模型
# best_model = grid_search.best_estimator_
#
# # 进行预测
# y_pred = best_model.predict(X_test)
#
# # 计算准确率
# accuracy = accuracy_score(y_test, y_pred)
# print("准确率:", accuracy)

import matplotlib.pyplot as plt

# 假设 best_model 已经是从上面的代码中获得的最优模型
# best_model = grid_search.best_estimator_

# 获取特征重要性
# feature_importances = best_model.feature_importances_
#
# # 获取特征名
# feature_names = X_train.columns
#
# # 排序特征重要性
# sorted_idx = feature_importances.argsort()[::-1]

# 绘图
# plt.figure(figsize=(10, 33))
# plt.title("Feature Importances")
# plt.barh(range(len(sorted_idx)), feature_importances[sorted_idx], align="center")
# plt.yticks(range(len(sorted_idx)), feature_names[sorted_idx],fontsize=7)
# plt.gca().invert_yaxis()  # 逆转y轴，确保特征按重要性递减顺序排列
# plt.tight_layout()
# plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# 选取前 top_features 个特征
# top_features = 9
# selected_features = feature_names[sorted_idx][:top_features]
# l = [4,8,9,10,11,12,13,16,18,19,20,21,22,23,24,25,26,27,31, 32,33,34,35,38]
# selected_features = feature_names[170:209]
# selected_features = rfe.support_

# 根据选取的特征筛选数据集
# X_train_selected = X_train.loc[:, selected_features]
# X_test_selected = X_test.loc[:, selected_features]

# 对数据进行标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_selected)
X_test_scaled = scaler.transform(X_test_selected)

# 使用PCA进行降维
pca = PCA(n_components=5)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, SVR
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def evaluate_model(model, X_train, y_train, X_test, y_test, labels):
    # 训练模型
    model.fit(X_train, y_train)

    # 预测测试集
    y_pred = model.predict(X_test)

    # 输出微平均、宏平均和加权平均指标
    precision_micro = precision_score(y_test, y_pred, average='micro', zero_division=0)
    recall_micro = recall_score(y_test, y_pred, average='micro', zero_division=0)
    f1_micro = f1_score(y_test, y_pred, average='micro', zero_division=0)

    precision_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)

    precision_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"微平均 - 精确率: {precision_micro}, 召回率: {recall_micro}, F1 分数: {f1_micro}")
    print(f"宏平均 - 精确率: {precision_macro}, 召回率: {recall_macro}, F1 分数: {f1_macro}")
    print(f"加权平均 - 精确率: {precision_weighted}, 召回率: {recall_weighted}, F1 分数: {f1_weighted}\n")

    # 输出每个工具的指标
    for i, label in enumerate(labels):
        precision = precision_score(y_test, y_pred, average=None, zero_division=0)[i]
        recall = recall_score(y_test, y_pred, average=None, zero_division=0)[i]
        f1 = f1_score(y_test, y_pred, average=None, zero_division=0)[i]

        print(f"{model.__class__.__name__} 对 {label} 的性能指标:")
        print(f"精确率: {precision}")
        print(f"召回率: {recall}")
        print(f"F1 分数: {f1}\n")



# 定义标签
labels = ['SpotBugs', 'PMD', 'SonarQube']

# 测试不同模型
models = [
    RandomForestClassifier(n_estimators=1000, max_depth=None),
    DecisionTreeClassifier(),
    LogisticRegression(),
    SVC(),
    MLPClassifier(hidden_layer_sizes=(100,))
]

for model in models:
    evaluate_model(model, X_train_pca, y_train, X_test_pca, y_test, labels)

def evaluate_rf_model(X_train, y_train, X_test, y_test, labels, num_trials=10):
    """
    多次训练和评估随机森林模型，并输出平均指标。

    参数:
    X_train: numpy数组, 训练集的特征。
    y_train: numpy数组, 训练集的标签。
    X_test: numpy数组, 测试集的特征。
    y_test: numpy数组, 测试集的标签。
    labels: 列表, 包含所有可能的类别名。
    num_trials: 整数, 训练和预测的次数。

    返回:
    无。
    """
    accuracies = []
    precisions_micro = []
    recalls_micro = []
    f1s_micro = []
    precisions_macro = []
    recalls_macro = []
    f1s_macro = []
    precisions_weighted = []
    recalls_weighted = []
    f1s_weighted = []

    # 多次训练和预测
    for _ in range(num_trials):
        # 初始化随机森林模型
        rf_model = RandomForestClassifier(n_estimators=1000, max_depth=None)

        # 训练模型
        rf_model.fit(X_train, y_train)

        # 预测测试集
        y_pred = rf_model.predict(X_test)

        # 计算并存储指标
        accuracies.append(accuracy_score(y_test, y_pred))

        precisions_micro.append(precision_score(y_test, y_pred, average='micro', zero_division=0))
        recalls_micro.append(recall_score(y_test, y_pred, average='micro', zero_division=0))
        f1s_micro.append(f1_score(y_test, y_pred, average='micro', zero_division=0))

        precisions_macro.append(precision_score(y_test, y_pred, average='macro', zero_division=0))
        recalls_macro.append(recall_score(y_test, y_pred, average='macro', zero_division=0))
        f1s_macro.append(f1_score(y_test, y_pred, average='macro', zero_division=0))

        precisions_weighted.append(precision_score(y_test, y_pred, average='weighted', zero_division=0))
        recalls_weighted.append(recall_score(y_test, y_pred, average='weighted', zero_division=0))
        f1s_weighted.append(f1_score(y_test, y_pred, average='weighted', zero_division=0))

    # 平均化指标
    avg_accuracy = np.mean(accuracies)
    avg_precision_micro = np.mean(precisions_micro)
    avg_recall_micro = np.mean(recalls_micro)
    avg_f1_micro = np.mean(f1s_micro)

    avg_precision_macro = np.mean(precisions_macro)
    avg_recall_macro = np.mean(recalls_macro)
    avg_f1_macro = np.mean(f1s_macro)

    avg_precision_weighted = np.mean(precisions_weighted)
    avg_recall_weighted = np.mean(recalls_weighted)
    avg_f1_weighted = np.mean(f1s_weighted)

    # 输出结果
    print(f"随机森林模型的平均准确率: {avg_accuracy}")
    print(f"微平均 - 精确率: {avg_precision_micro}, 召回率: {avg_recall_micro}, F1分数: {avg_f1_micro}")
    print(f"宏平均 - 精确率: {avg_precision_macro}, 召回率: {avg_recall_macro}, F1分数: {avg_f1_macro}")
    print(f"加权平均 - 精确率: {avg_precision_weighted}, 召回率: {avg_recall_weighted}, F1分数: {avg_f1_weighted}")

    # 输出每个工具的指标
    print(classification_report(y_test, y_pred, target_names=labels, zero_division=0))

# 假设 X_train, y_train, X_test, y_test 和 labels 已定义
evaluate_rf_model(X_train_pca, y_train, X_test_pca, y_test, labels)




def evaluate_random_predictions(y_test, labels, num_trials=10):
    """
    通过随机预测多次并取平均的方法评估模型性能。

    参数:
    y_test: numpy数组, 测试集的实际标签。
    labels: 列表, 包含所有可能的类别名。
    num_trials: 整数, 表示随机预测的次数。

    返回:
    字典，包含平均的性能指标。
    """
    accuracies = []
    precisions = []
    recalls = []
    f1_scores = []

    # 多次随机预测
    for _ in range(num_trials):
        # 随机预测
        np.random.seed()  # 每次循环产生不同的随机预测
        y_pred_random = np.random.choice(labels, size=len(y_test))

        # 计算指标
        accuracies.append(accuracy_score(y_test, y_pred_random))
        precisions.append(precision_score(y_test, y_pred_random, average='weighted', zero_division=0))
        recalls.append(recall_score(y_test, y_pred_random, average='weighted', zero_division=0))
        f1_scores.append(f1_score(y_test, y_pred_random, average='weighted', zero_division=0))

    # 计算平均指标
    avg_accuracy = np.mean(accuracies)
    avg_precision = np.mean(precisions)
    avg_recall = np.mean(recalls)
    avg_f1 = np.mean(f1_scores)

    return {
        "平均准确率": avg_accuracy,
        "平均精确率": avg_precision,
        "平均召回率": avg_recall,
        "平均F1分数": avg_f1
    }

# 假设 y_test 和 labels 已定义
y_test = np.array(y_test)  # 确保 y_test 为 numpy 数组

# 评估随机预测
random_metrics = evaluate_random_predictions(y_test, [0,1,2])

# 输出结果
print("随机预测（平均）:")
for key, value in random_metrics.items():
    print(f"{key}: {value}")

for i, label in enumerate(labels):
    # 仅预测一种工具
    y_pred_single = np.full(len(y_test), i)  # 或选择其他类别

    # 输出预测一种工具的性能指标
    print(f"仅预测一种工具: {label}")
    print(f"精确率: {precision_score(y_test, y_pred_single, average='weighted', zero_division=0)}")
    print(f"召回率: {recall_score(y_test, y_pred_single, average='weighted', zero_division=0)}")
    print(f"F1 分数: {f1_score(y_test, y_pred_single, average='weighted', zero_division=0)}")



# 计算每个主成分的累计方差
cumulative_variance_ratio = np.cumsum(pca.explained_variance_ratio_)

# 输出每个主成分的累计方差
for i, variance_ratio in enumerate(cumulative_variance_ratio):
    print(f"Principal Component {i+1}: 累计方差 = {variance_ratio:.4f}")

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 设置matplotlib支持中文字符
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 假设X_train已经准备好并且是一个二维numpy数组

# 标准化特征值
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 测试不同的n_components值
n_components_list = range(1, 50)  # 从1到20
explained_variance_ratios = []

for n_components in n_components_list:
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train_scaled)
    explained_variance_ratio = np.sum(pca.explained_variance_ratio_)
    explained_variance_ratios.append(explained_variance_ratio)

# 可视化使用折线图
plt.figure(figsize=(12, 8))
plt.plot(n_components_list, explained_variance_ratios, marker='o')
plt.xlabel('主成分数量')
plt.ylabel('累积解释方差比')
plt.title('PCA分析：不同主成分数量的累积解释方差比')
plt.xticks(n_components_list)  # 显示所有x轴刻度
plt.grid(True)  # 添加网格
plt.show()

from scipy.spatial import ConvexHull
def calculate_polygon_area(points):
    """
    计算由给定点序列构成的多边形的面积。
    参数:
    points: numpy数组, 包含多个二元组，每个二元组代表多边形的一个顶点坐标 (x, y)。

    返回值:
    多边形的面积。
    """
    # 生成凸包并获取按顺序排列的点集
    hull = ConvexHull(points)
    ordered_points = points[hull.vertices]

    x_coords = ordered_points[:, 0]
    y_coords = ordered_points[:, 1]

    # 计算面积
    area = 0.5 * np.abs(np.dot(x_coords, np.roll(y_coords, 1)) - np.dot(y_coords, np.roll(x_coords, 1)))

    return area


def filter_points(points, x_range=(-5, 5), y_range=(-5, 5)):
    """
    筛选坐标在给定范围内的点。

    参数:
    points: numpy数组, 包含多个二元组，每个二元组代表多边形的一个顶点坐标 (x, y)。
    x_range: 元组, 指定x坐标的范围，例如(-5, 5)。
    y_range: 元组, 指定y坐标的范围，例如(-5, 5)。

    返回:
    筛选后的点集。
    """
    # 获取所有符合条件的点
    # 获取所有符合条件的点
    x_filter = (points[:, 0] >= x_range[0]) & (points[:, 0] <= x_range[1])
    y_filter = (points[:, 1] >= y_range[0]) & (points[:, 1] <= y_range[1])

    # 返回同时满足x和y条件的点集
    return points[x_filter & y_filter], y[x_filter & y_filter]

from sklearn.preprocessing import StandardScaler

# 创建一个StandardScaler对象
scaler = StandardScaler()
X_selected = X[selected_features]
# 对数据进行归一化
X_normalized = scaler.fit_transform(X_selected)
# 使用PCA进行降维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_normalized)

X_pca_filtered, y_filtered = np.array(X_pca), y

# 假设X_pca和y已经定义并准备好数据
labels = ['SpotBugs', 'PMD', 'SonarQube']

# 按照给定标签筛选实例
for i, label in enumerate(labels):
    effective_mask = y_filtered == i  # 为筛选后的数据生成过滤器
    effective_points = X_pca_filtered[effective_mask]  # 根据过滤器选择有效点集

    # 计算有效实例的足迹面积

    area = calculate_polygon_area(effective_points)
    print(f"{label} 的有效实例足迹面积是: {area}")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, label in enumerate(labels):
    effective_mask = y == i
    ineffective_mask = ~effective_mask

    axes[i].scatter(X_pca[ineffective_mask, 0], X_pca[ineffective_mask, 1], marker='x', color='blue', label='Ineffective')
    axes[i].scatter(X_pca[effective_mask, 0], X_pca[effective_mask, 1], marker='o', color='orange', label='Effective')
    axes[i].tick_params(axis='both', labelsize=14)
    axes[i].legend(loc='upper right', fontsize=16)
    axes[i].set_title(label, fontsize=18, loc='left')
    axes[i].set_xlim(-5, 5)
    axes[i].set_ylim(-5, 5)
    axes[i].set_xticks(np.arange(-5, 6, 1))
    axes[i].set_yticks(np.arange(-5, 6, 1))
    axes[i].set_aspect('equal', adjustable='box')
    axes[i].spines['top'].set_visible(False)
    axes[i].spines['right'].set_visible(False)

# 显式设置子图间距
fig.subplots_adjust(wspace=0.4)

plt.show()

# 保存图形时减少空白区域
fig.savefig('my_plot.png', bbox_inches='tight')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 创建一个StandardScaler对象
scaler = StandardScaler()
X_selected = X[selected_features]
# 对数据进行归一化
X_normalized = scaler.fit_transform(X_selected)
# 使用PCA进行降维
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_normalized)

# 绘制三个三维子图
fig = plt.figure(figsize=(8, 16))

# 定义标签列表
labels = ['findbugs', 'pmd', 'sonarqube']

for i, label in enumerate(labels):
    # 为每个标签创建子图
    ax = fig.add_subplot(3, 1, i + 1, projection='3d')

    # 有效的点
    effective_mask = y == i
    # 无效的点
    ineffective_mask = ~effective_mask


    ax.scatter(X_pca[ineffective_mask, 0], X_pca[ineffective_mask, 1], X_pca[ineffective_mask, 2], marker='x',
               color='blue', label='Ineffective')
    ax.scatter(X_pca[effective_mask, 0], X_pca[effective_mask, 1], X_pca[effective_mask, 2], marker='o', color='orange',
               label='Effective')

    # 设置标签和标题
    ax.set_xlabel('Principal Component 1', fontsize=12)
    ax.set_ylabel('Principal Component 2', fontsize=12)
    ax.set_zlabel('Principal Component 3', fontsize=12)
    ax.set_title(label, fontsize=14)

    # 设置图例
    ax.legend(fontsize=10)

# plt.tight_layout()
plt.show()