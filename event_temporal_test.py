# -*- coding:utf-8 -*-

"""
事件时序分析测试程序
"""
from event_temporal_relationship.event_temporal import *

# from preprocess.shortTextSimilarity.short_text_similarity import *
from preprocess.event_evolution.noisy_analysis.outlier_analysis import *
from preprocess import *
from preprocess.tweet_pos import *
import codecs
import time
from nltk.corpus import wordnet as wn

TIME = 0
NUMS = 1
TEXT = 2


def read_data(path):
    """
    读取文本数据，文本格式为北京时间-推文数-推文文本
    :param path:
    :return:
    """
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

    key1, key2, key3 = "4354_origin", "437_origin", "710_origin"
    path1 = ".//data//time_feature//dallas//"+key1+".txt"
    path2 = ".//data//time_feature//dallas//"+key2+".txt"
    path3 = ".//data//time_feature//dallas//"+key3+".txt"
    data_time1, data_nums1, data_text1 = read_data(path1)
    data_time2, data_nums2, data_text2 = read_data(path2)
    data_time3, data_nums3, data_text3 = read_data(path3)

    boxplot_analysis([data_time1, data_time2, data_time3], [key1, key2, key3])

    # 词性标注
    pos_tagger = PerceptronPOSTagger()
    pos_tagger.load_model(file_find("tweet_pos/model/pos_model_150k.pickle"))
    # 地名识别
    loc_tagger = Maxent()
    loc_tagger.load_model(file_find("tweet_loc/model/Maxent_tweet_model_without_zero_#.pickle"))

    ner_tagger = MaxEntropy()
    ner_tagger.load_model(file_find("tweet_ner/model/Maxent_tweet_model.pickle"))

    loc_list = []
    loc_dict = {}
    for i, tokens in enumerate(data_text2):
        res = pos_tagger.tag(tokens)
        # print i, res
        (pre_tag, labels, result) = loc_tagger.token_classify([res])
        # print result
        loc_info = [item[0] for item in result if item[1] == 'LOC']
        for loc in loc_info:
            if loc in loc_dict:
                loc_dict[loc] += 1
            else:
                loc_dict[loc] = 1
        i += 1
        loc_list.append(loc_info)
    # print loc_list
    print loc_dict
    # from preprocess.tweet_tokenize.tweet_tokenize import *
    # stem = modalVerbExtract(["Can't", "What's"])  # 所有格还原
    # print stem

    # '''词性标注测试'''
    # # 地名识别
    # loc_tagger = Maxent()
    # loc_tagger.load_model(file_find("tweet_loc/model/Maxent_tweet_model_without_zero_#.pickle"))
