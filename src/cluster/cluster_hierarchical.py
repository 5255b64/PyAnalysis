from sklearn.cluster import AgglomerativeClustering
import numpy as np

from src.cluster import pca

"""
凝聚层次聚类削减算法
1.聚类方法：凝聚层次聚类
2.削减方法：取距离类簇最近的样本进行采样
"""
def run(attributes: list, cluster_num: int):
    """

    :param attributes:  输入特征
    :param cluster_num: 分类的类簇数量
    :return:    list 返回筛选后剩下的测试用例的编号（返回值数量与cluster_num相同）
    """
    X = np.array(attributes)
    n_clusters = cluster_num

    clustering = AgglomerativeClustering(linkage='ward', n_clusters=n_clusters)
    clustering.fit(X)

    # print(clustering.labels_)
    # 数据整合 将数据分至各个类簇
    labels = clustering.labels_.tolist()
    data = []
    sum_value = []
    means = []
    for i in range(n_clusters):
        data.append([])
        sum_value.append(np.zeros(X[0].shape))
        means.append([])
    for X_num in range(len(X)):
        data[labels[X_num]].append(X_num)
        sum_value[labels[X_num]] = np.add(sum_value[labels[X_num]], X[X_num])
    # print(data)
    # 求均值 计算类簇的中心点
    for i in range(len(sum_value)):
        means[i] = np.divide(sum_value[i], np.array(len(data[i]))).tolist()
    # print(means)
    # 削减：筛选出距离类簇中心最近的样本
    X_selected = []
    for cls_num in range(n_clusters):
        selected_num = -1
        selected_sum_square = -1
        center_value = means[cls_num]
        for num in range(len(data[cls_num])):
            # 计算平方和
            X_num = data[cls_num][num]
            X_value = X[X_num]
            sub = np.subtract(X_value, np.array(center_value)).tolist()
            sub_sum_square = sum([x * x for x in sub])
            if selected_sum_square < 0 or sub_sum_square > selected_sum_square:
                selected_sum_square = sub_sum_square
                selected_num = X_num
        X_selected.append(selected_num)
    # print(X_selected)
    return X_selected


if __name__ == "__main__":
    X = [
        [0, 0],
        [0, 1],
        [1, 0],
        [-1, 0],
        [0, -1],

        [2, 2],
        [2, 3],
        [3, 2],
        [1, 2],
        [2, 1]
    ]
    result = run(attributes=X, cluster_num=2)
    print(result)
    print("##############")
    print("### Ending ###")
