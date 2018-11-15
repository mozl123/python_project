# -*- coding:utf-8 -*-
"""
事件时序分析测试程序

"""
from event_temporal_relationship.event_temporal import *
import os
from preprocess import *
import codecs
from nltk.corpus import wordnet as wn
from kernel_density.kernel_density_model import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TIME = 0
NUMS = 1
TEXT = 2
KEYS = 3


def read_dir(dir_path='./'):
    keys_list = []
    path_list = []
    path_dir = os.listdir(dir_path)
    # print path_dir
    for allDir in path_dir:
        if allDir[0].isdigit():  # 只读取事件txt
            keys_list.append(allDir.strip(".txt"))
            path_list.append(os.path.join('%s%s' % (dir_path, allDir)))
    return keys_list, path_list


class EventTemporal:
    def __init__(self, keys, file_path):
        self.data = []
        self._data_time = []
        self._data_nums = []
        self._data_text = []
        self._keys = keys
        self.file_path = file_path
        self.cross_count = 0

    def read_data(self):
        for item in self.file_path:  # 读取每个文件中的数据
            self._read_file(item)

        self.data = zip(self._data_time, self._data_nums, self._data_text, self._keys)
        self.data.sort(key=lambda x: min(x[TIME]))  # 按照开始时间排序
        self._data_time = [item[TIME] for item in self.data]
        self._data_nums = [item[NUMS] for item in self.data]
        self._data_text = [item[TEXT] for item in self.data]
        self._keys = [item[KEYS] for item in self.data]

    def _read_file(self, input_path):
        """
        读取文本数据，文本格式为北京时间-推文数-推文文本
        :param input_path:
        :return:
        """
        data_time = []
        data_nums = []
        data_text = []

        with codecs.open(filename=input_path, mode='r') as f:
            for line in f:
                line = line.strip('\n')
                line = line.split('\t')
                times, nums, text = line[TIME], int(line[NUMS]), line[TEXT].split(' ')
                new_text = []
                for word in text:
                    w = wn.morphy(word)
                    if w is None:
                        new_text.append(word)
                    else:
                        new_text.append(w)

                data_time.append(time.mktime(time.strptime(times, "%Y %m %d %H:%M:%S")))
                data_nums.append(nums + 1)
                if len(new_text) < 3:
                    continue
                data_text.append(new_text)

        self._data_time.append(data_time)
        self._data_nums.append(data_nums)
        self._data_text.append(data_text)

    def print_temporal_relations(self):
        """
        绘制对比图，多组数据
        :return:
        """
        delay_time_matrix = []
        time_len = len(self._data_time)
        for i in xrange(time_len):
            for j in xrange(i + 1, time_len):
                delay_time = fastdtw_algorithm(self._data_time[i], self._data_time[j], self._keys[i],
                                               self._keys[j], n1=None, n2=None)
                delay_time_matrix.append(delay_time)

        # 打印二维矩阵
        new_delay_time_matrix = map(lambda x: 1 if x > 0 else -1, delay_time_matrix)
        j = 0
        for i in xrange(time_len - 1, 0, -1):
            print new_delay_time_matrix[j:j + i]
            j += i

    def compute_cross_num(self):
        row = len(self._data_time)
        count = 0
        for ii in xrange(row):
            for jj in xrange(ii + 1, row):
                if min(self._data_time[ii]) > max(self._data_time[jj]) or \
                                min(self._data_time[jj]) > max(self._data_time[ii]):
                    continue
                else:
                    print self._keys[ii], self._keys[jj]
                    count += 1
        self.cross_count = count
        print "总计：", count
        return count

if __name__ == '__main__':
    dir_path = ".//data//20180424-20180503//Toronto//"
    keys_list, path_list = read_dir(dir_path)
    # print keys_list, path_list

    temporal = EventTemporal(keys_list, path_list)
    temporal.read_data()
    cross_num = temporal.compute_cross_num()
    # temporal.print_temporal_relations()

    # 打印
    # for item in temporal.data:
    #     print item[3], item[0], item[1], item[2]
