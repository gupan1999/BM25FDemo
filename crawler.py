#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import requests
import re
import time
import os
import traceback


# 信息采集
def project_crawler(begin=66, end=None, result_path='result_.txt', log_path='log_.txt'):
    reg1 = r'<title>(.*?)</title>.*?<br>.*?<div style=\"font-size:17px;line-height:25px\;\">(.*?)</div>'
    p1 = re.compile(reg1, re.S)
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r')as load:
                s = load.read()
                print(type(s))
                print(s)
                try:
                    if int(s) > begin:
                        index = int(s)
                    else:
                        print('begin')
                        index = begin
                except:
                    index = begin

        else:
            with open(log_path, 'w+')as f:
                index = begin
                print('创建日志')
        with open(result_path, 'ab+') as f:
            print(index)
            for index in range(index, end + 1):
                print(f'id: {index} ok')
                r = requests.get(f'https://win.bupt.edu.cn/program.do?id={index}', timeout=5)
                m = p1.findall(r.text)
                if m:
                    for it in m:
                        docid = f'2020{index}'
                        title = it[0].strip()
                        info = it[1].strip().replace('\r\n', '')
                        if info == '':
                            info = 'NULL'
                        line = (docid + '\t\t' + title + '\t\t' + info + '\n').encode('utf-8')
                        f.write(line)
                else:
                    print('匹配失败')
                time.sleep(2*(1+random.random()))
        with open(log_path, 'w+')as log:
            log.write('ok')
            print('采集完成')
    except:
        with open(log_path, 'w+')as log:
            log.write(str(index))
        traceback.print_exc()


def project_seek_crawler(begin=1, end=None, result_path='result.txt', log_path='log.txt'):
    reg = r'<a href=\"project.do\?next=collectproject&id=(\d+)\"\s*?>(.*?)</a>.*?<p>(.*?)</p>'
    p = re.compile(reg, re.S)
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r')as load:
                s = load.read()
                try:
                    if int(s) > begin:
                        index = int(s)
                    else:
                        index = begin
                except:
                    index = begin

        else:
            with open(log_path, 'w+')as f:
                index = begin
                print('创建日志')
        with open(result_path, 'ab+') as f:
            for index in range(index, end+1):
                print(f'第{index}页 ok')
                r = requests.get('https://win.bupt.edu.cn/project.do?next=collectlist&p=%d' % index, timeout=5)
                m = p.findall(r.text)
                if m:
                    for it in m:
                        docid = it[0].replace('<br/>', '').strip()
                        title = it[1].replace('<br/>', '').strip()
                        info = it[2].replace('<br/>', '').strip()
                        line = (docid+'\t\t'+title+'\t\t'+info+'\n').encode('utf-8')
                        f.write(line)

                else:
                    print('匹配失败')
                time.sleep(3*(1+random.random()))
        with open(log_path, 'w+')as log:
            log.write('ok')
            print('采集完成')
    except:
        with open(log_path, 'w+')as log:
            log.write(str(index))
        traceback.print_exc()


if __name__ == '__main__':
    project_crawler(begin=68, end=2450)
    # project_seek_crawler(25, 28)
