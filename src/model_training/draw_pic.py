from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from matplotlib.colors import Normalize
import csv
from sklearn.preprocessing import RobustScaler
import matplotlib

# 读取CSV文件的标题行
def get_headers_from_csv(file_path):
    # 仅读取第一行作为标题
    df = pd.read_csv(file_path, nrows=0)
    return df.columns.tolist()

# 根据索引列表返回对应的标题
def get_headers_by_index(file_path, index_list):
    headers = get_headers_from_csv(file_path)
    # 根据索引列表获取对应的标题
    selected_headers = [headers[i] for i in index_list if i < len(headers)]
    return selected_headers



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

# 设置RFE（递归特征消除）, 选择保留的特征数目例如20
rfe = RFE(estimator=rf, n_features_to_select=100, step=1)

# 训练RFE模型
rfe.fit(X_train, y_train)

# 查看被选择的特征（返回布尔值数组）
selected_features = rfe.support_

# 使用RFE选定的特征进行训练
X_train_selected = X_train.loc[:, selected_features]
X_test_selected = X_test.loc[:, selected_features]

# 获取特征的排名（1 表示最重要）
feature_ranking = rfe.ranking_

# 筛选出排名前9的特征的索引
top_9_features_indices = np.argsort(feature_ranking)[:9]
top_9_features = X.columns[top_9_features_indices]

selected_headers = get_headers_by_index('total_labeled_data.csv', top_9_features)

# print("Top 100 features:", selected_headers)
#
# with open('top_100_features.csv', mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     writer.writerow(['No.', 'Feature'])
#
#     # 写入每一行数据
#     count = 0
#     for row in selected_headers:
#         writer.writerow([count + 1, row])
#         count += 1

# 选取顶级特征并归一化
scaler = StandardScaler()
X_normalized_top_features = scaler.fit_transform(X[top_9_features])

# 使用PCA降维到2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_normalized_top_features)

scaler = MinMaxScaler()

# 创建子图，调整figsize参数以放大整个图形
fig, axes = plt.subplots(3, 3, figsize=(16, 12))

for i, feature in enumerate(selected_headers):
    ax = axes[i // 3, i % 3]
    feature_data = X_normalized_top_features[:, i]
    # 使用MinMaxScaler归一化特征值到0到1的范围
    scaled_data = scaler.fit_transform(feature_data.reshape(-1, 1)).flatten()

    # 设置归一化范围为0到1
    norm = Normalize(vmin=0, vmax=1)

    # 绘制散点图
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=scaled_data, cmap='rainbow', norm=norm, s=40)
    ax.set_title(f"{feature}")
    ax.set_xlim(-3, 3.1)
    ax.set_ylim(-3, 3)
    ax.set_xticks(np.arange(-3, 4, 1))
    ax.set_yticks(np.arange(-3, 4, 1))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 添加颜色条，并显式设置归一化范围
    cbar = fig.colorbar(scatter, ax=ax, orientation='vertical', pad=0.02, norm=norm)
    # cbar.set_label('Feature Scale')

plt.tight_layout(h_pad=1)
plt.savefig('fig_2.png', dpi=800)
plt.show()


# # 假设X_pca和y已经定义并准备好数据
# labels = ['SpotBugs', 'PMD', 'SonarQube']
#
# # 创建子图，3个工具对应3个子图
# fig, axes = plt.subplots(1, 3, figsize=(16, 4))
#
# scaler = MinMaxScaler()
#
# # 遍历三个工具，分别绘制对应的子图
# for i, tool in enumerate(labels):
#     ax = axes[i]
#
#     # 根据y值选择对应工具的数据
#     tool_mask = (y == i)
#
#     # 标记为有效的数据点（y值等于当前工具）
#     valid_data = X_pca[tool_mask]
#
#     # 标记为无效的数据点（y值不等于当前工具）
#     invalid_data = X_pca[~tool_mask]
#
#     # 绘制有效数据点（蓝色）
#     ax.scatter(valid_data[:, 0], valid_data[:, 1], color='red', label=f'Optimal recommendation', s=40)
#
#     # 绘制无效数据点（红色）
#     ax.scatter(invalid_data[:, 0], invalid_data[:, 1], color='blue', label=f'Non-optimal recommendation', s=40)
#
#     # 设置图形标题和范围
#     ax.set_title(f"{tool}")
#     ax.set_xlim(-3, 3.1)
#     ax.set_ylim(-3, 3)
#     ax.set_xticks(np.arange(-3, 4, 1))
#     ax.set_yticks(np.arange(-3, 4, 1))
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#
#     # 添加图例
#     ax.legend()
#
# plt.tight_layout(h_pad=1)
# plt.savefig('tools_pca.png', dpi=800)
# plt.show()