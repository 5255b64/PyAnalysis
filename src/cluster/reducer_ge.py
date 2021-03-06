"""
使用ge算法进行测试用例削减
ge算法是一种贪心算法，具体如下：
1.在所有测试用例中，挑选覆盖率最高的；
2.对剩下的测试用例，以对“未覆盖代码”的覆盖比例，重新计算覆盖率；
3.在剩下的测试用例中，挑选覆盖率最高的；
4.重复2-3过程，直到满足一定的覆盖率要求，或者是测试用例数量要求；
"""


def run(attributes: list, cluster_num: int, X_selected: list = [], coverage_list: list = [], tc_coverage_list:list = []):
    """
    使用GE算法 根据数量要求进行测试用例削减
    :param attributes:  测试用例特征
    :param cluster_num: 数量要求
    :param X_selected 默认的返回值 存储之前已经计算好的结果
    :param coverage_list 覆盖率情况 存储之前已经计算好的结果
    :param tc_coverage_list 测试用例的覆盖率情况 存储之前已经计算好的结果
    :return: list 返回筛选后剩下的测试用例的编号（返回值数量与cluster_num相同）
    """
    # 特征向量长度
    attribute_length = len(attributes[0])

    counter = 0

    # 计算每条测试用例的覆盖率
    if len(tc_coverage_list) is not len(attributes):
        tc_coverage_list = []
        for tc_num in range(len(attributes)):
            tc_coverage = 0
            for attr_num in range(attribute_length):
                counter = counter + 1
                attr_value = attributes[tc_num][attr_num]
                if coverage_list[attr_num] is 0 and attr_value > 0:
                    tc_coverage = tc_coverage + 1
            tc_coverage_list.append(tc_coverage)

    # 筛选测试用例 挑选的数量为cluster_num
    for num in range(cluster_num):
        if num < len(X_selected):
            continue
        # 从剩余测试用例做中取最大值
        tc_coverage_max = -1
        tc_selected_num = -1
        for tc_num in range(len(tc_coverage_list)):
            if tc_num not in X_selected:
                # 计算覆盖率
                tc_coverage = tc_coverage_list[tc_num]
                if tc_coverage > tc_coverage_max:
                    tc_coverage_max = tc_coverage
                    tc_selected_num = tc_num
        # 挑选出一个新的测试用例
        X_selected.append(tc_selected_num)
        # 重新计算覆盖率
        tc_selected = attributes[tc_selected_num]
        for attr_num in range(attribute_length):
            if tc_selected[attr_num] > 0:
                coverage_list[attr_num] = 1
                for tc_num in range(len(attributes)):
                    counter = counter + 1
                    if tc_num not in X_selected and attributes[tc_num][attr_num] is 1:
                        tc_coverage_list[tc_num] = tc_coverage_list[tc_num] - 1
    # print("counter=" + str(counter))
    return [X_selected, coverage_list, tc_coverage_list]


if __name__ == "__main__":
    X = [
        [0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1],
    ]
    X_selected = []
    tc_coverage_list = []
    coverage_list = [0] * len(X[0])
    for i in range(5):
        [X_selected, coverage_list, tc_coverage_list] = run(attributes=X, cluster_num=i, X_selected=X_selected,
                                          coverage_list=coverage_list, tc_coverage_list=tc_coverage_list)

        print(X_selected)
    print(coverage_list)
    print("##############")
    print("### Ending ###")
