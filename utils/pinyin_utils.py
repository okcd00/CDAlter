# -*- coding: utf-8 -*-
"""
pinyin_utils - 拼音转换工具

功能：
- 中文转拼音（多种风格）
- 拼音转中文（同音字生成）
- 分词与拼音处理
- 同音字替换与并行语料生成

依赖：
- pypinyin: 拼音转换
- Pinyin2Hanzi: 拼音转汉字
- jieba: 中文分词
- numpy: 数值计算

使用示例：
    from utils.pinyin_utils import PinyinUtils

    pu = PinyinUtils()

    # 中文转拼音
    pu.to_pinyin("你好")  # ['ni', 'hao']
    pu.to_pinyin("中国", style='tone')  # [['zhōng'], ['guó']]

    # 拼音转汉字
    pu.to_hanzi(('ni', 'hao'))  # ['你好', '泥号', ...]

    # 获取同音字
    pu.get_homophones("你好")  # ['你好', '泥号', '尼豪', ...]

    # 生成并行语料（用于训练/测试）
    pu.generate_parallel_corpus("金融市场：今日股价上升！")
"""

from __future__ import annotations
import os
from pathlib import Path
from typing import List, Tuple, Optional, Union, Dict, Any

import jieba
import pypinyin
import numpy as np

from Pinyin2Hanzi import DefaultHmmParams, DefaultDagParams
from Pinyin2Hanzi import dag as dag_algorithm
from Pinyin2Hanzi import viterbi as viterbi_algorithm


class Py2HzUtils:
    """
    拼音转汉字工具类

    使用 Viterbi 或 DAG 算法将拼音序列转换为可能的汉字序列。

    使用示例：
        py2hz = Py2HzUtils()
        results = py2hz.to_hanzi(('ni', 'hao'))
        # ['你好', '泥号', '尼豪', ...]
    """

    hmm_params = DefaultHmmParams()
    dag_params = DefaultDagParams()

    def __init__(self, default_candidate_counts: int = 5):
        """
        Args:
            default_candidate_counts: 默认候选词数量
        """
        self.default_candidate_counts = default_candidate_counts

    def _py2hz_algorithm(
        self,
        pinyin_tuple: Tuple[str, ...],
        path_num: int = 10,
        log_score: bool = True,
        method: str = 'viterbi'
    ) -> List[Any]:
        """
        内部方法：执行拼音转汉字算法

        Args:
            pinyin_tuple: 拼音元组
            path_num: 返回结果数量
            log_score: 是否返回对数分数
            method: 算法选择 ('viterbi' 或 'dag')

        Returns:
            转换结果列表
        """
        method_selection = {
            'viterbi': (viterbi_algorithm, {
                'hmm_params': self.hmm_params,
                'observations': pinyin_tuple,
                'path_num': path_num,
                'log': log_score,
            }),
            'dag': (dag_algorithm, {
                'dag_params': self.dag_params,
                'pinyin_list': pinyin_tuple,
                'path_num': path_num,
                'log': log_score
            })
        }

        method_key = method.split()[0]
        func, args = method_selection.get(method_key, (None, {}))

        if func is None:
            raise ValueError(f"Unknown method: {method}")

        return func(**args)

    def to_hanzi(
        self,
        pinyin_tuple: Tuple[str, ...],
        method: str = 'viterbi join',
        n_candidates: Optional[int] = None
    ) -> List[str]:
        """
        将拼音转换为汉字候选列表

        Args:
            pinyin_tuple: 拼音元组，如 ('ni', 'hao')
            method: 转换方法 ('viterbi', 'dag', 'viterbi join', 'dag join')
            n_candidates: 候选词数量

        Returns:
            汉字候选列表
        """
        if n_candidates is None:
            n_candidates = self.default_candidate_counts

        results = self._py2hz_algorithm(
            pinyin_tuple,
            path_num=n_candidates,
            method=method
        )

        if 'join' in method:
            results = [''.join(r.path) for r in results]

        return results

    def __call__(
        self,
        pinyin_tuple: Tuple[str, ...],
        method: str = 'viterbi join',
        n_candidates: Optional[int] = None
    ) -> List[str]:
        return self.to_hanzi(pinyin_tuple, method, n_candidates)


