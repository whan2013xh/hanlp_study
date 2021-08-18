# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-22
    FileName   : double_array_trie_other.py
    Author     : Honghe
    Descreption: 
"""
import numpy as np


class Node:
    def __init__(self, node_name, parent_node=None, path_to_this=None):
        self.node_name = node_name
        self.children_node_map = None
        self.parent_node = parent_node
        self.is_leaf = False
        self.path_to_this = path_to_this

    def if_leaf(self):
        return self.is_leaf

    def set_as_leaf(self):
        self.is_leaf = True

    def add_children_node(self, a_node):
        if self.children_node_map is None:
            self.children_node_map = {}

        self.children_node_map[a_node.node_name] = a_node

class TrieHashMap:
    def __init__(self):
        self.root_node = Node("root")

    def add_item(self, element_list):
        cur = self.root_node
        parent_path = ""
        for element in element_list:
            if cur.children_node_map is None or element not in cur.children_node_map:
                new_node = Node(element)
                cur.add_children_node(new_node)
            cur = cur.children_node_map.get(element)
            parent_path += element
        print("这个模式的末尾节点是：" , cur.node_name)
        cur.set_as_leaf()

    def contains_key(self, element_list):
        cur = self.root_node
        for element in element_list:
            if element not in cur.children_node_map:
                return False
            cur = cur.children_node_map.get(element)

        if cur.if_leaf():
            return True
        else:
            return False

    def get_children_node_name(self, parent_path):
        cur = self.root_node
        for element in parent_path:
            if element not in cur.children_node_map:
                return False
            cur = cur.children_node_map.get(element)

        if cur.if_leaf():
            return False
        else:
            return list(cur.children_node_map.keys())

    def get_children_nodes(self, parent_path):
        cur = self.root_node
        for element in parent_path:
            if element not in cur.children_node_map:
                return False
            cur = cur.children_node_map.get(element)

        if cur.children_node_map is None:
            return False
        else:
            return cur.children_node_map

class HaskMapTriePuls(TrieHashMap):
    def __init__(self, max_word_len):
        self.root_node = Node("", None)
        self.nodes_list = [[] for k in range(max_word_len)]
        self.max_word_len = max_word_len

    def add_item(self, element_list):
        cur = self.root_node
        path_to_this = ""
        for depth in range(len(element_list)):
            element = element_list[depth]
            path_to_this += element
            if cur.children_node_map is None or element not in cur.children_node_map:
                new_node = Node(element, cur, path_to_this=path_to_this)
                cur.add_children_node(new_node)
                self.nodes_list[depth].append(new_node)
            cur = cur.children_node_map[element]
        cur.set_as_leaf()

    def get_path(self, node):
        return node.path_to_this

    def print_all(self):
        for i in range(self.max_word_len):
            nodes_this_depth = self.nodes_list[i]
            for node in nodes_this_depth:
                print(node.node_name, node.if_leaf(), end=' ')
            print()


class DoubleArrayTrie:
    def __init__(self, max_word_len):
        self.base = [1]
        self.check = [0]
        self.size = 1
        self.max_ascii_id = 0
        self.min_ascii_id = 0
        self.max_word_len = max_word_len
        self.hash_trie = HaskMapTriePuls(max_word_len)

    def build(self, item_list):
        self.iter_patterns_first(item_list)
        former_status = 0
        for node in self.hash_trie.nodes_list[0]:
            index = self.base[former_status] + ord(node.node_name)
            self.base[index] = -1 if node.if_leaf() else 1
            self.check[index] = former_status
        print("完成对第一层的初始化")
        for i in range(self.max_word_len):
            print(i, "这一层的节点个数是： ", len(self.hash_trie.nodes_list[i]))
            nodes_this_depth = self.hash_trie.nodes_list[i]
            for node in nodes_this_depth:
                path_to_this_node = self.hash_trie.get_path(node)
                former_status = 0
                former_status = self.update_stage1(former_status, path_to_this_node)
                self.update(former_status, path_to_this_node, node)

        indexes = list(range(len(self.base)))
        data = [indexes, self.base, self.check]
        for i in indexes:
            if self.base[i]!=0:
                print(i, self.base[i], self.check[i])
        # data = [self.base, self.check]
        # data = np.array(data)
        # print(np.where(data!=0))
        # idx = np.argwhere(np.all(data[..., :] == 0, axis=0))
        # data2 = np.delete(data, idx, axis=1)
        # print(data2)

    def iter_patterns_first(self, item_list):
        for item in item_list:
            self.hash_trie.add_item(item)

            for char in item:
                if ord(char)>self.max_ascii_id:
                    self.max_ascii_id = ord(char)
                if ord(char)<self.min_ascii_id:
                    self.min_ascii_id = ord(char)
        print(f"最大的ASCII码是： {self.max_ascii_id}, 最小的是：{self.min_ascii_id}")
        self.resize(self.max_ascii_id)
        for item in item_list:
            self.hash_trie.add_item(item)

    def update_stage1(self, former_status, parent_path):
        if former_status<0:
            former_status = -former_status
        former_base = 0
        for a_char in parent_path:
            former_base = self.base[former_status]
            if former_base < 0:
                former_base = -former_base
            current_status = former_base + ord(a_char)
            former_status = current_status
        return former_status

    def update(self, former_status, parent_path, node):
        """
        考察与node同源的节点情况
        :param former_status:
        :param parent_path:
        :param node:
        :return:
        """
        delta = abs(self.base[former_status])
        children_nodes = self.hash_trie.get_children_nodes(parent_path)
        while children_nodes!=False:
            if_clean = True
            for b_char in children_nodes.keys():
                b_index = delta + ord(b_char)
                if b_index >= self.size:
                    self.resize(b_index)
                if self.base[b_index] !=0:
                    if_clean = False
                    break
            if if_clean:
                break
            delta += 1
        self.base[former_status] = -delta if self.base[former_status]<0 else delta

        if children_nodes!=False:
            for b_char in children_nodes.keys():
                b_index = delta + ord(b_char)
                self.base[b_index] = -1 if children_nodes[b_char].if_leaf() else 1
                self.check[b_index] = former_status

    def resize(self, new_size):
        """
        线性扩容
        :param new_size:
        :return:
        """
        self.base += [0]*(new_size - len(self.base) + 10000)
        self.check += [0]*(new_size - len(self.check) + 10000)
        self.size = len(self.check)

    def contains_key(self, item):
        start_status = 0
        for a_char in item:
            former_base = self.base[start_status]
            new_index = abs(former_base) + ord(a_char)
            print(a_char, start_status, self.check[new_index])
            if self.check[new_index] == start_status:
                start_status = new_index
                continue
            else:
                return False
        print("判断是否是叶子节点：", new_index, self.base[new_index])
        return self.base[new_index]<0

if __name__ == '__main__':
    item_list = ['入门','自然', '自然人','自然语言','自语']
    max_length = 100
    double_array_trie = DoubleArrayTrie(max_length)
    double_array_trie.build(item_list)
    print(double_array_trie.contains_key("入门"))
