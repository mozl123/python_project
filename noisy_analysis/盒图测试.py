# -*- coding: utf-8 -*-
"""
盒图绘制测试程序
"""
import matplotlib.pyplot as plt
import numpy as np

all_data = [np.random.normal(0, std, 100) for std in range(1, 4)]

fig = plt.figure(figsize=(8, 6))

plt.boxplot(all_data,
            notch=False,  # box instead of notch shape
            sym='rs',  # red squares for outliers
            vert=True)  # vertical box aligmnent

plt.xticks([y + 1 for y in range(len(all_data))], ['x1', 'x2', 'x3'])
plt.xlabel('measurement x')
t = plt.title('Box plot')
plt.show()

d1 = [1, 2, 10, 11, 12, 13, 14, 17, 19, 30, 31]
subfig2 = plt.subplot(1, 1, 1)
subfig2.boxplot(d1, widths=.25, vert=True)
subfig2.plot(np.full(9, 1.26), d1[:9], '+k', markeredgewidth=1)

subfig2.set_title("1. from non-robust estimates\n(Maximum Likelihood)")
plt.yticks(())
plt.show()
