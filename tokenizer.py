#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
# 分词处理


class Tokenizer:
    def __init__(self):
        self.stop_words_list = [line.strip() for line in open('stopwords.txt', encoding='UTF-8').readlines()] + [' ']

    def show_stop_words(self):
        print(self.stop_words_list)

    # 带有位置信息的分词
    def cut_with_pos(self, text, lower=True):
        text_ = text
        if lower:
            text_ = text_.lower()
        seq = jieba.tokenize(text_, mode='search')
        return [w for w in seq if w[0] not in self.stop_words_list]

    def cut(self, text, lower=True):
        text_ = text
        if lower:
            text_ = text_.lower()
        seq = jieba.cut(text_)
        return [w for w in seq if w not in self.stop_words_list]

    def cuttest1(self):
        with open('test.txt', 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                for term in self.cut(line):
                    print(term[0])

    def cuttest2(self):
        query = '本项目涉及内容属于3D计算机视觉与深度学习的交叉领域。    项目基于双目视觉SFM（Structure from Motion）技术原理，利用当前先进的深度学习手段开展无监督SFM算法模块研究，主要包括：基于无监督学习的双目深度估计神经网络设计、从运动到结构的无监督神经网络设计、利用GPU计算平台加速算法实现等。本项目所涉及的技术，在自动驾驶、智能机器人、智能制造等领域有广阔的应用前景。'
        for term in self.cut(query):
            print(term)


if __name__ == '__main__':
    tokenizer = Tokenizer()
    tokenizer.show_stop_words()
    tokenizer.cuttest2()








