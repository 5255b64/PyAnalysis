import csv

import numpy as np
from sklearn.decomposition import PCA

"""
PCA测试
"""


def run():
    with open('xxx.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow([1,2,3,4,5])


if __name__ == "__main__":
    result = run()
