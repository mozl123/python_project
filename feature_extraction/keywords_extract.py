# -*- coding: utf-8 -*-
from summa import keywords
import codecs
from nltk.corpus import wordnet as wn
from summa import summarizer
from preprocess.shortTextSimilarity.short_text_similarity import *
import time
from preprocess.event_evolution.event_temporal_relationship.event_temporal import *


def key_sentences_extract(path):
    """
    提取语料库中的关键句子
    :param path:语料库路径
    :return:
    """
    sens = ""
    sens_list = []
    text_time_dict = {}  # 文本-时间戳字典
    with codecs.open(path, mode='r') as f:
        for line in f:
            line = line.strip('\n')
            line = line.split('\t')
            text = line[2].split(' ')
            times = line[0][:-3]

            # 词性还原
            new_sens = []
            for word in text:
                w = wn.morphy(word)
                if w is None:
                    w = word
                sens += " " + w
                new_sens.append(w)
            new_text = " ".join(new_sens)
            text_time_dict[new_text] = time.mktime(time.strptime(times, "%Y %m %d %H:%M"))
            sens += '.'
            sens_list.append(new_sens)
    print "***************keywords****************"
    print keywords.keywords(sens)
    # print text_time_dict
    key_sens = summarizer.summarize(sens, ratio=0.3)
    key_sens_list = key_sens.split('\n')
    key_sens_token_list = [sens.strip('.').split(' ') for sens in key_sens_list]
    res = []
    for item in sens_list:
        score = 0.0
        if " ".join(item) not in key_sens_token_list:
            for sen in key_sens_token_list:
                score += similarity_jaccard(item, sen)  # jaccard相似度
                # score += similarity_textrank(item, sen)   # textrank相似度
            score /= len(key_sens_token_list)
            res.append([item, score])

    res = sorted(res, key=lambda x: x[1], reverse=True)
    # for item in res:
    #     print " ".join(item[0]), item[1]

    new_time = []
    for item in res[:int(len(res)*0.8)]:
        key = " ".join(item[0])
        tt = text_time_dict[key]
        # print key, tt, item[1]
        new_time.append(tt)
    new_time.sort()
    return new_time

if __name__ == '__main__':

    key1 = '710'
    key2 = '4354'
    path1 = "..//data//time_feature//dallas//"+key1+".txt"
    path2 = "..//data//time_feature//dallas//"+key2+".txt"
    time1 = key_sentences_extract(path1)
    time2 = key_sentences_extract(path2)
    print time1
    print time2

    fastdtw_algorithm(time1, time2, key1, key2)
