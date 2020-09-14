# -*- coding: UTF-8 -*-
import numpy as np
from sklearn.cluster import KMeans
from sklearn import metrics


def main():
    expected_cluster = [1, 0, 1, 0]
    result = run(attributes=[
        [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1,
         1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
         0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1]],
        expected_cluster=expected_cluster,
        cluster_num=2)
    print(result)
    print(evaluate(result, expected_cluster))


def run(attributes: list, expected_cluster: list, cluster_num: int):
    random_state = 170
    x = np.array(attributes)
    y = np.array(expected_cluster)

    # Incorrect number of clusters
    y_pred = KMeans(n_clusters=cluster_num, random_state=random_state).fit_predict(x)

    return y_pred.tolist()


def evaluate(predicted, expected):
    print("评价指标:")
    print("1.兰德指数ARI [-1,1] 越大越好")
    metric1 = metrics.adjusted_rand_score(expected, predicted)
    print(metric1)
    print("2.同质性homogeneity [0,1] 越大越好")
    metric2 = metrics.homogeneity_score(expected, predicted)
    print(metric2)
    print("3.完整性completeness [0,1] 越大越好")
    metric3 = metrics.completeness_score(expected, predicted)
    print(metric3)
    print("4.调和平均V-measure [0,1] 越大越好")
    metric4 = metrics.v_measure_score(expected, predicted)
    print(metric4)
    return [metric1, metric2, metric3, metric4]


if __name__ == '__main__':
    main()
