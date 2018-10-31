# -*- coding:utf-8 -*-

from event_temporal_relationship.event_temporal import *
from preprocess.shortTextSimilarity.short_text_similarity import *
import codecs
import time
from nltk.corpus import wordnet as wn
if __name__ == '__main__':

    """
    DTW test
    动态时间规整算法比较两个时间序列
    """
    # event1_time每行为一个事件的时间序列
    event1_time = "./data/event1_time.txt"
    # event1_nums每行为一个事件的数目序列
    event1_nums = "./data/event1_nums.txt"

    d = {}
    with codecs.open(event1_time, mode='r', encoding="utf-8") as f:
        for line in f:
            line = line.strip('\n')
            event_id, event_time = line.split('\t')[0], line.split('\t')[1]
            event_time_list = event_time.split(' ')
            event_time_list = [float(item) for item in event_time_list]

            d[event_id] = event_time_list
    for k, v in d.iteritems():
        print k, v

    t = {}
    with codecs.open(event1_nums, mode='r', encoding="utf-8") as f:
        for line in f:
            line = line.strip('\n')
            event_id, event_nums = line.split('\t')[0], line.split('\t')[1]
            event_time_list = event_nums.split(' ')
            event_time_list = [int(item) for item in event_time_list]
            t[event_id] = event_time_list
    for k, v in t.iteritems():
        print k, v

    key1 = '1048'
    key2 = '929'
    fastdtw_algorithm(d[key1], d[key2], t[key1], t[key2], key1, key2)
	
