# coding: utf-8
# ==========================================================================
#   Copyright (C) 2018 All rights reserved.
#
#   filename : PinyinMemory.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-03-02
#   desc     : Utils for Pinyin and Hanzi with pypinyin and Pinyin2Hanzi packages
#              Used for transferring between pinyin and sentences
# ==========================================================================
from Pinyin2Hanzi import dag as dag_algorithm
from Pinyin2Hanzi import viterbi as viterbi_algorithm
from Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi import DefaultDagParams
import pypinyin


class PinyinUtils(object):
    hmm_params = DefaultHmmParams()
    dag_params = DefaultDagParams()

    def __init__(self):
        self.separator = ' '
        self.default_candidate_counts = 5
        self.style_dict = self._get_style_dict()
        pass

    def _py2hz_algorithm(self, pinyin_tuple, path_num=10, log_score=True, method='viterbi'):
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
        method = method.split()[0]
        func, args = method_selection.get(method, {})
        results = func(**args)
        return results

    def to_hanzi(self, pinyin_tuple, method='viterbi join', n_candidates=None):
        if n_candidates is None:
            n_candidates = self.default_candidate_counts
        results = self._py2hz_algorithm(
            pinyin_tuple,
            path_num=n_candidates,
            method=method)
        if 'join' in method:
            results = list(map(
                lambda x: ''.join(x.path),
                results))
        return results

    @staticmethod
    def style_register(style_func=None, style_name=None):
        from pypinyin.style import register

        def cd_style(pinyin, **kwargs):
            print(kwargs.items())
            return pinyin

        if style_func is None:  # example
            style_func = cd_style
        if style_name is None:
            # style_name = 'cd_style'
            style_name = style_func.__name__
        register(style_name, style_func)

    @staticmethod
    def _get_style_dict(extra_dict=None, print_help=False):
        from pypinyin import Style
        ret = {
            'normal':   (Style.NORMAL,
                         '普通风格，不带声调。如： 中国 -> zhong guo'),
            'tone':     (Style.TONE,
                         '标准声调风格，拼音声调在韵母第一个字母上（默认风格）。如： 中国 -> zhōng guó'),
            'tone1':    (Style.TONE,
                         '标准声调风格，拼音声调在韵母第一个字母上（默认风格）。如： 中国 -> zhōng guó'),
            'tone2':    (Style.TONE2,
                         '声调风格2，即拼音声调在各个韵母之后，用数字 [1-4] 进行表示。如： 中国 -> zho1ng guo2'),
            'tone3':    (Style.TONE3,
                         '声调风格3，即拼音声调在各个拼音之后，用数字 [1-4] 进行表示。如： 中国 -> zhong1 guo2'),
            'initials': (Style.INITIALS,
                         '声母风格，只返回各个拼音的声母部分（注：有的拼音没有声母，详见 #27）。如： 中国 -> zh g'),
            'first_letter': (Style.FIRST_LETTER,
                             '首字母风格，只返回拼音的首字母部分。如： 中国 -> z g'),
            'finals':       (Style.FINALS,
                             '韵母风格，只返回各个拼音的韵母部分，不带声调。如： 中国 -> ong uo'),
            'finals_tone':  (Style.FINALS_TONE,
                             '标准韵母风格，带声调，声调在韵母第一个字母上。如：中国 -> ōng uó'),
            'finals_tone1': (Style.FINALS_TONE,
                             '标准韵母风格，带声调，声调在韵母第一个字母上。如：中国 -> ōng uó'),
            'finals_tone2': (Style.FINALS_TONE2,
                             '韵母风格2，带声调，声调在各个韵母之后，用数字 [1-4] 进行表示。如： 中国 -> o1ng uo2'),
            'finals_tone3': (Style.FINALS_TONE3,
                             '韵母风格3，带声调，声调在各个拼音之后，用数字 [1-4] 进行表示。如： 中国 -> ong1 uo2'),
        }
        if extra_dict:
            ret = ret.update(extra_dict)
        if print_help:
            for k, (style, description) in ret.items():
                print("{}:\t{}".format(k, description))
        return ret

    def _get_pinyin_style(self, _style):
        if isinstance(_style, int):
            if 0 <= _style <= 13:
                return _style
        return self.style_dict.get(_style, _style)

    def update_pinyin_dict(self, py_dict, style='default'):
        sample_key, sample_value = py_dict.items()[0]
        if isinstance(sample_value, list):
            # phrases_dict (dict) – 词语拼音库。比如： {u"阿爸": [[u"ā"], [u"bà"]]}
            # style – phrases_dict 参数值的拼音库风格. 支持 ‘default’, ‘tone2’
            pypinyin.load_phrases_dict(py_dict, style=style)
        else:
            # pinyin_dict (dict) – 单字拼音库。比如： {0x963F: u"ā,ē"}
            # style – pinyin_dict 参数值的拼音库风格. 支持 ‘default’, ‘tone2’
            pypinyin.load_single_dict(py_dict, style=style)

    def _pinyin_detail(self, _word,
                       _style='normal', _heteronym=False,
                       _errors='ignore', _strict=False):
        _style = self._get_pinyin_style(_style)
        ret = pypinyin.pinyin(
            hans=_word, style=_style,
            heteronym=_heteronym,
            errors=_errors,
            strict=True)
        return ret

    def _lazy_pinyin_detail(self, _word, _style='normal'):
        _style = self._get_pinyin_style(_style)
        return pypinyin.lazy_pinyin(hans=_word, style=_style)

    def _slug_detail(self, _word, _separator=None,
                       _style='normal', _heteronym=False,
                       _errors='ignore', _strict=False):
        _style = self._get_pinyin_style(_style)
        if _separator is None:
            _separator = self.separator
        ret = pypinyin.slug(
            hans=_word, style=_style,
            separator=_separator,
            heteronym=_heteronym,
            errors=_errors,
            strict=True)
        return ret

    def _to_pinyin(self, _word, _method='lazy', **kwargs):
        if _method == 'lazy':
            ret = self._lazy_pinyin_detail(
                _word=_word, _style='normal')
        elif _method == 'slug':
            ret = self._slug_detail(
                _word=_word, _style='normal')
        else:  # custom parameters for high-level developers
            ret = self._pinyin_detail(
                _word=_word, **kwargs)
        return ret

    def to_pinyin(self, text, method='lazy', **kwargs):
        return self._to_pinyin(
            _word=text, _method=method, **kwargs)

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pu = PinyinUtils()
    print(pu.to_pinyin(u'我的苹果', method='custom'))
