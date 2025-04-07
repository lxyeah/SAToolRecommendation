import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import csv
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from imblearn.over_sampling import SMOTE
import src.configure as c


def logisticRegression(X_train, y_train, X_test, y_test):
    print('------------------Logistic Regression--------------------')
    # 创建逻辑回归模型
    classifier = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=42)

    # 训练模型
    classifier.fit(X_train, y_train)

    # 在测试集上评估模型
    # y_pred = classifier.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: {:.2f}%".format(accuracy * 100))
    #
    # # 分类报告
    # report = classification_report(y_test, y_pred, zero_division=0)
    # print("Classification Report:\n", report)

    # 交叉验证
    cross_val_precision_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision_weighted')
    cross_val_accuracy_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='balanced_accuracy')
    cross_val_f1_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='f1_weighted')
    cross_val_auc_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='roc_auc_ovr')
    print("Cross Validation PRECISION_WEIGHTED Scores: ", cross_val_precision_scores)
    print("Average Cross Validation PRECISION_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_precision_scores) * 100))
    print("Cross Validation BALANCED_ACCURACY Scores: ", cross_val_accuracy_scores)
    print("Average Cross Validation BALANCED_ACCURACY Score: {:.2f}%".format(np.mean(cross_val_accuracy_scores) * 100))
    print("Cross Validation F1_WEIGHTED Scores: ", cross_val_f1_scores)
    print("Average Cross Validation F1_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_f1_scores) * 100))
    print("Cross Validation ROC_AUC Scores: ", cross_val_auc_scores)
    print("Average Cross Validation ROC_AUC Score: {:.2f}%".format(np.mean(cross_val_auc_scores) * 100))


def SVM(X_train, y_train, X_test, y_test):
    print('------------------SVM--------------------')
    # 创建SVM分类器实例
    svm = SVC(probability=True)

    # 设置网格搜索的参数范围
    # param_grid = {'C': [0.1, 1, 10, 100], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto', 0.1, 1, 10]}

    # 使用网格搜索和交叉验证寻找最优参数
    # grid_search = GridSearchCV(svm, param_grid, scoring='f1_weighted', cv=5)
    # grid_search.fit(X_train_resampled, y_train_resampled)

    # 获取最佳参数组合
    # best_params = grid_search.best_params_
    # print("Best Parameters: ", best_params)

    # 使用最佳参数训练SVM模型
    # best_svm = SVC(**best_params, probability=True)
    # svm.fit(X_train_resampled, y_train_resampled)
    # 使用RFE进行特征选择
    # rfe = RFE(estimator=svm, n_features_to_select=220, step=10)
    # rfe.fit(X_train_resampled, y_train_resampled)

    # 将特征选择应用到训练和测试集
    # X_train_selected = rfe.transform(X_train_resampled)
    # X_test_selected = rfe.transform(X_test)

    # 使用选择的特征训练SVM模型
    svm.fit(X_train_resampled, y_train_resampled)

    # 在测试集上评估模型
    # y_pred = best_svm.predict(X_test_selected)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: {:.2f}%".format(accuracy * 100))
    #
    # # 分类报告
    # report = classification_report(y_test, y_pred, zero_division=0)
    # print("Classification Report:\n", report)

    # 交叉验证
    cross_val_precision_scores = cross_val_score(svm, X_train, y_train, cv=5, scoring='precision_weighted')
    cross_val_accuracy_scores = cross_val_score(svm, X_train, y_train, cv=5, scoring='balanced_accuracy')
    cross_val_f1_scores = cross_val_score(svm, X_train, y_train, cv=5, scoring='f1_weighted')
    cross_val_auc_scores = cross_val_score(svm, X_train, y_train, cv=5, scoring='roc_auc_ovr')
    print("Cross Validation PRECISION_WEIGHTED Scores: ", cross_val_precision_scores)
    print("Average Cross Validation PRECISION_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_precision_scores) * 100))
    print("Cross Validation BALANCED_ACCURACY Scores: ", cross_val_accuracy_scores)
    print("Average Cross Validation BALANCED_ACCURACY Score: {:.2f}%".format(np.mean(cross_val_accuracy_scores) * 100))
    print("Cross Validation F1_WEIGHTED Scores: ", cross_val_f1_scores)
    print("Average Cross Validation F1_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_f1_scores) * 100))
    print("Cross Validation ROC_AUC Scores: ", cross_val_auc_scores)
    print("Average Cross Validation ROC_AUC Score: {:.2f}%".format(np.mean(cross_val_auc_scores) * 100))


def decisionTree(X_train, y_train, X_test, y_test):
    print('------------------Decision Tree--------------------')
    # 创建决策树分类器
    classifier = DecisionTreeClassifier(random_state=42)



    # 训练模型
    classifier.fit(X_train, y_train)

    # 在测试集上评估模型
    # y_pred = classifier.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: {:.2f}%".format(accuracy * 100))
    #
    # # 分类报告
    # report = classification_report(y_test, y_pred, zero_division=0)
    # print("Classification Report:\n", report)

    # 交叉验证
    cross_val_precision_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision_weighted')
    cross_val_accuracy_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='balanced_accuracy')
    cross_val_f1_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='f1_weighted')
    cross_val_auc_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='roc_auc_ovr')
    print("Cross Validation PRECISION_WEIGHTED Scores: ", cross_val_precision_scores)
    print("Average Cross Validation PRECISION_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_precision_scores) * 100))
    print("Cross Validation BALANCED_ACCURACY Scores: ", cross_val_accuracy_scores)
    print("Average Cross Validation BALANCED_ACCURACY Score: {:.2f}%".format(np.mean(cross_val_accuracy_scores) * 100))
    print("Cross Validation F1_WEIGHTED Scores: ", cross_val_f1_scores)
    print("Average Cross Validation F1_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_f1_scores) * 100))
    print("Cross Validation ROC_AUC Scores: ", cross_val_auc_scores)
    print("Average Cross Validation ROC_AUC Score: {:.2f}%".format(np.mean(cross_val_auc_scores) * 100))


def randomForest(X_train, y_train, X_test, y_test):
    print('------------------Random Forest--------------------')


    # 创建随机森林分类器
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)

    # # 使用RFE进行特征选择
    # rfe = RFE(estimator=classifier, n_features_to_select=220, step=10)
    # rfe.fit(X_train_resampled, y_train_resampled)
    #
    # # 将特征选择应用到训练和测试集
    # X_train_selected = rfe.transform(X_train_resampled)
    # X_test_selected = rfe.transform(X_test)

    # 训练模型
    classifier.fit(X_train_resampled, y_train_resampled)

    # 获取特征重要性
    importances = classifier.feature_importances_

    # 输出每个特征的重要性
    for i in range(X_train.shape[1]):
        print(f"The importance of {i} is: {importances[i]}")


    # 在测试集上评估模型
    # y_pred = classifier.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: {:.2f}%".format(accuracy * 100))
    #
    # # 分类报告
    # report = classification_report(y_test, y_pred, zero_division=0)
    # print("Classification Report:\n", report)

    # 交叉验证
    cross_val_precision_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision_weighted')
    cross_val_accuracy_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='balanced_accuracy')
    cross_val_f1_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='f1_weighted')
    cross_val_auc_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='roc_auc_ovr')
    print("Cross Validation PRECISION_WEIGHTED Scores: ", cross_val_precision_scores)
    print("Average Cross Validation PRECISION_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_precision_scores) * 100))
    print("Cross Validation BALANCED_ACCURACY Scores: ", cross_val_accuracy_scores)
    print("Average Cross Validation BALANCED_ACCURACY Score: {:.2f}%".format(np.mean(cross_val_accuracy_scores) * 100))
    print("Cross Validation F1_WEIGHTED Scores: ", cross_val_f1_scores)
    print("Average Cross Validation F1_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_f1_scores) * 100))
    print("Cross Validation ROC_AUC Scores: ", cross_val_auc_scores)
    print("Average Cross Validation ROC_AUC Score: {:.2f}%".format(np.mean(cross_val_auc_scores) * 100))


def knn(X_train, y_train, X_test, y_test):
    print('------------------KNN--------------------')
    # 创建 KNN 分类器
    k = 4  # 可以尝试其他的 k 值
    classifier = KNeighborsClassifier(n_neighbors=k)

    # 训练模型
    classifier.fit(X_train, y_train)

    # 在测试集上评估模型
    # y_pred = classifier.predict(X_test)
    # accuracy = accuracy_score(y_test, y_pred)
    # print("Accuracy: {:.2f}%".format(accuracy * 100))
    #
    # # 分类报告
    # report = classification_report(y_test, y_pred, zero_division=0)
    # print("Classification Report:\n", report)

    # 交叉验证
    cross_val_precision_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='precision_weighted')
    cross_val_accuracy_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='balanced_accuracy')
    cross_val_f1_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='f1_weighted')
    cross_val_auc_scores = cross_val_score(classifier, X_train, y_train, cv=5, scoring='roc_auc_ovr')
    print("Cross Validation PRECISION_WEIGHTED Scores: ", cross_val_precision_scores)
    print("Average Cross Validation PRECISION_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_precision_scores) * 100))
    print("Cross Validation BALANCED_ACCURACY Scores: ", cross_val_accuracy_scores)
    print("Average Cross Validation BALANCED_ACCURACY Score: {:.2f}%".format(np.mean(cross_val_accuracy_scores) * 100))
    print("Cross Validation F1_WEIGHTED Scores: ", cross_val_f1_scores)
    print("Average Cross Validation F1_WEIGHTED Score: {:.2f}%".format(np.mean(cross_val_f1_scores) * 100))
    print("Cross Validation ROC_AUC Scores: ", cross_val_auc_scores)
    print("Average Cross Validation ROC_AUC Score: {:.2f}%".format(np.mean(cross_val_auc_scores) * 100))


if __name__ == '__main__':
    X_list = []
    y_list = []
    with open('total_labeled_data_1.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            # print(len(i))
            # features = i[0:40] + i[80:125] + i[170:209] + i[248:275]
            features = i[40:80] + i[125:170] + i[209:248] + i[275: -3]
            # selected_list = []
            # for j in c.selected_features:
            #     selected_list.append(features[j])
            # 40 45 39 27
            X_list.append(features)
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



    logisticRegression(X_train_resampled, y_train_resampled, X_test, y_test)
    SVM(X_train_resampled, y_train_resampled, X_test, y_test)
    decisionTree(X_train_old, y_train, X_test_old, y_test)
    randomForest(X_train_resampled, y_train_resampled, X_test, y_test)
    knn(X_train_resampled, y_train_resampled, X_test, y_test)

