# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-11-01
    FileName   : viterb.py
    Author     : Honghe
    Descreption: 
"""
import numpy as np

state = np.array([[0.9, 0.1, 0.3],
         [0.1, 0.8, 0.4],
         [0.0, 0.1, 0.3]])
weight = np.array([[[0.1, 0.4, 0.5], [0.2, 0.7, 0.1], [0.9, 0.0, 0.1]],
          [[0.8, 0.1, 0.1], [0.4, 0.3, 0.3], [0.1, 0.2, 0.7]]])


def viterbi(state, weight):
    '''
    :param state: 状态矩阵
    :param weight: 权重矩阵
    :return:
    '''
    state = np.array(state)
    weight = np.array(weight)
    d, n = state.shape
    assert weight.shape == (n - 1, d, d), 'state not match path!'

    # 路径矩阵，元素值表示当前节点从前一层的那一个节点过来是最优的
    path = np.zeros(shape=(d, n))

    for i in range(n):
        print(f'进入第 {i} 层')
        if i == 0:
            path[:, i] = np.array(range(d)) + 1
            print('')
            continue

        for j in range(d):
            print(f'更新节点 ({j}, {i}) 的状态')
            temp = state[:, i - 1] * weight[i - 1, :, j]
            temp_max = max(temp)
            temp_index = np.where(temp == temp_max)
            path[j, i] = temp_index[0] + 1

            state[j, i] = max(temp) * state[j, i]
        print('')

    print(state)
    print(path)


def viterbi_decode(nodes, trans):
    """
    Viterbi算法求最优路径
    其中 nodes.shape=[seq_len, num_labels],
        trans.shape=[num_labels, num_labels].
    """
    # 获得输入状态序列的长度，以及观察标签的个数
    seq_len, num_labels = len(nodes), len(trans)
    # 简单起见，先不考虑发射概率，直接用起始0时刻的分数
    scores = nodes[0].reshape((-1, 1))

    paths = []
    # 递推求解上一时刻t-1到当前时刻t的最优
    for t in range(1, seq_len):
        # scores 表示起始0到t-1时刻的每个标签的最优分数
        scores_repeat = np.repeat(scores, num_labels, axis=1)
        # observe当前时刻t的每个标签的观测分数
        observe = nodes[t].reshape((1, -1))
        observe_repeat = np.repeat(observe, num_labels, axis=0)
        # 从t-1时刻到t时刻最优分数的计算，这里需要考虑转移分数trans
        M = scores_repeat + trans + observe_repeat
        # 寻找到t时刻的最优路径
        scores = np.max(M, axis=0).reshape((-1, 1))
        idxs = np.argmax(M, axis=0)
        # 路径保存
        paths.append(idxs.tolist())

    best_path = [0] * seq_len
    best_path[-1] = np.argmax(scores)
    # 最优路径回溯
    for i in range(seq_len - 2, -1, -1):
        idx = best_path[i + 1]
        best_path[i] = paths[i][idx]

    return best_path


if __name__ == '__main__':
    # viterbi(state, weight)
    viterbi_decode(state, weight)