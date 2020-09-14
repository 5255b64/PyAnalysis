from src.CFeatureData import FeatureData
from src.CIndicatorCollector import IndicatorCollector
from src.cluster import cluster_hierarchical

if __name__ == "__main__":
    # 加载特征数据
    feature_data_file_path = "..\\..\\resource\\feature_FxclDealLogParser_1000.json"
    fd = FeatureData()
    fd.load(feature_data_file_path=feature_data_file_path)

    # 统计数据
    ic1 = IndicatorCollector(fd)
    # print("ic1")
    # ic1.print()

    # 绘图
    ic1.plot_case_cover_probe_num_list()

    # for i in list(range(960, 10, -50)):
    # for i in [500, 250, 100, 50, 10]:
    for i in [500, 250, 100, 50, 10, 8, 6, 4, 2]:
        # 聚类削减
        feature_lists, key_list = fd.get_blackbox_feature_matrix()
        result = cluster_hierarchical.run(feature_lists, i)
        # print(result)

        # 构建削减后的测试集
        selected_tc_list = list()
        for x in result:
            selected_tc_list.append(key_list[x])
        # print(selected_tc_list)
        fd2 = fd.select(selected_tc_list)

        # 统计数据
        ic2 = IndicatorCollector(fd2)
        # print("ic2")
        ic2.print()

        ic2.plot_case_cover_probe_num_list()
