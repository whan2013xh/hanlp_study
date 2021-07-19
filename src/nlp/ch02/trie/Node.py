# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-13
    FileName   : Node.py
    Author     : Honghe
    Descreption: 节点类
"""
import copy

from base_node import BaseNode, Status
from array_tool import ArrayTool

class Node(BaseNode):
    """
    字典树节点
    """
    def __init__(self, key=None, status=None, value=None):
        super().__init__(key, status, value)

    def add_child(self, node):
        add = False
        if not self._children:
            self._children = BaseNode()._children
        index = ArrayTool.binary_search(self._children, node)
        if index >= 0:
            target = self._children[index]
            if node.status==Status.UNDEFINED_0 and target.status != Status.NOT_WORD_1:
                target.status = Status.NOT_WORD_1
                target.value = None
                add = True
            elif node.status==Status.NOT_WORD_1 and target.status == Status.WORD_END_3:
                target.status = Status.WORD_MIDDLE_2
            elif node.status==Status.WORD_END_3:
                if target.status!=Status.WORD_END_3:
                    target.status = Status.WORD_MIDDLE_2
                if target.get_value() is None:
                    add = True
                target.set_value(node.get_value())
        else:
            insert = -(index + 1)
            self._children.insert(insert, node)
            add = True
        return add

    def get_child(self, key):
        if self._children is None:
            return None
        index = ArrayTool.binary_search(self._children, key)
        if index<0:
            return None
        return self._children[index]






if __name__ == '__main__':
    a = BaseNode()
    b = Node()
    print(a)