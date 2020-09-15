"""
“凝聚层次”聚类削减方法 与
“随机采样”削减方法的比较
"""
import csv

from src.CFeatureData import FeatureData
from src.CIndicatorCollector import IndicatorCollector
from src.CONFIG import CLUSTER_NUM_SAMPLE_LIST, RANDOM_TIMES, F_MEASURE_BETA
from src.cluster import cluster_hierarchical, cluster_random, cluster_hierarchical_ver2, cluster_hierarchical_pca, \
    reducer_ge
import matplotlib.pyplot as plt


def run(input_file_addr: str, output_file_addr: str, cluster_sample_list: list = CLUSTER_NUM_SAMPLE_LIST,
        random_times: int = RANDOM_TIMES, f_measure_beta: float = F_MEASURE_BETA, is_draw_plot: bool = False):
    """

    :param input_file_addr:     输出的特征文件
    :param output_file_addr:    对比结果的输出文件
    :param cluster_sample_list: 聚类数量的采样列表
    :param random_times:        随机方法进行多次求平均时的重复次数
    :param is_draw_plot:        是否对结果进行绘图
    :return:
    """
    # 关键数据
    result_hierarchical_f_score = list()
    result_hierarchical_redundancy_score = list()
    result_hierarchical_coverage_score = list()
    result_random_f_score = list()
    result_random_redundancy_score = list()
    result_random_coverage_score = list()

    fd = FeatureData()
    fd.load(feature_data_file_path=input_file_addr)
    feature_lists, key_list = fd.get_blackbox_feature_matrix()  # 黑盒特征
    # feature_lists, key_list = fd.get_blackbox_feature_matrix()  # 白盒特征
    ic = IndicatorCollector(fd)  # 统计数据
    pca_n_components = ic.total_probe_num

    # 采用何种聚类削减方法
    cluster_function = reducer_ge
    # cluster_function = cluster_random
    # cluster_function = cluster_hierarchical
    # cluster_function = cluster_hierarchical_pca
    # cluster_function = cluster_hierarchical_ver2

    reduced_testsuite = []
    coverage_list = [0] * len(feature_lists[0])

    for cluster_num in cluster_sample_list:
        print("cluster_num=" + str(cluster_num))
        # 凝聚层次聚类削减方法
        # reduced_testsuite = cluster_function.run(feature_lists, cluster_num, pca_n_components=pca_n_components)
        [reduced_testsuite, coverage_list] = cluster_function.run(feature_lists, cluster_num,
                                                                  X_selected=reduced_testsuite,
                                                                  coverage_list=coverage_list)
        print("reduced_testsuite:", end="")
        print(reduced_testsuite)
        # 构建削减后的测试集
        selected_tc_list = list()
        for selected_tc_num in reduced_testsuite:
            selected_tc_list.append(key_list[selected_tc_num])
        fd2 = fd.select(selected_tc_list)
        ic2 = IndicatorCollector(fd2)  # 统计数据

        [f_score, redundancy_score, coverage_score] = ic2.cal_calculate_index(beta=f_measure_beta)
        result_hierarchical_f_score.append(f_score)
        result_hierarchical_redundancy_score.append(redundancy_score)
        result_hierarchical_coverage_score.append(coverage_score)

        # 随机采样削减方法
        result_random_f_score.append(0)
        result_random_redundancy_score.append(0)
        result_random_coverage_score.append(0)
        list_ptr = len(result_random_f_score) - 1
        for random_sample in range(random_times):
            # 凝聚层次聚类削减方法
            reduced_testsuite = cluster_random.run(feature_lists, cluster_num)
            # 构建削减后的测试集
            selected_tc_list = list()
            for selected_tc_num in reduced_testsuite:
                selected_tc_list.append(key_list[selected_tc_num])
            fd2 = fd.select(selected_tc_list)
            ic2 = IndicatorCollector(fd2)  # 统计数据

            # 数据累加
            [f_score, redundancy_score, coverage_score] = ic2.cal_calculate_index(beta=f_measure_beta)
            result_random_f_score[list_ptr] = result_random_f_score[list_ptr] + f_score
            result_random_redundancy_score[list_ptr] = result_random_redundancy_score[list_ptr] + redundancy_score
            result_random_coverage_score[list_ptr] = result_random_coverage_score[list_ptr] + coverage_score
        # 数据求均值
        result_random_f_score[list_ptr] = result_random_f_score[list_ptr] / random_times
        result_random_redundancy_score[list_ptr] = result_random_redundancy_score[list_ptr] / random_times
        result_random_coverage_score[list_ptr] = result_random_coverage_score[list_ptr] / random_times

    # 绘制图表
    if is_draw_plot:
        x = cluster_sample_list
        plt.axis([cluster_sample_list[0], cluster_sample_list[-1], 0, 1])

        plt.plot(x, result_hierarchical_f_score)
        plt.plot(x, result_hierarchical_redundancy_score)
        plt.plot(x, result_hierarchical_coverage_score)
        plt.legend(labels=['f_score', 'redundancy_score', 'coverage_score'])
        plt.title("reduced")
        plt.show()

        plt.axis([cluster_sample_list[0], cluster_sample_list[-1], 0, 1])
        plt.plot(x, result_random_f_score)
        plt.plot(x, result_random_redundancy_score)
        plt.plot(x, result_random_coverage_score)
        plt.legend(labels=['f_score', 'redundancy_score', 'coverage_score'])
        plt.title("random")
        plt.show()

    # 输出数据
    headers = ["测试用例数"] + cluster_sample_list
    with open(output_file_addr, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows([
            ["削减-f指标"] + result_hierarchical_f_score,
            ["削减-冗余程度"] + result_hierarchical_redundancy_score,
            ["削减-覆盖率"] + result_hierarchical_coverage_score,
            ["随机-f指标"] + result_random_f_score,
            ["随机-冗余程度"] + result_random_redundancy_score,
            ["随机-覆盖率"] + result_random_coverage_score
        ])


if __name__ == "__main__":
    # f_measure_beta = 2
    #     # feature_data_file_addr = "..\\..\\resource\\feature_FxclDealLogParser_1000.json"
    #     # output_file_addr = "..\\..\\resource\\FxclDealLogParser_1000.csv"
    #     # run(input_file_addr=feature_data_file_addr, output_file_addr=output_file_addr,
    #     #     f_measure_beta=f_measure_beta, is_draw_plot=True)
    #     #
    #     # feature_data_file_addr = "..\\..\\resource\\feature_FxDealLogParser_1000.json"
    #     # output_file_addr = "..\\..\\resource\\FxDealLogParser_1000.csv"
    #     # run(input_file_addr=feature_data_file_addr, output_file_addr=output_file_addr,
    #     #     f_measure_beta=f_measure_beta, is_draw_plot=True)

    f_measure_beta = 2
    feature_data_file_addr = "..\\..\\resource\\feature_FxclDealLogParser_1000.json"
    output_file_addr = "..\\..\\resource\\FxclDealLogParser_1000_all.csv"
    run(input_file_addr=feature_data_file_addr, output_file_addr=output_file_addr,
        f_measure_beta=f_measure_beta, is_draw_plot=True)

    feature_data_file_addr = "..\\..\\resource\\feature_FxDealLogParser_1000.json"
    output_file_addr = "..\\..\\resource\\FxDealLogParser_1000_all.csv"
    run(input_file_addr=feature_data_file_addr, output_file_addr=output_file_addr,
        f_measure_beta=f_measure_beta, is_draw_plot=True)
