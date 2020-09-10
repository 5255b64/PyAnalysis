from src.CFeatureData import FeatureData
import matplotlib.pyplot as plt


class IndicatorCollector:
    """
    指标收集器
    在已有特征数据FeatureData的情况下
    计算所需的指标
    """

    def get_calculate_index(self):
        """
        获取评价指标
        使用AUC指标
        图表的纵轴最大值固定为self.total_probe_num（插桩总数）
        横纵坐标为self.case_cover_probe_num_list内的数组（仅有两个值[x,y]，x代表横坐标值，y代表纵坐标值）
        :return:
        """
        value = 0
        previous = self.case_cover_probe_num_list[0]
        for sample in self.case_cover_probe_num_list:
            x = sample[0]
            y = sample[1]
            x_previous = previous[0]
            y_previous = previous[1]
            value = value + (y + y_previous) * (x - x_previous) / 2
            previous = [x, y]
        value = value * 100 / previous[0] / self.total_probe_num
        return value

    def get_probe_covered_num_total(self):
        return self.probe_covered_num_total

    def get_probe_covered_by_case_num(self):
        return self.probe_covered_by_case_num

    def get_case_cover_probe_num_list(self):
        return self.case_cover_probe_num_list

    def plot_case_cover_probe_num_list(self):
        x = list()
        y = list()
        for sample in self.case_cover_probe_num_list:
            x.append(sample[0])
            y.append(sample[1])
        plt.axis([self.case_cover_probe_num_list[0][0], self.case_cover_probe_num_list[-1][0], 0, self.total_probe_num])

        plt.plot(x, y)

        plt.text(self.case_cover_probe_num_list[-1][0]/2, self.total_probe_num*0.7, str(self.get_calculate_index()), fontsize=10)

        plt.show()

    def get_total_case_cover_probe_num_list(self):
        return self.total_case_cover_probe_num_list

    def plot_total_case_cover_probe_num_list(self):
        x = list()
        y = list()
        for sample in self.total_case_cover_probe_num_list:
            x.append(sample[0])
            y.append(sample[1])

        plt.plot(x, y)

        plt.show()

    def __init__(self, feature_data: FeatureData):
        self.feature_data = feature_data
        # 插入的桩总数
        self.total_probe_num = feature_data.totalProbeNum
        # 每个桩被覆盖的次数 以及 每个桩被多少个测试用例覆盖
        self.probe_covered_num_total = dict()  # 每个桩被覆盖的次数（有重复）
        self.probe_covered_by_case_num = dict()  # 每个桩被多少个测试用例覆盖（无重复）
        self.case_cover_probe_num_dict = dict()  # 仅被x个测试用例覆盖的桩有多少个（字典类型）
        self.case_cover_probe_num_list = list()  # 仅被x个测试用例覆盖的桩有多少个（数组类型）
        self.total_case_cover_probe_num_dict = dict()  # 仅被覆盖x次的桩有多少个（字典类型）
        self.total_case_cover_probe_num_list = list()  # 仅被覆盖x次的桩有多少个（数组类型）
        testsuite = feature_data.testSuite
        for tc_key in testsuite.keys():
            testcase = testsuite[tc_key]
            for probe_key in testcase.probeInfos:
                probe_str = probe_key  # 桩的唯一标识（字符串形式）
                probe_covered_num_within_sigle_testcase = testcase.probeInfos[probe_key]  # 某个桩被单个测试用例cover的次数

                # 计算数据 每个桩被覆盖的次数（有重复）
                if probe_key not in self.probe_covered_num_total:
                    self.probe_covered_num_total[probe_key] = probe_covered_num_within_sigle_testcase
                else:
                    self.probe_covered_num_total[probe_key] = self.probe_covered_num_total[
                                                                  probe_key] + probe_covered_num_within_sigle_testcase

                # 计算数据 每个桩被多少个测试用例覆盖（无重复）
                if probe_key not in self.probe_covered_by_case_num:
                    self.probe_covered_by_case_num[probe_key] = 1
                else:
                    self.probe_covered_by_case_num[probe_key] = self.probe_covered_by_case_num[probe_key] + 1

        # 计算数据 仅被x个测试用例覆盖的桩有多少个
        for key in self.probe_covered_by_case_num:
            if self.probe_covered_by_case_num[key] not in self.case_cover_probe_num_dict:
                self.case_cover_probe_num_dict[self.probe_covered_by_case_num[key]] = 1
            else:
                self.case_cover_probe_num_dict[self.probe_covered_by_case_num[key]] = self.case_cover_probe_num_dict[
                                                                                          self.probe_covered_by_case_num[
                                                                                              key]] + 1
        """计算未被覆盖的桩的数量
        sum = 0
        for i in self.case_cover_probe_num_dict:
            sum = sum + self.case_cover_probe_num_dict[i]
        self.case_cover_probe_num_dict[0] = self.total_probe_num - sum
        """

        for i in sorted(self.case_cover_probe_num_dict):
            self.case_cover_probe_num_list.append((i, self.case_cover_probe_num_dict[i]))
        # 计算数据 仅被覆盖x次的桩有多少个
        for key in self.probe_covered_num_total:
            if self.probe_covered_num_total[key] not in self.total_case_cover_probe_num_dict:
                self.total_case_cover_probe_num_dict[self.probe_covered_num_total[key]] = 1
            else:
                self.total_case_cover_probe_num_dict[self.probe_covered_num_total[key]] = \
                    self.total_case_cover_probe_num_dict[
                        self.probe_covered_num_total[
                            key]] + 1
        """计算未被覆盖的桩的数量
        sum = 0
        for i in self.probe_covered_num_total:
            sum = sum + self.probe_covered_num_total[i]
        self.probe_covered_num_total[0] = self.total_probe_num - sum
        """

        for i in sorted(self.total_case_cover_probe_num_dict):
            self.total_case_cover_probe_num_list.append((i, self.total_case_cover_probe_num_dict[i]))

    def print(self):
        print("total_probe_num=" + str(self.total_probe_num))
        print("probe_covered_num_total=" + str(self.probe_covered_num_total))
        print("probe_covered_by_case_num=" + str(self.probe_covered_by_case_num))
        print("case_cover_probe_num_list=" + str(self.case_cover_probe_num_list))
        # for i in sorted(self.case_cover_probe_num_dict):
        #     print((i, self.case_cover_probe_num_dict[i]))
        print("total_case_cover_probe_num_list=" + str(self.total_case_cover_probe_num_list))

        # for i in sorted(self.total_case_cover_probe_num_dict):
        #     print((i, self.total_case_cover_probe_num_dict[i]))


if __name__ == "__main__":
    feature_data_file_path = "..\\resource\\cstp_feature.json"
    fd = FeatureData()
    fd.load(feature_data_file_path)
    ic = IndicatorCollector(fd)
    ic.print()
