# CLUSTER_NUM_SAMPLE_LIST = list(range(1, 20, 1))  # 聚类的簇数量的采样
CLUSTER_NUM_SAMPLE_LIST = list(range(1, 21, 1)) + list(range(30, 110, 10)) + list(range(200, 1000, 100))  # 聚类的簇数量的采样
RANDOM_TIMES = 100  # 随机方法进行多次求平均时的重复次数
PCA_N_COMPONENTS = 100
F_MEASURE_BETA = 1  # f-meature指标的参数β的默认值
