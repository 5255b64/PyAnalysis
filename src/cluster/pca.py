import numpy as np
from sklearn.decomposition import PCA

"""
PCA算法
"""
def run(attributes: list, n_components: int, ratio_threshold: float=0.95):
    """

    :param attributes:          被降维的特征矩阵
    :param n_components:        降维后 每一行特征向量的维度（n_components不能超过attributes的原始维度）
    :param ratio_threshold:     降维后 根据各成分分量的占比进行筛选 保留最主要的分量 直到所有选取分量之和大于ratio_threshold
                                    ratio_threshold=1表示保留所有分量
    :return:
    """
    X = np.array(attributes)

    pca = PCA(n_components=n_components)
    attribute = pca.fit(X).transform(X).tolist()
    ratio_all = pca.explained_variance_ratio_.tolist()  # 所有属性的占比
    ratio = list()  # 只考虑占比总和超过ratio_threshold的一部分（最大重要的）属性
    result = list()
    r_sum = 0
    for r in ratio_all:
        ratio.append(r)
        r_sum = r_sum+r
        if r_sum >ratio_threshold:
            break
    for sample_num in range(len(attribute)):
        new_sample_vertor = list()
        for attribute_num in range(len(ratio)):
            # new_sample_vertor.append(attribute[sample_num][attribute_num] * ratio[attribute_num])
            new_sample_vertor.append(attribute[sample_num][attribute_num])
        result.append(new_sample_vertor)

    # print(str(pca.explained_variance_ratio_))
    # print(str(sum(pca.explained_variance_ratio_)))
    # pca.explained_variance_ratio_ 主成分方差 值越大代表占比越高

    return result


if __name__ == "__main__":
    attributes = [[1, 1, 2, 2], [1, 1, 2, 2], [-1, -1, -2, -2]]
    n_components = 3
    result = run(attributes=attributes, n_components=n_components)
    print(result)
