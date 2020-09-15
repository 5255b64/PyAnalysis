"""
使用ge算法进行测试用例削减
ge算法是一种贪心算法，具体如下：
1.在所有测试用例中，挑选覆盖率最高的；
2.对剩下的测试用例，以对“未覆盖代码”的覆盖比例，重新计算覆盖率；
3.在剩下的测试用例中，挑选覆盖率最高的；
4.重复2-3过程，直到满足一定的覆盖率要求，或者是测试用例数量要求；
"""


def run(attributes: list, cluster_num: int):
    """
    使用GE算法 根据数量要求进行测试用例削减
    :param attributes:  测试用例特征
    :param cluster_num: 数量要求
    :return: list 返回筛选后剩下的测试用例的编号（返回值数量与cluster_num相同）
    """
    # 返回值 挑选的测试用例list
    X_selected = list()
    # 特征向量长度
    attribute_length = len(attributes[0])
    # 已挑选测试用例的覆盖情况
    coverage_list = [0] * attribute_length
    # 筛选测试用例 挑选的数量为cluster_num
    for num in range(cluster_num):
        # 对剩余测试用例做遍历
        tc_coverage_max = -1
        tc_selected = -1
        for tc_num in range(len(attributes)):
            if tc_num not in X_selected:
                # 计算覆盖率
                tc_coverage = 0
                for attr_num in range(attribute_length):
                    attr_value = attributes[tc_num][attr_num]
                    if coverage_list[attr_num] is 0 and attr_value > 0:
                        tc_coverage = tc_coverage + 1
                if tc_coverage > tc_coverage_max:
                    tc_coverage_max = tc_coverage
                    tc_selected = tc_num
        # 挑选出一个新的测试用例
        X_selected.append(tc_selected)
        # 重新计算覆盖率
        for attr_num in range(attribute_length):
            if attributes[tc_selected][attr_num] > 0:
                coverage_list[attr_num] = 1

    return X_selected


if __name__ == "__main__":
    X = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    result = run(attributes=X, cluster_num=3)
    print(result)
    print("##############")
    print("### Ending ###")