class Hz2PyUtils:
    """
    汉字转拼音工具类

    支持多种拼音输出风格，包括：
    - normal: 普通风格（无声调）
    - tone: 标准声调风格
    - tone2/tone3: 数字声调风格
    - initials: 声母风格
    - finals: 韵母风格
    - first_letter: 首字母风格

    使用示例：
        hz2py = Hz2PyUtils()
        hz2py.to_pinyin("中国")  # ['zhong', 'guo']
        hz2py.to_pinyin("中国", style='tone')  # [['zhōng'], ['guó']]
    """

    def __init__(self, separator: str = ' '):
        """
        Args:
            separator: slug 模式下的分隔符
        """
        self.separator = separator
        self.style_dict = self._get_style_dict()

    @staticmethod
    def _get_style_dict(
        extra_dict: Optional[Dict] = None,
        print_help: bool = False
    ) -> Dict[str, Tuple]:
        """
        获取拼音风格映射字典

        Args:
            extra_dict: 额外的风格映射
            print_help: 是否打印帮助信息

        Returns:
            风格映射字典
        """
        from pypinyin import Style

        ret = {
            'normal': (Style.NORMAL, '普通风格，不带声调。如： 中国 -> zhong guo'),
            'tone': (Style.TONE, '标准声调风格，拼音声调在韵母第一个字母上。如： 中国 -> zhōng guó'),
            'tone2': (Style.TONE2, '声调风格2，即拼音声调在各个韵母之后。如： 中国 -> zho1ng guo2'),
            'tone3': (Style.TONE3, '声调风格3，即拼音声调在各个拼音之后。如： 中国 -> zhong1 guo2'),
            'initials': (Style.INITIALS, '声母风格，只返回各个拼音的声母部分。如： 中国 -> zh g'),
            'first_letter': (Style.FIRST_LETTER, '首字母风格，只返回拼音的首字母部分。如： 中国 -> z g'),
            'finals': (Style.FINALS, '韵母风格，只返回各个拼音的韵母部分，不带声调。如： 中国 -> ong uo'),
            'finals_tone': (Style.FINALS_TONE, '标准韵母风格，带声调。如：中国 -> ōng uó'),
            'finals_tone2': (Style.FINALS_TONE2, '韵母风格2，带声调。如： 中国 -> o1ng uo2'),
            'finals_tone3': (Style.FINALS_TONE3, '韵母风格3，带声调。如： 中国 -> ong1 uo2'),
        }

        if extra_dict:
            ret.update(extra_dict)

        if print_help:
            for k, (_, description) in ret.items():
                print(f"{k}:\t{description}")

        return ret

    def _get_pinyin_style(self, _style: Union[str, int]) -> Union[int, Any]:
        """获取 pypinyin 风格常量"""
        if isinstance(_style, int):
            if 0 <= _style <= 13:
                return _style

        style_index, _ = self.style_dict.get(_style, (_style, ''))
        return style_index

    def _pinyin_detail(
        self,
        _word: str,
        _style: str = 'normal',
        _heteronym: bool = False,
        _errors: str = 'ignore',
        _strict: bool = False
    ) -> List[List[str]]:
        """详细拼音转换"""
        _style = self._get_pinyin_style(_style)
        return pypinyin.pinyin(
            hans=_word,
            style=_style,
            heteronym=_heteronym,
            errors=_errors,
            strict=True
        )

    def _lazy_pinyin_detail(
        self,
        _word: str,
        _style: str = 'normal'
    ) -> List[str]:
        """简化拼音转换（返回一维列表）"""
        _style = self._get_pinyin_style(_style)
        return pypinyin.lazy_pinyin(hans=_word, style=_style)

    def _slug_detail(
        self,
        _word: str,
        _separator: Optional[str] = None,
        _style: str = 'normal',
        _heteronym: bool = False,
        _errors: str = 'ignore',
        _strict: bool = False
    ) -> str:
        """Slug 格式拼音转换"""
        _style = self._get_pinyin_style(_style)
        if _separator is None:
            _separator = self.separator

        return pypinyin.slug(
            hans=_word,
            style=_style,
            separator=_separator,
            heteronym=_heteronym,
            errors=_errors,
            strict=True
        )

    @staticmethod
    def style_register(style_func=None, style_name=None):
        """注册自定义拼音风格"""
        from pypinyin.style import register

        def cd_style(pinyin, **kwargs):
            return pinyin

        if style_func is None:
            style_func = cd_style
        if style_name is None:
            style_name = style_func.__name__

        register(style_name, style_func)

    @staticmethod
    def update_pinyin_dict(py_dict: Dict, style: str = 'default'):
        """更新拼音字典"""
        sample_value = next(iter(py_dict.values()))

        if isinstance(sample_value, list):
            pypinyin.load_phrases_dict(py_dict, style=style)
        else:
            pypinyin.load_single_dict(py_dict, style=style)

    def to_pinyin(
        self,
        word: str,
        method: str = 'lazy',
        **kwargs
    ) -> Union[List[str], List[List[str]], str]:
        """
        将中文转换为拼音

        Args:
            word: 中文文本
            method: 转换方法
                - 'lazy': 返回简化列表 ['zhong', 'guo']
                - 'slug': 返回分隔字符串 'zhong guo'
                - 其他: 返回详细列表 [['zhōng'], ['guó']]
            **kwargs: 其他参数
                - style: 拼音风格
                - heteronym: 是否返回多音字
                - errors: 错误处理方式
                - strict: 是否严格模式

        Returns:
            拼音结果
        """
        _style = kwargs.get('style', 'normal')
        _heteronym = kwargs.get('heteronym', False)

        if method == 'lazy':
            return self._lazy_pinyin_detail(_word=word, _style=_style)
        elif method == 'slug':
            return self._slug_detail(
                _word=word,
                _style=_style,
                _heteronym=_heteronym,
                _errors=kwargs.get('errors', 'ignore'),
                _strict=kwargs.get('strict', False)
            )
        else:
            return self._pinyin_detail(
                _word=word,
                _style=_style,
                _heteronym=_heteronym,
                _errors=kwargs.get('errors', 'ignore'),
                _strict=kwargs.get('strict', False)
            )

    def __call__(self, **kwargs):
        return self.to_pinyin(**kwargs)


