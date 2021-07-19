# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-19
    FileName   : bin_tree_speed.py
    Author     : Honghe
    Descreption: 
"""
import time
from bin_trie import BinTrie
from nlp.ch02.forward_segment import forward_segment
from nlp.ch02.backward_segment import backward_segment
from nlp.ch02.bidirectional_segment import bidirectional_segment

from pyhanlp import *

def load_dictionary():
    """
    加载Hanlp中的mini词库
    :return:
    """
    IOUtil = JClass('com.hankcs.hanlp.corpus.io.IOUtil')
    path = HanLP.Config.CoreDictionaryPath.replace('.txt', '.mini.txt')
    print(path)
    dic = IOUtil.loadDictionary([path])
    return dic


def evaluate_speed(segment, text, dic, pressure):
    start = time.time()
    for i in range(pressure):
        segment(text, dic)
    elapsed_time = time.time()-start
    print("%s :%.2f 万字/秒" %(segment.__name__, len(text)*pressure/10000/elapsed_time))

def tranfer2dict(dic):
    res = {}
    for key in dic:
        value = dic.get(key)
        res[key] = value
    return res

def test_list(list, pressure):
    start = time.time()
    for i in range(pressure):
        if i in list:
            pass
    print(f"list search cost: {time.time()-start}")

def test_set(set_dic, pressure):
    start = time.time()
    for i in range(pressure):
        if i in set_dic:
            pass
    print(f"set search cost: {time.time()-start}")


if __name__ == '__main__':
    text = "江西鄱阳湖干枯，中国最大淡水湖变成大草原"
    pressure = 10000
    dic = load_dictionary()
    list_dic = [i for i in range(60000)]
    set_dic = set(list_dic)
    test_list(list_dic, pressure)
    test_set(set_dic,pressure)
    start = time.time()
    dict_dic = tranfer2dict(dic)
    bin_tree_dic = BinTrie(dict_dic)
    print(f"build tree cost: {time.time()-start}")
    print(forward_segment(text, bin_tree_dic))

    # evaluate_speed(forward_segment, text, bin_tree_dic, pressure)
    # evaluate_speed(backward_segment, text, bin_tree_dic, pressure)
    # evaluate_speed(bidirectional_segment, text, bin_tree_dic, pressure)