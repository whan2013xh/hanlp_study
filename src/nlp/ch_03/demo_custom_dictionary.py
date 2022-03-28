# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-12-13
    FileName   : demo_custom_dictionary.py
    Author     : Honghe
    Descreption: 
"""
from pyhanlp import *

ViterbiSegment = SafeJClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')

segment = ViterbiSegment()
sentence = "社会摇摆简称社会摇"
segment.enableCustomDictionary(False)
print("不挂载词典：", segment.seg(list(sentence)))
CustomDictionary.insert("社会摇","nz 100")
segment.enableCustomDictionary(True)
print("低优先级词典：", segment.seg(list(sentence)))
segment.enableCustomDictionaryForcing(True)
print("高优先级词典：", segment.seg(list(sentence)))


