from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt


def KMeans_method(X, n):
    # 创建KMeans聚类模型，设定聚类数量为n_clusters
    n_clusters = n
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)

    # 用数据来训练模型
    kmeans.fit(X)

    # 查看每个样本所属的聚类标签
    labels = kmeans.labels_
    print(labels)
    return labels


def DBSCAN_method(X):
    # 创建DBSCAN模型，设置邻域半径为eps，至少包含min_samples个点的区域被认为是密集区域
    eps = 0.3
    min_samples = 6
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)

    # 用数据来训练模型
    dbscan.fit(X)

    # 查看每个样本所属的聚类标签，噪音点的标签为-1
    labels = dbscan.labels_
    print(labels)

    # 聚类的数量（忽略噪声点，所以需要减1）
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    # 噪声点的百分比
    noise_ratio = np.sum(labels == -1) / len(labels)

    # 各个聚类的数量
    cluster_counts = np.bincount(labels[labels >= 0])  # 只对非噪声点计数

    print(f"Number of clusters: {n_clusters}")
    print(f"Noise ratio: {noise_ratio}")
    print(f"Cluster counts: {cluster_counts}")

    return labels


def K_distance_method(X, n):
    nbrs = NearestNeighbors(n_neighbors=n).fit(X)
    distances, indices = nbrs.kneighbors(X)

    distances = np.sort(distances, axis=0)
    distances = distances[:, 1]
    plt.plot(distances)
    plt.show()