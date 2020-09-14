from sklearn.cluster import AgglomerativeClustering
import numpy as np

"""
凝聚层次聚类削减算法ver2
在前者基础之上：
1.加入PCA降维
2.修改削减方法为：取类簇中覆盖范围最大的样本进行采样（没有太大的效果）
"""


def run(attributes: list, cluster_num: int):
    """

    :param attributes_pca:  输入特征（原始） one-hot 编码
    :param cluster_num: 分类的类簇数量
    :return:    list 返回筛选后剩下的测试用例的编号（返回值数量与cluster_num相同）
    """
    # TODO 引入PCA降维方法 对attributes进行降维
    attributes_pca = attributes  # TODO 修改
    #

    X = np.array(attributes_pca)
    n_clusters = cluster_num

    clustering = AgglomerativeClustering(linkage='ward', n_clusters=n_clusters)
    clustering.fit(X)

    # print(clustering.labels_)
    # 数据整合 将数据分至各个类簇
    labels = clustering.labels_.tolist()  # 聚类后每个样本被分至的类簇编号
    list_cluster_max_sample = list()  # 保存“类簇编号-类簇内覆盖范围最大的样本编号“的映射数组
    sample_coverage = list()  # 保存每个样本的覆盖范围
    data = []

    for i in range(n_clusters):
        data.append([])
        list_cluster_max_sample.append(-1)
    for X_num in range(len(X)):
        sample_coverage.append(sum(attributes[X_num]))
        data[labels[X_num]].append(X_num)
    # print(data)
    # print(means)
    # 削减：取类簇中覆盖范围最大的样本进行采样
    X_selected = []  # 被选中的样本
    for X_num in range(len(X)):
        label = labels[X_num]
        coverage = sample_coverage[X_num]
        if list_cluster_max_sample[label] < 0 or coverage > sample_coverage[list_cluster_max_sample[label]]:
            list_cluster_max_sample[label] = X_num
    for selected_sample in list_cluster_max_sample:
        X_selected.append(selected_sample)
    # print(X_selected)
    return X_selected


if __name__ == "__main__":
    # X = [
    #     [0, 0],
    #     [0, 1],
    #     [1, 0],
    #     [-1, 0],
    #     [0, -1],
    #
    #     [2, 2],
    #     [2, 3],
    #     [3, 2],
    #     [1, 2],
    #     [2, 1]
    # ]
    X = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [2, 0, 0, 0],
        [0, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 2],
    ]
    result = run(attributes=X, cluster_num=2)
    print(result)
    print("##############")
    print("### Ending ###")
