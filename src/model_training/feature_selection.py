import csv

import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC

from src.model_training.model_training import SVM

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

# 打印编码后的标签
# print(encoded_labels)

# 加载数据
X = np.array(X_list)  # 特征数据，形状为(419, 302)
y = np.array(encoded_labels)  # 标签数据，形状为(400,)，包含5个不同类别

print(X.shape)
print(y.shape)

# 划分数据集
X_train_old, X_test_old, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 数据预处理
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train_old)
X_test = scaler.transform(X_test_old)

# 使用SMOTE进行过采样
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# 初始化模型
model = SVC()


def backward_elimination(X_train, y_train, X_test, y_test, model):
    features = list(range(X_train.shape[1]))
    best_r2 = -np.inf
    best_features = features.copy()

    while len(features) > 0:
        r2_scores = []

        for feature in features:
            remaining_features = [f for f in features if f != feature]

            model.fit(X_train[:, remaining_features], y_train)
            y_pred = model.predict(X_test[:, remaining_features])
            r2 = r2_score(y_test, y_pred)
            r2_scores.append(r2)

        max_r2 = max(r2_scores)
        worst_feature = features[np.argmax(r2_scores)]

        if max_r2 >= best_r2:
            best_r2 = max_r2
            features.remove(worst_feature)
            best_features = features.copy()
        else:
            break

    return best_features, best_r2


# 使用greedy backward elimination algorithm进行特征选择
selected_features, best_r2 = backward_elimination(X_train_resampled, y_train_resampled, X_test, y_test, model)
print(f"Selected features: {selected_features}")
print(f"Best R-squared: {best_r2}")
