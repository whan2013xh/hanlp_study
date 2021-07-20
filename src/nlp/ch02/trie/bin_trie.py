# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-06
    FileName   : bin_trie.py
    Author     : Honghe
    Descreption: 二分字典树
"""
from pyhanlp import JClass
from base_node import Status, BaseNode
from Node import Node


def char_hash(str):
    """
    哈希函数，调用Java 字符哈希函数
    :param str:
    :param length:
    :return:
    """
    return abs((hash(str)))%(10**5)
    # return JClass('java.lang.Character')(str).hashCode()

class BinTrie(BaseNode):
    def __init__(self, map=None):
        self._size = 0
        # self._children = [BaseNode()] * (65535+1)
        self._children = [BaseNode()] * 100000
        self.status = Status.NOT_WORD_1
        if map:
            for key, value in map.items():
                self.put(key, value)

    def put(self, key, value):
        if len(key)==0:
            return
        branch = self
        for char in key[:-1]:
            branch.add_child(Node(char, Status.NOT_WORD_1, None))
            branch = branch.get_child(char)
        if branch.add_child(Node(key[-1], Status.WORD_END_3, value)):
            self._size += 1

    def __setitem__(self, key, value):
        self.put(key, value)

    def __getitem__(self, item):
        state = self
        for i, char in enumerate(item):
            if state is None:
                return None
            # 这个地方要理解一下，对于第一个字符是按hash获取到对应的node，然后后面是判断node的子树
            state = state.get_child(char)
        if state is None:
            return None
        if state.status != Status.WORD_END_3 and state.status != Status.WORD_MIDDLE_2:
            return None
        return state.value

    def __contains__(self, item):
        return self[item] is not None

    def remove(self, key):
        branch = self
        for char in key[:-1]:
            if branch is None:
                return
            branch = branch.get_child(char)
        if branch is None:
            return
        if branch.add_child(Node(key[-1], Status.UNDEFINED_0, None)):
            self._size -= 1

    def add_child(self, node):
        add = False
        key = node.get_key()
        hash_index = char_hash(key)
        target = self.get_child(hash_index)
        if target.status is None:
            self._children[hash_index] = node
            add = True
        else:
            if node.status == Status.UNDEFINED_0 and target.status != Status.NOT_WORD_1:
                target.status = Status.NOT_WORD_1
                add = True
            elif node.status == Status.NOT_WORD_1 and target.status == Status.WORD_END_3:
                target.status = Status.WORD_MIDDLE_2
            elif node.status == Status.WORD_END_3:
                if target.status == Status.NOT_WORD_1:
                    target.status = Status.WORD_MIDDLE_2
                if target.get_value() is None:
                    add = True
                target.set_value(node.get_value())
        return add

    def __sizeof__(self):
        return self._size

    def get_key(self):
        return 0

    def get_child(self, key):
        if isinstance(key, str):
            key = char_hash(key)
        return self._children[key]

    def parse_text(self, text):
        """
        前缀全切分
        :param text:
        :return:
        """
        length = len(text)
        begin = 0
        state = self
        res = []
        i=0

        while i<length:
            state = state.transition(text[i])
            if state is not None:
                value = state.get_value()
                if value is not None:
                    res.append(text[begin:i+1])
            else:
                i = begin
                begin += 1
                state = self
            i += 1
        return res

    def parse_longest_text(self, text):
        length = len(text)
        res = []
        i = 0
        state = self

        while i<length:
            state = state.transition(text[i])
            if state is not None:
                value = state.get_value()
                to = i+1
                end = to
                while to<length:
                    state = state.transition(text[end])
                    if state is not None:
                        end += 1
                    else:
                        res.append(text[i:end])
                        i = to
                        break









if __name__ == '__main__':
    trie = BinTrie()
    # add
    trie['自然'] = 'nature'
    trie['自然人'] = 'human'
    # trie['自然语言'] = 'language'
    # trie['自语'] = 'talk to oneself'
    # trie['入门'] = 'introduction'
    # print('自然' in trie)

    #delete
    trie.remove('自然')
    print('自然' in trie)
    #modify
    trie['自然语言处理'] = 'human language'