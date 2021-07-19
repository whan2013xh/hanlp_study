# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-16
    FileName   : forward_segment.py
    Author     : Honghe
    Descreption: 正向最长匹配
"""
from .load_dictionary import load_dictionary


def forward_segment(text, dic):
    word_list = []
    i = 0
    while i <len(text):
        longest_word = text[i]
        for j in range(i+1, len(text)+1):
            word = text[i:j]
            # 这里其实只需要判断word是否在词典中，而不用判断是否是最长的
            # 因为j是在不断增大的
            if word in dic:
                longest_word = word
        i += len(longest_word)
        word_list.append(longest_word)
    return word_list


if __name__ == '__main__':
    dic = load_dictionary()
    word_list = forward_segment("就读北京大学", dic)
    print(word_list)