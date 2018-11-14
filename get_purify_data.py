# -*- coding:utf-8 -*-
"""
推文格式转换,得到纯净推文
"""
import codecs
import re
from preprocess import *
EVENT_ID_PATTERN = re.compile(r"Event cluster_id: \d+")   # 匹配事件id
PATTERN2 = re.compile(r"\d+ \w{3} \w{3} \d+")
DESCRIPTION_PATTERN = re.compile(r"event description: .+")  # 匹配事件描述
NUM_PATTERN = re.compile(r"^\d+:.+")   # 匹配数字+冒号
# 分词器
tokenizer = TweetTokenize()

# t = u'event description: RT @FoxNews: Breaking News: Waffle House shooting suspect in custody, police say https://t.co/1UZKwsCIyP'
# res = PATTERN3.findall(t)
# print res
# print res[0][len(u'event description: '):]
# t = u'5:    After van attack, Toronto mayor emphasizes how ‘inclusive’ and ‘accepting’ his city is | TheBlaze https://t.co/MQkwf36sU4'
# res = PATTERN4.findall(t)
# print res
stop_words = load_stop_words(file_find("stop_words/english.stop"))
# print stop_words
MONTH_DICT = {'Jan': '01', "Feb": '02', "Mar": '03', "Apr": '04', "May": '05', "Jun": '06',
              "Jul": '07', "Aug": '08', "Sep": '09', "Oct": '10', "Nov": '11', "Dec": '12'}


def formatTweet(input_path, output_path):
    event_dict = {}  # 事件id不唯一！
    event_id = 0
    with codecs.open(input_path, encoding="utf-8", mode="r") as f:
        for line in f:
            line = line.strip()  # 去除边缘的空格和换行符
            if len(line) == 0:  # 无效推文
                continue
            res = EVENT_ID_PATTERN.findall(line)
            res1 = DESCRIPTION_PATTERN.findall(line)

            if len(res) > 0 or len(res1):
                if len(res) > 0:
                    cur_id = re.compile("\d+").findall(res[0])
                    event_dict[cur_id[0]] = []
                    event_id = cur_id[0]
                if len(res1) > 0:
                    desc = res1[0][len(u'event description: '):]
                    event_dict[event_id].append(desc)
                continue
            line = line.split("\t")
            if line[0].isdigit():
                event_dict[event_id].append([line[1], line[2], line[3]])

    output_file = codecs.open(output_path, encoding="utf-8", mode="w")

    res = sorted(event_dict.items(), key=lambda x: int(x[0]))
    # print res
    for item in res:
        output_file.write(item[0] + ":" + "\t" + item[1][0] + "\n")
        for sens in item[1][1:]:
            date = sens[0].split(' ')
            year = date[5]
            month = MONTH_DICT[date[1]]     # 月份
            day = date[2]
            time = date[3]
            res = year+u" "+month+u" "+day + u" "+time
            output_file.write(res + "\t" + str(sens[1]) + "\t" + sens[2] + "\n")
    output_file.close()


def tweetPurify(input_path, output_path):
    outputfile = codecs.open(output_path, encoding="utf8", mode="w")
    with codecs.open(input_path, encoding="utf8", mode="r") as f:
        for line in f:
            res = NUM_PATTERN.findall(line)
            if res:  # 找到了数字开头的行
                # outputfile.write(line)
                text1 = line.strip().split("\t")
                process_text = tokenizer.tokenize(text1[1])
                process_text = tokenizer.normalize(process_text)[0]
                text = " ".join(process_text)  # 先将列表转化为字符串，方便处理
                text = text.replace(':', '').replace(';', '').replace('?', '').replace('!', ''). \
                    replace('\'', '').replace('"', '').replace(',', '').replace('-', '').replace('_', ''). \
                    replace('/', '').replace('\\', '').replace('.', '')  # 替换标点符号
                text = text.strip()  # 去除边缘的空格
                text = re.sub('\s+', ' ', text)  # 将内部的连续多个空格替换成一个空格
                # text = text.lower()
                # text_list = text.split(" ")
                # text_list = [item for item in text_list if item not in stop_words]
                # text = " ".join(text_list)
                outputfile.write(text1[0] + "\t" + text + '\n')
            else:
                text1 = line.strip().split("\t")
                process_text = tokenizer.tokenize(text1[2])
                process_text = tokenizer.normalize(process_text)[0]
                # print process_text
                # if process_text is None:  # 如果预处理过后无内容则跳过
                #     continue
                #
                # if len(process_text) < 2:  # 如果预处理过后长度小于2则跳过
                #     continue

                text = " ".join(process_text)  # 先将列表转化为字符串，方便处理
                text = text.replace(':', '').replace(';', '').replace('?', '').replace('!', ''). \
                    replace('\'', '').replace('"', '').replace(',', '').replace('-', '').replace('_', ''). \
                    replace('/', '').replace('\\', '').replace('.', '')  # 替换标点符号
                text = text.strip()  # 去除边缘的空格
                text = re.sub('\s+', ' ', text)  # 将内部的连续多个空格替换成一个空格
                # text = text.lower()
                # text_list = text.split(" ")
                # text_list = [item for item in text_list if item not in stop_words]
                # text = " ".join(text_list)
                outputfile.write(text1[0] + "\t" + text1[1]+"\t"+text + '\n')  # 将文本转换为小写形式
    outputfile.close()

input_path1 = "data//20180424-20180503//event_realtime_result_20180424-20180503.txt"
output_path1 = "data//20180424-20180503//event_realtime_result_20180424-20180503_output.txt"
formatTweet(input_path=input_path1, output_path=output_path1)

output_path2 = "data//20180424-20180503//event_data.txt"
tweetPurify(input_path=output_path1, output_path=output_path2)



