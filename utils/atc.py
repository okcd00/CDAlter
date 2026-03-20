# -*- coding: utf-8 -*-
"""
atc - 数字转中文工具 (Arabic To Chinese)

功能：
- 将阿拉伯数字转换为中文表示
- 支持简体/繁体中文
- 支持普通/大写（财务）字符
- 支持科学计数法之外的任意大小数字

使用示例：
    from utils.atc import num2chinese

    # 基本用法
    num2chinese(12345)           # "一万二千三百四十五"
    num2chinese(100000000)       # "一亿"

    # 大写（财务用）
    num2chinese(12345, big=True) # "壹万贰仟叁佰肆拾伍"

    # 繁体中文
    num2chinese(12345, simp=False)  # "一萬二千三百四十五"

    # 使用"两"代替"二"
    num2chinese(200, twoalt=True)   # "两百"

参数说明：
    num: 要转换的数字（int/float/str）
    big: 使用财务大写字符（壹贰叁...）
    simp: 使用简体中文（默认True）
    o: 使用"〇"代替"零"
    twoalt: 使用"两"代替"二"（在适当位置）

原作者：junzew (HanTTS)
许可证：WTFPL / Unlicense / CC0
"""

from __future__ import annotations
import itertools
from typing import Union


def num2chinese(
    num: Union[int, float, str],
    big: bool = False,
    simp: bool = True,
    o: bool = False,
    twoalt: bool = False
) -> str:
    """
    将阿拉伯数字转换为中文表示。

    Args:
        num: 要转换的数字，支持 int、float 或字符串形式
        big: 是否使用财务大写字符（壹贰叁肆伍陆柒捌玖）
        simp: 是否使用简体中文（默认 True）
        o: 是否使用"〇"表示零（正式场合）
        twoalt: 是否使用"两"代替"二"（如"两百"）

    Returns:
        中文数字字符串

    Raises:
        ValueError: 数字超出范围或使用科学计数法

    Examples:
        >>> num2chinese(12345)
        '一万二千三百四十五'
        >>> num2chinese(12345, big=True)
        '壹万贰仟叁佰肆拾伍'
    """
    # 检查数字有效性
    nd = str(num)
    if abs(float(nd)) >= 1e48:
        raise ValueError('number out of range')
    if 'e' in nd:
        raise ValueError('scientific notation is not supported')

    # 字符集定义
    c_symbol = '正负点' if simp else '正負點'
    if o:  # 正式场合
        twoalt = False

    if big:
        c_basic = '零壹贰叁肆伍陆柒捌玖' if simp else '零壹貳參肆伍陸柒捌玖'
        c_unit1 = '拾佰仟'
        c_twoalt = '贰' if simp else '貳'
    else:
        c_basic = '〇一二三四五六七八九' if o else '零一二三四五六七八九'
        c_unit1 = '十百千'
        c_twoalt = '两' if simp else '兩' if twoalt else '二'

    c_unit2 = '万亿兆京垓秭穰沟涧正载' if simp else '萬億兆京垓秭穰溝澗正載'

    def reversed_unique(s: str) -> str:
        """去除连续重复字符"""
        return ''.join(k for k, _ in itertools.groupby(reversed(s)))

    # 处理正负号
    result = []
    if nd[0] == '+':
        result.append(c_symbol[0])
    elif nd[0] == '-':
        result.append(c_symbol[1])

    # 分离整数和小数部分
    if '.' in nd:
        integer, remainder = nd.lstrip('+-').split('.')
    else:
        integer, remainder = nd.lstrip('+-'), None

    # 处理整数部分
    if int(integer):
        # 按4位一组分割
        splitted = [integer[max(i - 4, 0):i]
                    for i in range(len(integer), 0, -4)]
        intresult = []

        for nu, unit in enumerate(splitted):
            # 特殊情况处理
            if int(unit) == 0:  # 0000
                intresult.append(c_basic[0])
                continue
            elif nu > 0 and int(unit) == 2:  # 0002
                intresult.append(c_twoalt + c_unit2[nu - 1])
                continue

            ulist = []
            unit = unit.zfill(4)

            for nc, ch in enumerate(reversed(unit)):
                if ch == '0':
                    if ulist:
                        ulist.append(c_basic[0])
                elif nc == 0:
                    ulist.append(c_basic[int(ch)])
                elif nc == 1 and ch == '1' and unit[1] == '0':
                    # 特殊情况：十四, 三千零十四
                    ulist.append(c_unit1[0])
                elif nc > 1 and ch == '2':
                    ulist.append(c_twoalt + c_unit1[nc - 1])
                else:
                    ulist.append(c_basic[int(ch)] + c_unit1[nc - 1])

            ustr = reversed_unique(ulist)
            if nu == 0:
                intresult.append(ustr)
            else:
                intresult.append(ustr + c_unit2[nu - 1])

        result.append(reversed_unique(intresult).strip(c_basic[0]))
    else:
        result.append(c_basic[0])

    # 处理小数部分
    if remainder:
        result.append(c_symbol[2])
        result.append(''.join(c_basic[int(ch)] for ch in remainder))

    return ''.join(result)


__all__ = ['num2chinese']


if __name__ == '__main__':
    # 测试示例
    test_cases = [
        0, 1, 10, 12, 20, 100, 101, 110, 123, 1000, 1001,
        1234, 10000, 10001, 12345, 100000000, 123456789012
    ]

    print("=== 数字转中文测试 ===")
    for num in test_cases:
        print(f"{num:>15} -> {num2chinese(num)}")

    print("\n=== 大写（财务）形式 ===")
    for num in [1234, 5678, 10000]:
        print(f"{num:>6} -> {num2chinese(num, big=True)}")
