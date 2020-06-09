#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from tokenizer import Tokenizer
import time
#  建立索引


class Indexer:

    def __init__(self, file_path, index_path):
        self.id_doc = {}    # 文档集合
        self.inverted = {}      # 倒排索引字典
        self.doc_num = 0
        self.avg_len_title = 0
        self.avg_len_content = 0
        self.tokenizer = Tokenizer()
        self.index_path = index_path
        self.init_doc(file_path)

    # 读取文本初始化
    def init_doc(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                id, title, info = line.strip().split('\t\t')
                doc = Doc(doc_id=id, content=info, title=title)
                self.id_doc[id] = doc

            self.doc_num = len(self.id_doc)  # 文档总数

    def index(self):
        # 逐文档逐域扫描
        for doc in self.id_doc.values():
            content_term_info = self.tokenizer.cut_with_pos(doc.content)
            title_term_info = self.tokenizer.cut_with_pos(doc.title)
            for term_info in title_term_info:
                term, start, end = term_info[0], term_info[1], term_info[2]
                doc.title_term_list.append(term)
                # 已出现过的词
                if term in self.inverted:
                    # 未记录过的文档id
                    if doc.doc_id not in self.inverted[term]:
                        inverted = Inverted()
                        inverted.add_title_pos(start, end)
                        self.inverted[term][doc.doc_id] = inverted
                    else:
                        # 在已有对象添加位置信息
                        self.inverted[term][doc.doc_id].add_title_pos(start, end)
                # 新词
                else:
                    inverted = Inverted()
                    inverted.add_title_pos(start, end)
                    self.inverted[term] = {doc.doc_id: inverted}

            for term_info in content_term_info:
                term, start, end = term_info[0], term_info[1], term_info[2]
                doc.content_term_list.append(term)
                if term in self.inverted:
                    if doc.doc_id not in self.inverted[term]:
                        inverted = Inverted()
                        inverted.add_content_pos(start, end)
                        self.inverted[term][doc.doc_id] = inverted
                    else:
                        self.inverted[term][doc.doc_id].add_content_pos(start, end)
                else:
                    inverted = Inverted()
                    inverted.add_content_pos(start, end)
                    self.inverted[term] = {doc.doc_id: inverted}

            self.avg_len_content += len(doc.content_term_list)
            self.avg_len_title += len(doc.title_term_list)
        self.avg_len_title /= self.doc_num     # 平均标题长度
        self.avg_len_content /= self.doc_num    # 平均内容长度
        # print(self.avg_len_title)
        # print(self.avg_len_content)
        print('词汇数:%d' % len(self.inverted))
        pickle.dump(self, open(self.index_path, 'wb'))

    # 词出现的文档数
    def freq(self, term):
        return len(self.inverted[term])


# 倒排索引项
class Inverted:
    def __init__(self):
        # 存各域中查询词出现的位置
        self.title_positions = []
        self.content_positions = []

    # # 词在整个文档中出现的次数
    # def __len__(self):
    #     return len(self.title_positions + self.content_positions)

    def add_title_pos(self, start, end):
        self.title_positions.append([start, end])

    def add_content_pos(self, start, end):
        self.content_positions.append([start, end])

    # 词在文档的标题或内容中出现的次数
    def field_freq(self, field_name):
        if field_name == 'title':
            return len(self.title_positions)
        else:
            return len(self.content_positions)


# 文档对象
class Doc:
    def __init__(self, doc_id, title, content=None):
        self.title = title
        self.doc_id = doc_id
        self.title_shown = title
        self.content_shown = content
        self.content = content
        self.content_term_list = []
        self.title_term_list = []
        self.score = 0

    # 文档长度(按词表长度计算)
    def __len__(self):
        return len(self.content_term_list+self.title_term_list)

    # 打印格式
    def __str__(self):
        return 'id:{}\t\t{}\t\tscore:{}\n{}'.format(self.doc_id, self.title_shown, self.score, self.content_shown)

    # 域(即标题或内容的长度)
    def field_len(self, field_name):
        if field_name == 'title':
            return len(self.title_term_list)
        else:
            return len(self.content_term_list)

    # 清除搜索时的打分和高亮文本
    def reset(self):
        self.content_shown = self.content
        self.title_shown = self.title
        self.score = 0


if __name__ == '__main__':
    print('开始建立索引')
    start = time.time()
    # indexer = Indexer('test.txt', 'test')
    indexer = Indexer('final.txt', 'final')
    indexer.index()
    print(f'{time.time()-start:.6f}s 索引建立完成')
