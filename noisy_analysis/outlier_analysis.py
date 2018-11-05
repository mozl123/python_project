# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np


def boxplot_analysis(temporal_data, keys=None):
    """
    盒图分析
    :param temporal_data: 数据
    :param keys: 数据的标识
    :return:
    """
    plt.boxplot(temporal_data,
                notch=False,  # box instead of notch shape
                sym='rs',  # red squares for outliers
                vert=True)  # vertical box aligmnent
    i = 1
    for item in temporal_data:
        plt.plot(np.full(len(item), i+0.26), item, '+k', markeredgewidth=1)
        i += 1
    plt.xticks([y + 1 for y in range(len(temporal_data))], keys)
    plt.xlabel('measurement x')
    plt.title('Box plot')
    plt.show()


if __name__ == '__main__':
    t = [[1, 2, 3, 4, 6, 9, 20], [1, 3, 4, 5, 6, 7, 10, 20]]
    boxplot_analysis(t, keys=['1', '2'])

