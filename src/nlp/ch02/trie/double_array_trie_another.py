# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-28
    FileName   : double_array_trie_another.py
    Author     : Honghe
    Descreption: 
"""

class TrieNode:
    def __init__(self, code, depth=0, is_leaf=False, label=None, value=-1):
        self.code = code
        self.is_leaf = is_leaf
        self.label = label
        self.value = value
        self.depth = depth
        self.child_node = {}

class HashTrie:


class DATrie:
    def __init__(self):
        self.ARRAY_SIZE = 655350
        self.BASE_ROOT = 1
        self.BASE_NULL = 0
        self.CHECK_ROOT = -1
        self.CHECK_NULL = -2
        self.base = []
        self.check = []

    def get_code(self, char):
        return ord(char)

    def transfer(self, start_state, offset):
        return abs(self.base[start_state].transfer_ratio)+offset

    def init(self):
        self.base = [TrieNode()]*self.ARRAY_SIZE
        self.check = [0]*self.ARRAY_SIZE

        for i in range(self.ARRAY_SIZE):
            node = TrieNode()
            node.transfer_ratio = self.BASE_NULL
            self.base[i] = node
            self.check[i] = self.CHECK_NULL
        root = TrieNode()
        root.transfer_ratio = self.BASE_ROOT
        self.base[0] = root
        self.check[0] = self.CHECK_ROOT

    def insert(self, start_state, offset, is_leaf, idx):
        """

        :param start_state:
        :param offset:
        :param is_leaf:
        :param idx:
        :return:
        """
        end_state = self.transfer(start_state, offset)
        if self.base[end_state].transfer_ratio!=self.BASE_NULL and self.check[end_state]!=start_state:
            # 找到空闲的位置
            while self.base[end_state].transfer_radio != self.BASE_NULL:
                end_state +=1
            self.base[start_state].transfer_radio = end_state-offset

        if is_leaf:
            self.base[end_state].transfer_radio = abs(self.base[start_state].transfer_ratio)*(-1)
            self.base[end_state].is_leaf = True
            self.base[end_state].value = idx
        elif self.base[end_state].transfer_radio == self.BASE_NULL:
            # 所有节点的初始base都是前一个节点的base
            self.base[end_state].transfer_radio = abs(self.base[start_state].transfer_ratio)
        # 设置check数组
        self.check[end_state] = start_state
        return self.base[end_state]

    def build(self, words):
        """
        构建双数组字典树，
        :param words:
        :return:
        """
        self.init()
        shut = False
        # 单词索引
        idx = 0
        while idx<len(words):
            start_state = 0
            #
            chars = words[idx]
            # 先遍历插入每个单词的第一个字符
            if not shut:
                node = self.insert(start_state, self.get_code(chars[0]), len(chars)==1, idx)
                node.label = chars[0]
            else:
                # 插入单词的其他字符，这个地方有问题，如果同一个前缀的不同单词会导致
                for j in range(1, len(chars)):
                    start_state = self.transfer(start_state, self.get_code(chars[j-1]))
                    node = self.insert(start_state, self.get_code(chars[j]), len(chars)==j+1, idx)
                    node.label = chars[j]

            if idx==len(words)-1 and not shut:
                idx = -1
                shut = True

            idx += 1
