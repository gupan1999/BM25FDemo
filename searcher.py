#!/usr/bin/env python
# -*- coding: utf-8 -*-
from indexer import Indexer,Doc,Inverted
import pickle
import numpy as np
import time
# 检索模块


class Searcher:
    def __init__(self, index_path):
        self.bm25 = Bm25()
        self.ranked_doc_list = []
        self.index = None
        self.load_index(index_path)

    def load_index(self, path):
        with open(path, 'rb') as f:
            self.index = pickle.load(f)

    # BM25F打分 query_terms_idf:带有idf的查询词字典
    def score(self, query_terms_idf: dict, doc):
        b = self.bm25.b
        k1 = self.bm25.k1
        w_title = self.bm25.w_title
        w_content = self.bm25.w_content

        for qterm, qidf in query_terms_idf.items():
            if qterm not in doc.title_term_list and qterm not in doc.content_term_list:
                continue
            else:
                self.mark(qterm, doc)
                # 代入公式
                R = w_content * self.index.inverted[qterm][doc.doc_id].field_freq('content') / (
                        1 - b + b * doc.field_len('content') / self.index.avg_len_content) \
                        + w_title * self.index.inverted[qterm][doc.doc_id].field_freq('title') / (
                        1 - b + b * doc.field_len('title') / self.index.avg_len_title)
            doc.score += qidf * R / (R + k1)

    def search(self, query):
        start = time.time()
        # 查询词与索引词表取交集过滤
        query_terms = set(self.index.tokenizer.cut(query)).intersection(set(self.index.inverted))
        print(f'有效关键词: {query_terms}')
        if not query_terms:
            print('无有效关键词')
            return
        valid_terms_with_idf = {}
        # 预计算idf
        for qterm in query_terms:
            valid_terms_with_idf[qterm] = np.log(
                1 + (self.index.doc_num - self.index.freq(qterm) + 0.5) / (self.index.freq(qterm) + 0.5))
            print(f'{qterm}: {self.index.freq(qterm)}')

        for doc in self.index.id_doc.values():
            # str转list方便在指定位置插入高亮符号
            doc.tsl = list(doc.title_shown)
            doc.csl = list(doc.content_shown)
            self.score(valid_terms_with_idf, doc)
            if doc.score > 0:
                self.ranked_doc_list.append(doc)

        if not self.ranked_doc_list:
            print('找不到结果')
            return
        self.ranked_doc_list = sorted(self.ranked_doc_list, key=lambda d: d.score, reverse=True)
        self.highlight()
        print(f'{time.time()-start:.6f}s 检索完成，共{len(self.ranked_doc_list)}个结果')

    # 在指定位置插入高亮符号
    def mark(self, qterm, doc):
        if qterm in doc.title_term_list:
            for pos in self.index.inverted[qterm][doc.doc_id].title_positions:
                start, end = pos[0], pos[1]
                # print(f"title:{start} {end}")
                doc.tsl[start] = f'\033[34m{doc.tsl[start]}'
                doc.tsl[end-1] = f'{doc.tsl[end-1]}\033[0m'

        if qterm in doc.content_term_list:
            for pos in self.index.inverted[qterm][doc.doc_id].content_positions:
                start, end = pos[0], pos[1]
                # print(f"content:{start} {end}")
                doc.csl[start] = f'\033[34m{doc.csl[start]}'
                doc.csl[end-1] = f'{doc.csl[end-1]}\033[0m'

    def highlight(self):
        for doc in self.index.id_doc.values():
            doc.title_shown = ''.join(doc.tsl)
            doc.content_shown = ''.join(doc.csl)

    def show(self):
        for doc in self.ranked_doc_list:
            print(doc)


class Bm25:
    def __init__(self, b=0.75, k1=1.2, w_title=5, w_content=1):
        self.b = b
        self.k1 = k1
        self.w_title = w_title
        self.w_content = w_content


if __name__ == '__main__':
    searcher = Searcher(index_path='final')
    searcher.search('content1 数据')
    searcher.show()
