# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-19
    FileName   : speed_benchmark.py
    Author     : Honghe
    Descreption: 双向最长匹配
"""
import time
from nlp.ch02.load_dictionary import load_dictionary
from nlp.ch02.forward_segment import forward_segment
from nlp.ch02.backward_segment import backward_segment
from nlp.ch02.bidirectional_segment import bidirectional_segment

def evaluate_speed(segment, text, dic, pressure):
    start = time.time()
    for i in range(pressure):
        segment(text, dic)
    elapsed_time = time.time()-start
    print("%s :%.2f 万字/秒" %(segment.__name__,len(text)*pressure/10000/elapsed_time))

if __name__ == '__main__':
    text = "江西鄱阳湖干枯，中国最大淡水湖变成大草原"
    pressure = 10000
    dic = load_dictionary()

    evaluate_speed(forward_segment, text, dic, pressure)
    evaluate_speed(backward_segment, text, dic, pressure)
    evaluate_speed(bidirectional_segment, text, dic, pressure)