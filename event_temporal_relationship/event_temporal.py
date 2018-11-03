# -*- coding:utf-8 -*-
"""用于事件时序关系定量计算"""

import matplotlib.pyplot as plt
from fastdtw import fastdtw


def plot_qq(t1, t2, key1, key2, n1=None, n2=None):
    """
    绘制两个时间序列的QQ图
    :param t1:时间序列1
    :param t2:时间序列2
    :param n1:时间序列1对应的事件个数序列
    :param n2:时间序列2对应的事件个数序列
    :param key1:时间序列1的标志
    :param key2:时间序列2的标志
    :return:t1-t2
    """
    l = len(t1)
    # 获得各分位数
    f = [(i - 0.5) / l for i in xrange(1, l + 1)]

    # 得到每个分位数对应的值
    t11 = [t1[int(f[i] * l)] for i in xrange(0, l)]
    t22 = [t2[int(f[i] * l)] for i in xrange(0, l)]

    # qq图描点
    plt.scatter(t11, t22)
    plt.plot(t11, t11)
    plt.xlabel(u"时间/秒, " + key1, fontproperties='SimHei')
    plt.ylabel(u"时间/秒, " + key2, fontproperties='SimHei')
    plt.title(u"q-q图", fontproperties='SimHei')
    plt.show()

    if n1 is not None and n2 is not None:
        # 建立dtw算法得到的对齐以后的时间序列和事件个数的键值对
        n1_dict = {k: v for k, v in zip(t1, n1)}
        n2_dict = {k: v for k, v in zip(t2, n2)}

        # 建立对齐以后的时间序列的事件个数列表
        new_n1 = [n1_dict[item] for item in n1]
        new_n2 = [n2_dict[item] for item in n2]
        # 绘制推文数目随时间变化曲线
        plt.plot(t1, new_n1, c='g', label=u"1")
        plt.scatter(t1, new_n1, c='g')
        plt.plot(t2, new_n2, c='r', label=u"2")
        plt.scatter(t2, new_n2, c='r')
        plt.legend(loc='upper left')
        plt.xlabel(u"时间/秒", fontproperties='SimHei')
        plt.ylabel(u"推文数目/条", fontproperties='SimHei')
        plt.title(u"时间分布对比图", fontproperties='SimHei')
        plt.show()

    # 计算平均时延
    delay = [i1 - i2 for i1, i2 in zip(t1, t2)]
    delay_time = sum(delay) / l

    print key1 + "-" + key2 + ":", delay_time
    return delay_time


def fastdtw_algorithm(t1, t2, key1, key2, n1=None, n2=None):
    """
    快速动态时间规整算法
    :param t1:时间序列1
    :param t2:时间序列2
    :param n1:时间序列1对应的事件的个数序列
    :param n2:时间序列2对应的事件的个数序列
    :param key1:时间序列1标志
    :param key2:时间序列2标志
    :return:
    """
    # t为两时间序列的近似距离，默认绝对值距离作为度量标准。
    # path为对应关系。每个元素为一个2维元组。
    # 执行动态时间规整
    t, path = fastdtw(t1, t2)

    # 获得每一对“下标对应关系”
    index1 = [item[0] for item in path]
    index2 = [item[1] for item in path]

    # dtw算法得到的对齐的新的时间序列
    new_t1 = [t1[item] for item in index1]
    new_t2 = [t2[item] for item in index2]

    # 绘图，便于可视化，在y=1和y=5画线
    y1 = len(new_t1) * [1]
    y2 = len(new_t2) * [5]
    l1 = plt.scatter(new_t1, y1, c='r')
    l2 = plt.scatter(new_t2, y2, c='g')
    plt.ylim(0, 6)
    """绘制dtw算法得到的对应关系"""
    # 构建坐标
    coordinate1 = zip(new_t1, y1)
    coordinate2 = zip(new_t2, y2)

    # 定义坐标
    xx = 0
    yy = 1
    # 绘制对应关系
    for item1, item2 in zip(coordinate1, coordinate2):
        plt.plot((item1[xx], item2[xx]), (item1[yy], item2[yy]), c='b')

    plt.xlabel(u"时间/秒, ", fontproperties='SimHei')
    plt.title(u"动态时间规整对应关系图", fontproperties='SimHei')
    plt.legend(prop={'family': 'SimHei', 'size': 15})
    plt.legend(handles=[l1, l2, ], labels=[key1, key2], loc='upper left')
    plt.show()

    # 绘制QQ图
    plot_qq(new_t1, new_t2, key1, key2, n1, n2)


def is_same_time(delay_time, threshold):
    """
    根据时延阈值判断是否同时发生
    :param delay_time:时延值，单位是秒。
    :param threshold:时延阈值，小于该值认为同时发生
    :return:
    """
    if abs(delay_time) < threshold:
        return True
    else:
        return False
