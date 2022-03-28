# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-10-25
    FileName   : ngram_segment.py
    Author     : Honghe
    Descreption: 
"""
from jpype import JString

from pyhanlp import *

from src.nlp.tests.test_utility import test_data_path

WordNet = JClass('com.hankcs.hanlp.seg.common.WordNet')
Vertex = JClass('com.hankcs.hanlp.seg.common.Vertex')
CoreDictionary = LazyLoadingJClass('com.hankcs.hanlp.dictionary.CoreDictionary')
CorpusLoader = SafeJClass("com.hankcs.hanlp.corpus.document.CorpusLoader")
NatureDictionaryMaker = SafeJClass('com.hankcs.hanlp.corpus.dictionary.NatureDictionaryMaker')
ViterbiSegment = JClass('com.hankcs.hanlp.seg.Viterbi.ViterbiSegment')
DijkstraSegment = JClass('com.hankcs.hanlp.seg.Dijkstra.DijkstraSegment')


def my_cws_corpus(data_root=None):
    data_root = test_data_path() if data_root is None else data_root
    corpus_path = os.path.join(data_root, 'my_cws_corpus.txt')
    if not os.path.isfile(corpus_path):
        with open(corpus_path, 'w', encoding='utf-8') as out:
            out.write('''商品 和 服务
商品 和服 物美价廉
服务 和 货币''')
    return corpus_path

def train_bigram(corpus_path, model_path):
    sents = CorpusLoader.convert2SentenceList(corpus_path)
    for sent in sents:
        for word in sent:
            if word.label is None:
                word.setLabel("n")
    maker = NatureDictionaryMaker()
    maker.compute(sents)
    maker.saveTxtTo(model_path)

def load_bigram(model_path, verbose=True, ret_viterbi=True):
    HanLP.Config.CoreDictionaryPath = model_path +".txt"
    HanLP.Config.BiGramDictionaryPath = model_path + ".ngram.txt"
    # 以下部分为兼容新标注集，不感兴趣可以跳过
    HanLP.Config.CoreDictionaryTransformMatrixDictionaryPath = model_path + ".tr.txt"  # 词性转移矩阵，分词时可忽略
    CoreBiGramTableDictionary = SafeJClass('com.hankcs.hanlp.dictionary.CoreBiGramTableDictionary')
    CoreDictionary.getTermFrequency("商品")
    if verbose:
        print(CoreDictionary.getTermFrequency("商品"))
        print(CoreBiGramTableDictionary.getBiFrequency("商品", "和"))
        sent = '商品和服务'
        # sent = '货币和服务'
        wordnet = generate_wordnet(sent, CoreDictionary.trie)
        print(wordnet)
        print(viterbi(wordnet))
    return ViterbiSegment().enableAllNamedEntityRecognize(False).enableCustomDictionary(
        False) if ret_viterbi else DijkstraSegment().enableAllNamedEntityRecognize(False).enableCustomDictionary(False)


def generate_wordnet(sent, trie):
    """
    生成词网
    :param sent: 句子
    :param trie: 词典
    :return:
    """
    searcher = trie.getSearcher(JString(sent), 0)
    wordnet = WordNet(sent)
    while searcher.next():
        wordnet.add(searcher.begin + 1, Vertex(sent[searcher.begin:searcher.begin+searcher.length], searcher.value, searcher.index))

    vertexes = wordnet.getVertexes()
    i = 0
    while i<len(vertexes):
        # 如果是空行
        print(len(vertexes[i]))
        if len(vertexes[i])==0:
            j = i+1
            # 寻找第一个非空行
            for j in range(i+1, len(vertexes)-1):
                if len(vertexes[j]):
                    break
            # 填充[i,j)之间的空行
            wordnet.add(i, Vertex.newPunctuationInstance(sent[i-1:j-1]))
            i = j
        else:
            i += len(vertexes[i][-1].realWord)
    return wordnet

def viterbi(wordnet):
    nodes = wordnet.getVertexes()
    for i in range(0,len(nodes)-1):
        for node in nodes[i]:
            for to in nodes[i+len(node.realWord)]:
                to.updateFrom(node)

    path = []
    f = nodes[len(nodes)-1].getFirst()
    while f:
        path.insert(0,f)
        f = f.getFrom()
    return [v.realWord for v in path]

if __name__ == '__main__':
    sent = "商品和服务"
    # trie = CoreDictionary.trie
    # res = generate_wordnet(sent,trie)
    # vi_res = viterbi(res)
    #
    # print(res)
    # print(vi_res)


    root_path = "models"
    corpus_path = my_cws_corpus(root_path)
    # corpus_path = os.path.join(root_path, 'my_cws_corpus.txt')
    model_path = os.path.join(root_path, 'my_cws_model')
    # train_bigram(corpus_path, model_path)
    load_bigram(model_path)
