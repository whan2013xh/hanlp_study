# -*- coding: utf-8 -*-
"""
    CreatedDate: 2021-12-14
    FileName   : eval_bigram_cws.py
    Author     : Honghe
    Descreption: 
"""
from pyhanlp import *
from ngram_segment import train_bigram, load_bigram
import os

from src.nlp.tests.test_utility import ensure_data, test_data_path

sighan05 = ensure_data('icwb2-data', 'http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip')
msr_dict = os.path.join(sighan05, 'gold', 'msr_training_words.utf8')
msr_train = os.path.join(sighan05, 'training', 'msr_training.utf8')
msr_model = os.path.join(test_data_path(), 'msr_cws')
msr_test = os.path.join(sighan05, 'testing', 'msr_test.utf8')
msr_output = os.path.join(sighan05, 'testing', 'msr_bigram_output.txt')
msr_gold = os.path.join(sighan05, 'gold', 'msr_test_gold.utf8')

CWSEvaluator = SafeJClass('com.hankcs.hanlp.seg.common.CWSEvaluator')

if __name__ == '__main__':
    train_bigram(msr_train, msr_model)  # 训练
    segment = load_bigram(msr_model)  # 加载
    result = CWSEvaluator.evaluate(segment, msr_test, msr_output, msr_gold, msr_dict)  # 预测打分
    print(result)