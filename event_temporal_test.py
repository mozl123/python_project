# -*- coding:utf-8 -*-

"""
事件时序分析测试程序
"""
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

    key1 = '437'
    key2 = '929'
    # fastdtw_algorithm(d[key1], d[key2], t[key1], t[key2], key1, key2)
    # """
    # noise and outlier test
    # 去除停止词，词性还原
    # """
    # path1 = ".//data//time_feature//temp//929.txt"
    # # path2 = ".//data//time_feature//temp//1048.txt"
    #
    # TIME = 0
    # NUMS = 1
    # TEXT = 2
    #
    # d929_time = []
    # d929_nums = []
    # d929_text = []
    # with codecs.open(filename=path1, mode='r') as f:
    #     for line in f:
    #         line = line.strip('\n')
    #         line = line.split('\t')
    #         times, nums, text = line[TIME][:-3], \
    #                             int(line[NUMS]), line[TEXT].split(' ')
    #         new_text = []
    #         for word in text:
    #             w = wn.morphy(word)
    #             if w is None:
    #                 new_text.append(word)
    #             else:
    #                 new_text.append(w)
    #
    #         d929_time.append(time.mktime(time.strptime(times, "%Y %m %d %H:%M")))
    #         d929_nums.append(nums + 1)
    #         if len(new_text) < 3:
    #             continue
    #         d929_text.append(new_text)

    # from preprocess.tweet_tokenize.tweet_tokenize import *
    # stem = modalVerbExtract(["attacks", "attack"])  # 所有格还原
    # print stem

    # '''词性标注测试'''
    #
    # from preprocess.tweet_pos import *
    # from preprocess import *
    # pos_tagger = PerceptronPOSTagger()
    # pos_tagger.load_model(file_find("tweet_pos/model/pos_model_150k.pickle"))
    # tokens = "US police seek motive van attack killed 10 manila bulletin".split(' ')
    # print tokens
    # res = pos_tagger.tag(tokens)
    # print res
    #
    # # 地名识别
    # loc_tagger = Maxent()
    # loc_tagger.load_model(file_find("tweet_loc/model/Maxent_tweet_model_without_zero_#.pickle"))
