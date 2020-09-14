import random


def run(attributes: list, cluster_num: int):
    """

    :param attributes:  输入特征
    :param cluster_num: 分类的类簇数量
    :return:    list 返回筛选后剩下的测试用例的编号（返回值数量与cluster_num相同）
    """
    random_list = list(range(len(attributes)))
    random.shuffle(random_list)

    result = random_list[0:cluster_num]

    return result


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
    result = run(cluster_num=2)
    print(result)
    print("##############")
    print("### Ending ###")
