# -*- coding: utf8 -*-
# ==========================================================================
#   Copyright (C) since 2020 All rights reserved.
#
#   filename : ReadEye.py
#   author   : chendian / okcd00@qq.com
#   date     : 2023-06-27
#   desc     : Read contents in some common kinds of files
# ==========================================================================
import os
from pathlib import Path

lines = [line.strip() for line in open('fileB.txt', 'r', encoding='UTF-8')]
rec_B = {}

for line in lines[1:]:
    items = [item.strip('"') for item in line.split('\t')]
    value = round(float(items[6]), 2)
    key = f"{items[1]}\t{value}\t{items[4]}"  # 资产名称、原值、入账日期
    rec_B[key] = [items[1], items[6], items[9]]

print(len(rec_B), len(lines)-1)


hit, total = 0, 0
with open('./result.txt', 'w', encoding='utf-8') as f:
    lines = [line.strip() for line in open('fileA.txt', 'r', encoding='UTF-8')]
    for line in lines[1:]:
        items = [item.strip('"') for item in line.split('\t')]
        value = round(float(items[6]), 2)
        key = f"{items[1]}\t{value}\t{items[4]}"  # 资产名称、原值、入账日期
        if key in rec_B:
            hit += 1
            """
            f.write(line)
            f.write('\t')
            f.write('\t')
            f.write(key)
            f.write('\t')
            f.write(items[-2])
            f.write('\n')
            """
        else:
            print(key)
            f.write(items[0])
            f.write('\t')
            f.write(key)
            f.write('\n')
        total += 1
    print(hit, total)