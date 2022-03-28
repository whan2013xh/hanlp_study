# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-11-01
    FileName   : viterbi2.py
    Author     : Honghe
    Descreption: 
"""
import numpy as np


# 迭代过程，每次只需要记录第t个时间点 每个节点的最大概率即可，后续计算时直接使用前序节点的最大概率即可
def compute(obser, state, start_p, transition_p, emission_p):
    """
    维特比算法，回溯算法
    :param obser:
    :param state:
    :param start_p:
    :param transition_p:
    :param emission_p:
    :return:
    """
    # max_p 记录每个时间点每个状态的最大概率，i行j列，（i,j）记录第i个时间点 j隐藏状态的最大概率
    max_p = [[0 for col in range(len(state))] for row in range(len(obser))]
    # path 记录max_p 对应概率处的路径 i 行 j列 （i,j）记录第i个时间点 j隐藏状态最大概率的情况下 其前驱状态
    path = [[0 for col in range(len(state))] for row in range(len(obser))]
    # 初始状态(1状态)
    for i in range(len(state)):
        # max_p[0][i]表示初始状态第i个隐藏状态的最大概率
        # 概率 = start_p[i] * emission_p [state[i]][obser[0]]
        max_p[0][i] = start_p[i] * emission_p[state[i]][obser[0]]
        path[0][i] = i
    # 后续循环状态(2-t状态)
    # 此时max_p 中已记录第一个状态的两个隐藏状态概率
    for i in range(1, len(obser)):  # 循环t-1次，初始已计算
        max_item = [0 for i in range(len(state))]
        for j in range(len(state)):  # 循环隐藏状态数，计算当前状态每个隐藏状态的概率
            item = [0 for i in state]
            for k in range(len(state)):  # 再次循环隐藏状态数，计算选定隐藏状态的前驱状态为各种状态的概率
                p = max_p[i - 1][k] * emission_p[state[j]][obser[i]] * transition_p[state[k]][state[j]]
                # k即代表前驱状态 k或state[k]均为前驱状态
                item[state[k]] = p
            # 设置概率记录为最大情况
            max_item[state[j]] = max(item)
            # 记录最大情况路径(下面语句的作用：当前时刻下第j个状态概率最大时，记录其前驱节点)
            # item.index(max(item))寻找item的最大值索引，因item记录各种前驱情况的概率
            path[i][state[j]] = item.index(max(item))
        # 将单个状态的结果加入总列表max_p
        max_p[i] = max_item
    #newpath记录最后路径
    newpath = []
    #判断最后一个时刻哪个状态的概率最大
    p=max_p[len(obser)-1].index(max(max_p[len(obser)-1]))
    newpath.append(p)
    #从最后一个状态开始倒着寻找前驱节点
    for i in range(len(obser) - 1, 0, -1):
        newpath.append(path[i][p])
        p = path[i][p]
    newpath.reverse()
    return newpath


def compute2(obs, states, start_p, trans_p, emit_p):
    """
    维特比算法，非回溯算法
    :param obs:
    :param states:
    :param start_p:
    :param trans_p:
    :param emit_p:
    :return:
    """
    #   max_p（3*2）每一列存储第一列不同隐状态的最大概率
    max_p = np.zeros((len(obs), len(states)))

    #   path（2*3）每一行存储上max_p对应列的路径
    path = np.zeros((len(states), len(obs)))

    #   初始化
    for i in range(len(states)):
        max_p[0][i] = start_p[i] * emit_p[i][obs[0]]
        path[i][0] = i

    for t in range(1, len(obs)):
        newpath = np.zeros((len(states), len(obs)))
        for y in range(len(states)):
            prob = -1
            for y0 in range(len(states)):
                nprob = max_p[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]]
                if nprob > prob:
                    prob = nprob
                    state = y0
                    #   记录路径
                    max_p[t][y] = prob
                    for m in range(t):
                        newpath[y][m] = path[state][m]
                    newpath[y][t] = y

        path = newpath

    max_prob = -1
    path_state = 0
    #   返回最大概率的路径
    for y in range(len(states)):
        if max_p[len(obs)-1][y] > max_prob:
            max_prob = max_p[len(obs)-1][y]
            path_state = y

    return path[path_state]


def compute3(obs, states, start_p, trans_p, emit_p):
    """
    维特比算法：包含需要回溯和不需要回溯两种思路
    :param obs: 观察状态
    :param states:隐状态
    :param start_p:初始概率
    :param trans_p:转移概率
    :param emit_p:发射概率
    :return:
    """
    # max_p[i][j]表示观察状态为obs[j]，隐状态为states[i]时候的最大概率
    max_p=[[0 for _ in range(len(obs))] for _ in range(len(states))]
    # path1[i][j]表示观察状态为obs[j]，隐状态为states[i]时候的前驱状态，这个是用于回溯使用
    path1 = [[0 for _ in range(len(obs))] for _ in range(len(states))]
    # path2[i][j]表示观察状态为obs[j]，最后隐状态为states[i]的当前状态，path[i]对应的就是最佳路径，不需要回溯
    path2 = [[0 for _ in range(len(obs))] for _ in range(len(states))]

    #初始化第一个观察状态下的数值
    for i in range(len(states)):
        max_p[i][0] = start_p[i]*emit_p[i][0]
        path1[i][0] = states[i]
        path2[i][0] = states[i]

    # 计算从第二个观察状态之后得概率和路径
    for t in range(1,len(obs)):
        tmp_path = [[0 for _ in range(len(obs))] for _ in range(len(states))]
        for y in range(len(states)):
            tmp_item = [0 for _ in range(len(states))]
            for y0 in range(len(states)):
                tmp_item[y0] = max_p[y0][t-1]*trans_p[y0][y]*emit_p[y][t]
            max_p[y][t] = max(tmp_item)
            tmp_index = tmp_item.index(max(tmp_item))
            # 这个是前驱状态
            path1[y][t] = tmp_index
            tmp_path[y][:t] = path2[tmp_index][:t]
            # 这个是当前状态
            tmp_path[y][t] = y
        # 不回溯，每次都更新最佳的路径
        path2 = tmp_path

    max_index = max_p[:][-1].index(max(max_p[:][-1]))
    path = []
    path.append(max_index)
    for i in range(len(obs)-1,0,-1):
        p = path1[max_index][i]
        path.append(p)
        max_index = p
    return path.reverse(), path2[max_index]

if __name__ == '__main__':
    #   隐状态
    hidden_state = ['rainy', 'sunny']
    #   观测序列
    obsevition = ['walk', 'shop', 'clean']
    state_s = [0, 1]
    obser = [0, 1, 2]
    #   初始状态，测试集中，0.6概率观测序列以sunny开始
    start_probability = [0.6, 0.4]
    #   转移概率，0.7：sunny下一天sunny的概率
    transititon_probability = [[0.7, 0.3], [0.4, 0.6]]
    #   发射概率，0.4：sunny在0.4概率下为shop
    emission_probability = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]
    result = compute2(obser, state_s, start_probability, transititon_probability, emission_probability)
    for k in range(len(result)):
        print(hidden_state[int(result[k])])