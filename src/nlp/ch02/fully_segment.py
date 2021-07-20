# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-16
    FileName   : fully_segment.py
    Author     : Honghe
    Descreption: 完全切分
"""
from .load_dictionary import load_dictionary


def fully_segment(text, dic):
    word_list = []
    for i in range(len(text)):
        for j in range(i, len(text)+1):
            word = text[i:j]
            if word in dic:
                word_list.append(word)
    return word_list



if __name__ == '__main__':
    dic = load_dictionary()
    word_list = fully_segment("北京大学", dic)
    print(word_list)