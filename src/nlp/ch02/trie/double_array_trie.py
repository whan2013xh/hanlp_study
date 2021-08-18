# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-07-22
    FileName   : double_array_trie.py
    Author     : Honghe
    Descreption: 双数组字典树
"""
import copy

class Node:
    def __init__(self, code=None, depth=None, left=None, right=None, char=None):
        """
        节点
        :param code:字符对应的编码，这里是ASCII码
        :param depth:节点所在层数
        :param left: 记录左边最近的单词索引
        :param right: 记录右边最近单词索引
        """
        self.code = code
        self.depth = depth
        self.left = left
        self.right = right

        # 方便查看结果
        self.char = char


class DoubleArrayTrie:
    def __init__(self, dic=None):
        self.BUF_SIZE = 16384
        self.UNIT_SIZE = 8
        self.check = []
        self.base = []
        self.size = 0
        self.alloc_size = 0
        # key数组维护的是插入的单词
        self.key = []
        self.key_size = 0
        # length数组维护的是每个单词对应的长度，
        self.length = []
        #
        self.value = []
        # ？
        self.v = []
        self.progress = 0
        # 寻找下一个check[i]=0的起始点，i=next_check_pos
        self.next_check_pos = 0
        self.error_ = 0
        self.node_list = []
        if dic is not None:
            self.build(list(dic.keys()), len(dic.keys()), None, None)

    def resize(self, new_size):
        self.check += [0] * (new_size - self.alloc_size)
        self.base += [0] * (new_size - self.alloc_size)
        self.alloc_size = new_size

    def fetch(self, parent, siblings):
        """
        获取相连的子节点，dfs
        :param parent: 父节点
        :param siblings: 兄弟节点
        :return: parent下的子节点
        """
        if self.error_ < 0:
            return 0
        prev = 0
        left_child = parent.left
        # 这个循环是指遍历所有子节点，看哪些节点是子节点
        while left_child < parent.right:
            # 对应词语所在层
            cur_depth = self.length[left_child] if self.length else len(self.key[left_child])
            # 对于单词结尾插入的\0，这个条件成立，同是也会跳出循环
            if cur_depth < parent.depth:
                left_child += 1
                continue

            tmp = self.key[left_child]
            cur = 0
            if cur_depth != parent.depth:
                cur = ord(tmp[parent.depth]) + 1

            # 这个是为了确认插入的数据是字典序
            # 如果不是字典序就会直接失败
            # 这个维持字典序是为了保障检索速度
            if prev > cur:
                self.error_ = -3
                return 0

            # 不同前缀，或者是第一个子节点
            if cur != prev or len(siblings) == 0:
                tmp_node = Node()
                tmp_node.depth = parent.depth + 1
                tmp_node.code = cur
                # 修改左指针
                tmp_node.left = left_child
                tmp_node.char = tmp[parent.depth] if parent.depth<len(tmp) else "\0"
                # 修改上一个子节点的右指针
                if len(siblings) != 0:
                    siblings[-1].right = left_child
                siblings.append(tmp_node)
            prev = cur
            left_child += 1
        # 修改最后一个子节点的右指针
        if len(siblings) != 0:
            siblings[-1].right = parent.right

            self.node_list.append(copy.deepcopy(siblings))
        return len(siblings)

    def insert(self, siblings, used):
        """
        插入节点，这个是双数组字典树的核心函数，完成了树构建的核心逻辑：
        1、找到check[begin+a1...an]==0的n个空闲空间,
        父节点 b, 子节点列表[a1...an],找到一片空间能让
        check[base[b]+a1]=0,
        然后再赋值check[base[b]+a1]=base[b].
        2、dfs计算对应的base数组，
        如果节点有子节点，递归执行insert，一直到单词结束，确定每一次层的base值
        base值的选择一般是从0开始从小到大，同时保持base的唯一性，需要一个表来记录哪些值已经使用了
        :param siblings:等待插入的兄弟节点
        :param used: 为了保证base数组的唯一性，当对应数字使用后就再找下一个
        :return: 插入的偏移位置，返回的不是绝对的插入的索引位置，而是距离对应的code的相对位置
        """
        if self.error_ < 0:
            return 0
        begin = 0
        pos = max(siblings[0].code + 1, self.next_check_pos) - 1
        nonzero_num = 0
        first = 0

        if self.alloc_size <= pos:
            self.resize(pos + 1)
        # 该循环目标找到base[begin+a1...an]==0的n个空闲空间, a1...an是siblings中的节点
        while 1:
            pos += 1
            if self.alloc_size <= pos:
                self.resize(pos + 1)

            if self.check[pos] != 0:
                nonzero_num += 1
                continue
            elif first == 0:
                self.next_check_pos = pos
                first = 1
            # 当前位置离第一个兄弟节点的距离
            begin = pos - siblings[0].code
            # 如果分配的空间不够放入an元素则扩容
            if self.alloc_size <= (begin + siblings[-1].code):
                self.resize(begin + siblings[-1].code + siblings[-1].code)
            # 如果这个begin对应的数字已经使用，就再次寻找
            if used.get(begin, False):
                continue
            # n个空间不都是空闲的那就再次重新找
            continue_flag = False
            for i in range(1, len(siblings)):
                if self.check[begin + siblings[i].code] != 0:
                    continue_flag = True
                    break
            if continue_flag:
                continue
            else:
                break

        # 从next_check_pos开始到POS之间，如果已占用的空间到95%以上，下次插入节点时，之间从POS开始查找
        if 1 * nonzero_num / (pos - self.next_check_pos + 1) >= 0.95:
            self.next_check_pos = pos

        used[begin] = True
        self.size = max(self.size, begin + siblings[-1].code + 1)
        # 赋值check数组，这里begin就是对于base[parent]
        for i in range(len(siblings)):
            self.check[begin + siblings[i].code] = begin

        for i in range(len(siblings)):
            new_siblings = []
            # 一个词的终止且不为其他词的前缀，fetch返回0就代表没有子节点了
            if self.fetch(siblings[i], new_siblings) == 0:
                # 设置\0结尾的节点对应的base值，对应的绝对值就是这个词所在的索引位置
                # 其实如果value为空的话，就是一直是-siblings[i].left - 1
                self.base[begin + siblings[i].code] = (-self.value[siblings[i].code.left] - 1) if self.value else (
                            -siblings[i].left - 1)
                if self.value and (-self.value[siblings[i].left] - 1)>=0:
                    self.error_ = -2
                    return 0
                self.progress+=1
            else:
                h = self.insert(new_siblings, used)
                self.base[begin+siblings[i].code] = h
        return begin

    def build(self, _key, _key_size, _length=None, _value=None):
        """
        双数组字典树构建
        :param _key: 字典的key，也就是汉字单词，必须是字典序
        :param _key_size: len(_key),词典单词书
        :param _length: 每个key的长度
        :param _value: 每个key对应的value
        :return:
        """
        if not _key or _key_size>len(_key):
            return 0

        self.key = _key
        self.length = _length
        self.key_size = _key_size
        self.value = _value
        self.progress = 0
        self.alloc_size = 0
        # 初始化数组长度
        self.resize(65536 * 32)
        self.base[0] = 1
        self.next_check_pos = 0
        # 创建根节点
        root_node = Node()
        root_node.left = 0
        root_node.right = _key_size
        root_node.depth = 0

        siblings = []
        self.node_list.append([root_node])
        self.fetch(root_node, siblings)
        self.insert(siblings, {})

        self.key = None
        self.length = None
        return self.error_

    def get_dat(self):
        return [(index, i, self.check[index]) for index,i in enumerate(self.base) if i!=0]

    def get_node_list(self):
        return {index: [(node.char, node.code, node.depth, node.left, node.right) for node in nodes] for index, nodes in enumerate(self.node_list)}


if __name__ == '__main__':
    keys = ["入门","自然","自然人","自然语言处理","自语"]
    dic = {
        "入门":"introduction",
        "自然":"nature",

        "自然人":"human",
        "自然语言处理": "language",
        "自语":"talk	to oneself"
    }
    dat = DoubleArrayTrie(dic)
    res = dat.get_dat()
    node_res = dat.get_node_list()
    for i in res:
        print(i)
    print("===")
    for key,value in node_res.items():
        print(key, value)