class PinyinUtils:
    """
    拼音工具主类

    整合拼音-汉字双向转换功能，提供：
    - 中文转拼音
    - 拼音转汉字
    - 同音字获取
    - 并行语料生成

    使用示例：
        pu = PinyinUtils()

        # 基本转换
        pu.to_pinyin("你好")  # ['ni', 'hao']
        pu.to_hanzi(('ni', 'hao'))  # ['你好', '泥号', ...]

        # 同音字
        pu.get_homophones("你好")  # ['你好', '泥号', ...]

        # 并行语料生成
        corpus = pu.generate_parallel_corpus("今日天气很好")
    """

    def __init__(self):
        self.ph_utils = Py2HzUtils()
        self.hp_utils = Hz2PyUtils()
        self.custom_dict = 'my_custom_dictionary.txt'

        # 快捷方法引用
        self.to_hanzi = self.ph_utils.to_hanzi
        self.to_pinyin = self.hp_utils.to_pinyin

    def load_custom_dictionary(self, dic_path: Optional[str] = None):
        """加载自定义词典"""
        if dic_path is None or not os.path.exists(dic_path):
            dic_path = self.custom_dict
        jieba.load_userdict(dic_path)

    @staticmethod
    def segmentation(
        sentence: str,
        segmenter: Optional[str] = 'jieba'
    ) -> List[str]:
        """
        中文分词

        Args:
            sentence: 待分词句子
            segmenter: 分词器 ('jieba' 或 None)

        Returns:
            分词结果列表
        """
        if segmenter is None:
            return list(sentence)
        elif segmenter in [True, 'jieba']:
            return jieba.lcut(sentence)
        else:
            return list(sentence)

    @staticmethod
    def sentence_pinyin(sent: str) -> List[str]:
        """句子转拼音（忽略非中文字符）"""
        return pypinyin.lazy_pinyin(
            sent,
            errors=lambda item: [c for c in item]
        )

    def to_pinyin_list(
        self,
        sentence: str,
        segmenter: Optional[str] = None
    ) -> List[List[str]]:
        """将句子转换为拼音列表"""
        if segmenter is not None:
            token_list = self.segmentation(sentence, segmenter=segmenter)
        else:
            token_list = list(sentence)

        return [self.to_pinyin(tok) for tok in token_list]

    def get_homophones(
        self,
        word: str,
        n_candidates: int = 5,
        heteronym: bool = False
    ) -> List[str]:
        """
        获取同音字候选

        Args:
            word: 输入词语
            n_candidates: 候选词数量
            heteronym: 是否考虑多音字

        Returns:
            同音字候选列表
        """
        def _bfs_crawl(nodes: List) -> List[Tuple]:
            """BFS 遍历所有拼音组合"""
            cur_idx, queue = 0, [[-1, ()]]
            while cur_idx < len(nodes):
                head_idx, head_tuple = queue.pop(0)
                for py in nodes[cur_idx]:
                    cur_tuple = (*head_tuple, py)
                    queue.append([cur_idx, cur_tuple])
                if cur_idx - queue[0][0] < 1:
                    cur_idx += 1
            return [item[1] for item in queue]

        pinyin_case = self.to_pinyin(word, method='custom', heteronym=heteronym)
        pinyin_candidates = _bfs_crawl(pinyin_case)

        hanzi_candidates = []
        for word_pinyin in pinyin_candidates:
            if len(word_pinyin) == 1:
                cur_case = self.to_hanzi(
                    pinyin_tuple=word_pinyin, method='viterbi')
            else:
                cur_case = self.to_hanzi(
                    pinyin_tuple=word_pinyin, method='dag')
            hanzi_candidates.extend(cur_case)

        hanzi_candidates.sort(key=lambda x: -x.score)

        ret = []
        for hc in hanzi_candidates:
            if len(ret) == n_candidates:
                break
            cur_candidate = ''.join(hc.path)
            if cur_candidate not in ret:
                ret.append(cur_candidate)

        return ret

    def _random_modify(
        self,
        sentence: Union[str, List[str]],
        mask: Optional[np.ndarray] = None,
        n_position: int = 1,
        n_sample: int = 5,
        heteronym: bool = True
    ) -> Tuple[List[List[str]], np.ndarray]:
        """内部方法：随机替换同音字"""
        if isinstance(sentence, str):
            sentence = list(sentence)

        if mask is None:
            mask = np.ones(len(sentence), dtype=np.int32)
        elif isinstance(mask, list):
            mask = np.array(mask)

        assert len(sentence) == mask.shape[0]

        def check_valid_token(token: str) -> bool:
            py_str = self.to_pinyin(token, method='slug', errors=lambda p: '$')
            return '$' not in py_str

        mask = mask * np.array(
            list(map(check_valid_token, sentence)),
            dtype=np.int32
        )

        available_index = np.argwhere(mask).reshape(-1)
        selected_index = np.random.choice(
            available_index, size=n_position, replace=False
        )

        selected_token = [sentence[i] for i in selected_index]
        candidates = [
            self.get_homophones(tok, n_candidates=n_sample, heteronym=heteronym)
            for tok in selected_token
        ]

        ret = []
        for _ in range(n_sample):
            cur_sample = list(sentence)
            for idx, can in zip(selected_index, candidates):
                cur_sample[idx] = np.random.choice(can)
            ret.append(cur_sample)

        return ret, selected_index

    def random_modify(
        self,
        sentence: str,
        mask: Optional[np.ndarray] = None,
        segmenter: Optional[str] = None,
        n_position: int = 1,
        n_sample: int = 5,
        heteronym: bool = True,
        de_duplication: bool = True
    ) -> Tuple[List[List[str]], np.ndarray]:
        """
        随机替换同音字生成变体

        Args:
            sentence: 输入句子
            mask: 替换位置掩码
            segmenter: 分词器
            n_position: 替换位置数量
            n_sample: 生成样本数量
            heteronym: 是否考虑多音字
            de_duplication: 是否去重

        Returns:
            (变体列表, 替换位置)
        """
        if segmenter:
            tokens = self.segmentation(sentence, segmenter=segmenter)
            py_list = self.to_pinyin_list(tokens, segmenter=None)
            mask = [0 if '$' in tok else 1 for tok in py_list]
        else:
            tokens = list(sentence)

        sample_list, selected_index = self._random_modify(
            sentence=tokens,
            mask=mask,
            n_position=n_position,
            n_sample=n_sample,
            heteronym=heteronym
        )

        if de_duplication:
            samples, records = [], []
            for sample in sample_list:
                feature = ''.join(sample)
                if feature not in records:
                    samples.append(sample)
                    records.append(feature)
            sample_list = samples

        return sample_list, selected_index

    def generate_parallel_corpus(
        self,
        sentence: str,
        n_position: int = 1,
        n_sample: int = 5,
        segmenter: str = 'jieba'
    ) -> List[Dict[str, Any]]:
        """
        生成并行语料（用于训练/测试）

        Args:
            sentence: 输入句子
            n_position: 替换位置数量
            n_sample: 生成样本数量
            segmenter: 分词器

        Returns:
            语料字典列表，每个包含：
            - original_tokens: 原始分词
            - faulty_tokens: 替换后分词
            - faulty_mask: 替换位置掩码
            - cell_len: 长度
        """
        original_tokens = self.segmentation(sentence, segmenter=segmenter)
        candidates, selected_index = self.random_modify(
            sentence=original_tokens,
            n_position=n_position,
            n_sample=n_sample
        )

        def item_formatter(
            faulty_tokens: List[str],
            is_modified_sign: int = 1
        ) -> Dict[str, Any]:
            cell_len = len(faulty_tokens)
            faulty_mask = np.zeros(cell_len, dtype=np.int32)
            for idx in selected_index:
                faulty_mask[idx] = is_modified_sign

            return {
                'original_tokens': original_tokens,
                'faulty_tokens': faulty_tokens,
                'faulty_mask': faulty_mask,
                'cell_len': cell_len,
            }

        return [item_formatter(can) for can in candidates]

    def __call__(self, *args, **kwargs):
        pass


__all__ = ['Py2HzUtils', 'Hz2PyUtils', 'PinyinUtils']


if __name__ == '__main__':
    pu = PinyinUtils()

    print("=== 拼音转换测试 ===")
    print(pu.to_pinyin("你好世界"))

    print("\n=== 拼音转汉字测试 ===")
    print(pu.to_hanzi(('ni', 'hao')))

    print("\n=== 同音字测试 ===")
    print(pu.get_homophones("你好"))

    print("\n=== 并行语料生成测试 ===")
    corpus = pu.generate_parallel_corpus(
        sentence='金融市场：今日股价上升！',
        n_position=2,
        n_sample=5
    )
    for item in corpus:
        print(item)
