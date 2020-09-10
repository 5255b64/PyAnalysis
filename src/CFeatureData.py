# -*- coding: UTF-8 -*-
import copy
import json
import sys


class FeatureData:
    """
    保存测试集合的特征数据
    """

    def __init__(self):
        self.totalProbeNum = -1
        self.testSuite = dict()

    def load(self, feature_data_file_path: str):
        """
        构造函数 根据提供的json文件路径 加载对象
        :param feature_data_file_path: 输入json文件路径（特征数据）
        """
        self.totalProbeNum = -1  # 桩总数
        self.testSuite = dict()  # 测试用例对象字典
        with open(feature_data_file_path, "r") as json_f:
            json_obj: list = json.load(json_f)
            for testcase_dict in json_obj:
                if testcase_dict.__len__() == 1:
                    self.totalProbeNum = testcase_dict["totalProbeNum"]
                else:
                    testcase_object = TestcaseData(testcase_dict)
                    self.testSuite[testcase_object.testcaseID] = testcase_object

    def select(self, selected_num_list: list):
        """
        筛选部分的测试用例信息 并返回
        :param selected_num_list    根据此参数 从test_suite中选取部分测试用例
        :return:
        """
        result = FeatureData()
        result.totalProbeNum = self.totalProbeNum
        result.testSuite = dict()
        for selected_num in selected_num_list:
            if selected_num in self.testSuite.keys():
                result.testSuite[selected_num] = self.testSuite[selected_num]
            else:
                print("测试用例编号不存在：" + str(selected_num), file=sys.stderr)
        return result

    def get_feature_matrix(self):
        """
        获取矩阵（二维数组）式的特征
        :return:
        feature_lists   特征矩阵
        key_list        矩阵中每一行对应的测试用例编号
        """
        feature_lists = list()
        key_list = list()
        for testcase_key in self.testSuite:
            key_list.append(testcase_key)
            feature_lists.append(self.testSuite[testcase_key].feature)
        return feature_lists, key_list

    def print(self):
        print("totalProbeNum=" + str(self.totalProbeNum))
        print("testSuite=" + str(self.testSuite))


class TestcaseData:
    """
    保存单挑测试用例的数据
    """

    def __init__(self, testcase: dict):
        # absoluteProbeNum 整数 触发的桩数量（不重复）
        self.absoluteProbeNum = testcase["absoluteProbeNum"]
        # feature 数组 组合覆盖特征 0-1值
        self.feature = testcase["feature"]
        # probeInfos 字典 key为桩标识 value为该桩被触发的次数
        self.probeInfos = testcase["probeInfos"]
        # probeNum 整数 触发的桩数量（有重复）
        self.probeNum = testcase["probeNum"]
        # testcaseCode 字符串 测试用例的字段以及值
        self.testcaseCode = testcase["testcaseCode"]
        # testcaseID 整数 测试用例的ID
        self.testcaseID = testcase["testcaseID"]


if __name__ == "__main__":
    """
    测试
    """
    feature_data_file_path = "..\\resource\\cstp_feature.json"
    print(feature_data_file_path)
    fd = FeatureData()
    fd.load(feature_data_file_path=feature_data_file_path)
    # fd.print()

    fd2 = fd.select([1, 2, 3])
    fd2.print()
    feature_lists, key_list = fd2.get_feature_matrix()
    print(feature_lists)
    print(key_list)
