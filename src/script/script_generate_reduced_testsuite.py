# -*- coding:utf-8 -*-
"""
对原测试用例集合进行削减
将削减后的测试用例（json格式）保存至指定文件夹
"""
import json
import os

from src.CFeatureData import FeatureData
from src.CIndicatorCollector import IndicatorCollector
from src.CONFIG import REDUCED_NUM_LIST
from src.cluster import reducer_ge, cluster_hierarchical


def run(input_file_addr: str, output_file_path: str, reduced_num_list: list, cluster_function):
    # 对列表reduced_num_list进行排序
    reduced_num_list.sort()
    # 日志信息提取
    fd = FeatureData()
    fd.load(feature_data_file_path=input_file_addr)
    feature_lists, key_list = fd.get_blackbox_feature_matrix()  # 黑盒特征
    # feature_lists, key_list = fd.get_blackbox_feature_matrix()  # 白盒特征
    ic = IndicatorCollector(fd)  # 统计数据
    pca_n_components = ic.total_probe_num

    # 必要变量初始化
    testsuite_selected = []
    tc_coverage_list = []
    coverage_list = [0] * len(feature_lists[0])

    for cluster_num in reduced_num_list:
        # 每个testsuite放置不同的根目录下
        output_file_root_path = os.path.join(output_file_path, str(cluster_num))
        # 创建根目录
        if not os.path.exists(output_file_root_path):
            os.makedirs(output_file_root_path)
        # 凝聚层次聚类削减
        if cluster_function is not None:
            testsuite_selected = cluster_function.run(feature_lists, cluster_num)
        else:
            testsuite_selected = list(range(cluster_num))
        # GE削减
        # [testsuite_selected, coverage_list, tc_coverage_list] = cluster_function.run(
        #     feature_lists, cluster_num,
        #     X_selected=testsuite_selected,
        #     coverage_list=coverage_list,
        #     tc_coverage_list=tc_coverage_list
        # )
        # 获取json格式的测试用例
        selected_fd = fd.select(testsuite_selected)
        for tc_key in selected_fd.testSuite:
            output_file_addr = os.path.join(output_file_root_path, "test" + str(tc_key) + ".json")
            with open(output_file_addr, 'w', encoding='utf-8') as f_out:
                testcase_str = selected_fd.testSuite[tc_key].testcaseCode
                print(testcase_str, file=f_out)


if __name__ == "__main__":
    # 采用何种聚类削减方法
    # cluster_function = reducer_ge
    # cluster_function = cluster_random
    cluster_function = cluster_hierarchical

    reduced_num_list = REDUCED_NUM_LIST

    # input_file_addr = "..\\..\\resource\\feature_bcbip_type1_1000.json"
    # output_file_path = "..\\..\\resource\\reduced_testsuite\\bcbip\\type1_1000"
    # run(input_file_addr=input_file_addr, output_file_path=output_file_path, reduced_num_list=reduced_num_list,
    #     cluster_function=cluster_function)
    input_file_addr = "..\\..\\resource\\feature_bcbip_type3_1000.json"
    output_file_path = "..\\..\\resource\\reduced_testsuite\\bcbip\\type3_1000"
    run(input_file_addr=input_file_addr, output_file_path=output_file_path, reduced_num_list=[1000],
        cluster_function=None)

    # input_file_addr = "..\\..\\resource\\feature_bcbip_type2_1000.json"
    # output_file_path = "..\\..\\resource\\reduced_testsuite\\bcbip\\type2_1000"
    # run(input_file_addr=input_file_addr, output_file_path=output_file_path, reduced_num_list=reduced_num_list,
    #     cluster_function=cluster_function)
    #
    # input_file_addr = "..\\..\\resource\\feature_bcbip_type3_1000.json"
    # output_file_path = "..\\..\\resource\\reduced_testsuite\\bcbip\\type3_1000"
    # run(input_file_addr=input_file_addr, output_file_path=output_file_path, reduced_num_list=reduced_num_list,
    #     cluster_function=cluster_function)
