# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-12
    FileName   : base_node.py
    Author     : Honghe
    Descreption: 基础节点类
"""
from enum import Enum


class BaseNode:
    def __init__(self, key=None, status=None, value=None):
        self._children = []
        self.key = key
        self.value = value
        self.status = status

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def compare_to(self, other):
        key = other.key if isinstance(other, BaseNode) else other
        if self.key > key:
            return 1
        elif self.key < key:
            return -1
        else:
            return 0

    def transition(self, text, begin=0):
        cur = self
        for i in range(begin, len(text)):
            cur = cur.get_child(text[i])
            if cur is None or cur.status == Status.UNDEFINED_0:
                return None
        return cur


class Status(Enum):
    # 为序列值指定value值
    # 未指定，用于删除词条
    UNDEFINED_0 = 0
    # 不是词语的结尾
    NOT_WORD_1 = 1
    # 是个词语的结尾，并且还可以继续
    WORD_MIDDLE_2 = 2
    # 是个词语的结尾，并且没有继续
    WORD_END_3 = 3



