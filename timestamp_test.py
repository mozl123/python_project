# -*- coding:utf-8 -*-
import time

# 时间戳转格林威治时间
# timeStamp=0对应1970--01--01 08:00:00
# print time.time()   # 打印当地时间

# 第一次开始时间1523490881， 结束时间1523490881+43200
timeStamp = 1523423096    # 1523462058+86400*4+400
timeArray = time.localtime(timeStamp)   # 格式化时间戳为本地的时间
otherStyleTime = time.strftime("%Y %m %d %H:%M:%S", timeArray)
print otherStyleTime  # 2013 10 10 23:40:00

# 本地时间转时间戳
date = "2017 12 08 00:00:00"
timeStamp = time.mktime(time.strptime(date, "%Y %m %d %H:%M:%S"))
print timeStamp     # 5.15:1526313600, 5.17:1526486400

a = "123"

