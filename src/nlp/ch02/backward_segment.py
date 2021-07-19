# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-16
    FileName   : backward_segment.py
    Author     : Honghe
    Descreption: 逆向最长匹配
"""
from .load_dictionary import load_dictionary


def backward_segment(text, dic):
    word_list = []
    i = len(text)-1
    while i > 0:
        longest_word = text[i]
        for j in range(0, i):
            word = text[j:i+1]
            if word in dic and len(longest_word)<len(word):
                longest_word = word
        i -= len(longest_word)
        word_list.append(longest_word)
    return word_list


if __name__ == '__main__':
    dic = load_dictionary()
    word_list = backward_segment("就读北京大学", dic)
    print(word_list)