# -*- coding: utf-8 -*-
"""
特征抽取包，关键词的信息熵
"""
import math
import codecs
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt


def entropy_compute(d):
    # 计算词频字典d中的每个单词的信息熵
    num = sum(d.values())
    d = {k: float(v)/num for k, v in d.iteritems()}

    mydict = {}
    res = 0.0
    for item in d.iteritems():
        res += -item[1] * math.log(item[1])
    for item in d.iteritems():
        mydict[item[0]] = -item[1] * math.log(item[1]) / res
    return mydict


def loc_recognize(text_data):
    """
    空间实体识别
    :param text_data:文本序列
    :return:
    """
    for text in text_data:
        pass



if __name__ == '__main__':
    path1 = "..//data//time_feature//temp//710.txt"
    word_dict = {}

    with codecs.open(path1, mode='r') as f:
        for line in f:
            line = line.strip('\n')
            line = line.split('\t')
            text = line[2].split(' ')
            for word in text:
                w = wn.morphy(word)
                if w is None:
                    w = word
                if w in word_dict:
                    word_dict[w] += 1
                else:
                    word_dict[w] = 1

    mydict = entropy_compute(word_dict)

    res = sorted(mydict.items(), key=lambda x: x[1], reverse=True)
    num_list = [item[1] for item in res]
    name_list = [item[0] for item in res]

    value = 0.0
    N = 0
    lam = 0.4
    for k, v in res:
        value += v
        if value >= lam:
            print "**************************"
            print k
            print "**************************"
            break
        N += 1
        print k, v
    print N
    print name_list[:N]
    plt.bar(xrange(N), num_list[:N])
    plt.xticks(xrange(N), name_list[:N])
    plt.show()

    from preprocess.tweet_pos import *
    from preprocess import *
    pos_tagger = PerceptronPOSTagger()
    ll = "2 officers critically wounded in Dallas shooting".split(' ')
    pos_tagger.load_model(file_find("preprocess//data//tweet_pos/model/pos_model_150k.pickle"))

    res = pos_tagger.tag(ll)
    print res

