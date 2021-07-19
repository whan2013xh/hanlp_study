# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-16
    FileName   : load_dictionary.py
    Author     : Honghe
    Descreption: 词典加载
"""

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
    return set(dic.keySet())

if __name__ == '__main__':
    res = load_dictionary()
    print(res)