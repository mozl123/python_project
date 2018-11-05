# -*- coding: utf-8 -*-

"""测试1， z-score检测异常值"""
import pandas as pd  # 导入pandas库

# 生成异常数据
df = pd.DataFrame({'col1': [1, 120, 3, 5, 2, 12, 13],'col2':[12, 17, 31, 53, 22, 32, 43]})
print (df)  # 打印输出

# 通过Z-Score方法判断异常值
df_zscore = df.copy()  # 复制一个用来存储Z-score得分的数据框
cols = df.columns   # 获得数据框的列名
for col in cols:  # 循环读取每列
    df_col = df[col]  # 得到每列的值
    z_score = (df_col - df_col.mean()) / df_col.std()  # 计算每列的Z-score得分
    df_zscore[col] = z_score.abs() > 2.2  # 判断Z-score得分是否大于2.2，如果是则是True，否则为False
print df_zscore  # 打印输出

"""测试2，LOF算法"""
from sklearn.neighbors.lof import LocalOutlierFactor
clf = LocalOutlierFactor(n_neighbors=20, algorithm='auto', contamination=0.1, n_jobs=-1)
