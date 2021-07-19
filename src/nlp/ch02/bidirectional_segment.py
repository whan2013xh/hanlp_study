# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-16
    FileName   : bidirectional_segment.py
    Author     : Honghe
    Descreption: 双向最长匹配
"""
from .load_dictionary import load_dictionary
from .forward_segment import forward_segment
from .backward_segment import backward_segment

def count_single_char(word_list):
    """
    统计单个字符的单词
    :param word_list:
    :return:
    """
    return sum(1 for word in word_list if len(word))==1

def bidirectional_segment(text, dic):
    forward = forward_segment(text=text, dic=dic)
    backward = backward_segment(text=text, dic=dic)
    # print(f"forward segment: {forward}")
    # print(f"backward segment: {backward}")
    if len(forward)<len(backward):
        return forward
    elif len(forward)>len(backward):
        return backward
    else:
        if count_single_char(forward)>count_single_char(backward):
            return backward
        else:
            return forward

if __name__ == '__main__':
    text = "欢迎新老师生前来就餐"
    dic = load_dictionary()
    res = bidirectional_segment(text, dic)
    print(res)