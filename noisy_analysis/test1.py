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