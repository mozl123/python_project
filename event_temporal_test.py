# -*- coding:utf-8 -*-

"""
事件时序分析测试程序
"""
from event_temporal_relationship.event_temporal import *
from preprocess.shortTextSimilarity.short_text_similarity import *
from preprocess.event_evolution.noisy_analysis.outlier_analysis import *
import codecs
import time
from nltk.corpus import wordnet as wn

TIME = 0
NUMS = 1
TEXT = 2


def read_data(path):

    data_time = []
    data_nums = []
    data_text = []
    with codecs.open(filename=path, mode='r') as f:
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
    return data_time, data_nums, data_text

if __name__ == '__main__':

    path1 = ".//data//time_feature//dallas//4354.txt"
    path2 = ".//data//time_feature//dallas//437.txt"
    data_time1, data_nums1, data_text1 = read_data(path1)
    data_time2, data_nums2, data_text2 = read_data(path2)

    boxplot_analysis([data_time1, data_time2], ['4354', '437'])
    # from preprocess.tweet_tokenize.tweet_tokenize import *
    # stem = modalVerbExtract(["attacks", "attack"])  # 所有格还原
    # print stem

    # '''词性标注测试'''
    # from preprocess.tweet_pos import *
    # from preprocess import *
    # pos_tagger = PerceptronPOSTagger()
    # pos_tagger.load_model(file_find("tweet_pos/model/pos_model_150k.pickle"))
    # tokens = "US police seek motive van attack killed 10 manila bulletin".split(' ')
    # print tokens
    # res = pos_tagger.tag(tokens)
    # print res
    # # 地名识别
    # loc_tagger = Maxent()
    # loc_tagger.load_model(file_find("tweet_loc/model/Maxent_tweet_model_without_zero_#.pickle"))
