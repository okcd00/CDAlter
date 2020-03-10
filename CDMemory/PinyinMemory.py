# coding: utf-8
# ==========================================================================
#   Copyright (C) 2020 All rights reserved.
#
#   filename : PinyinMemory.py
#   author   : chendian / okcd00@qq.com
#   date     : 2020-03-02
#   desc     : Utils for Pinyin and Hanzi with pypinyin and Pinyin2Hanzi packages
#              Used for transferring between pinyin and sentences
# ==========================================================================
import os
import jieba
import pypinyin
import numpy as np
from Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag as dag_algorithm
from Pinyin2Hanzi import viterbi as viterbi_algorithm


class Py2HzUtils(object):
    hmm_params = DefaultHmmParams()
    dag_params = DefaultDagParams()

    def __init__(self):
        self.default_candidate_counts = 5

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

    def __call__(self, pinyin_tuple, method='viterbi join', n_candidates=None):
        return self.to_hanzi(
            pinyin_tuple, method=method, n_candidates=n_candidates)


class Hz2PyUtils(object):
    def __init__(self):
        self.separator = ' '
        self.style_dict = self._get_style_dict()

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
        style_index, style_description = self.style_dict.get(_style, _style)
        return style_index

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
        ret = pypinyin.lazy_pinyin(
            hans=_word, style=_style)
        return ret

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
    def update_pinyin_dict(py_dict, style='default'):
        sample_key, sample_value = py_dict.items()[0]
        if isinstance(sample_value, list):
            # phrases_dict (dict) – 词语拼音库。比如： {u"阿爸": [[u"ā"], [u"bà"]]}
            # style – phrases_dict 参数值的拼音库风格. 支持 ‘default’, ‘tone2’
            pypinyin.load_phrases_dict(py_dict, style=style)
        else:
            # pinyin_dict (dict) – 单字拼音库。比如： {0x963F: u"ā,ē"}
            # style – pinyin_dict 参数值的拼音库风格. 支持 ‘default’, ‘tone2’
            pypinyin.load_single_dict(py_dict, style=style)

    def to_pinyin(self, word, method='lazy', **kwargs):
        # get parameters from kwargs
        _style = self._get_pinyin_style(
            _style=kwargs.get('style', 'normal'))
        _heteronym = kwargs.get('heteronym', False)

        # apply functions
        if method == 'lazy':
            ret = self._lazy_pinyin_detail(
                _word=word, _style=_style)
        elif method == 'slug':
            ret = self._slug_detail(
                _word=word, _style=_style, _heteronym=_heteronym,
                _errors=kwargs.get('errors', 'ignore'),
                _strict=kwargs.get('strict', 'ignore'))
        else:  # 'custom' parameters for high-level developers
            ret = self._pinyin_detail(
                _word=word, _style=_style, _heteronym=_heteronym,
                _errors=kwargs.get('errors', 'ignore'),
                _strict=kwargs.get('strict', 'ignore'))
        return ret

    def __call__(self, **kwargs):
        return self.to_pinyin(**kwargs)


class PinyinUtils(object):
    ph_utils = Py2HzUtils()
    hp_utils = Hz2PyUtils()

    def __init__(self):
        self.to_hanzi = self.ph_utils.to_hanzi
        self.to_pinyin = self.hp_utils.to_pinyin
        self.custom_dict = 'my_custom_dictionary.txt'

    def load_custom_dictionary(self, dic_path=None):
        if (dic_path is None) or (not os.path.exists(dic_path)):
            dic_path = self.custom_dict
        # load a dict for jieba as default
        jieba.load_userdict(dic_path)

    @staticmethod
    def segmentation(sentence, segmenter='jieba'):
        if segmenter is None:
            return sentence  # do nothing
        elif segmenter in [True, 'jieba']:
            segmenter = jieba.lcut  # return a list as jieba.cut
        elif segmenter in ['others']:
            # others such as pyltp can be added
            pass
        tokens = segmenter(sentence)
        return tokens

    def to_pinyin_list(self, sentence, segmenter=None):
        if segmenter is not None:
            token_list = self.segmentation(sentence, segmenter=segmenter)
        else:  # char-wise as default
            token_list = [tok for tok in sentence]
        return list(map(self.to_pinyin, token_list))

    def get_homophones(self, word, n_candidates=5, heteronym=False):
        def _bfs_crawl(nodes):
            cur_idx, _queue = 0, [[-1, ()]]
            while cur_idx < nodes.__len__():
                head_idx, head_tuple = _queue.pop(0)
                for _py in nodes[cur_idx]:
                    cur_tuple = (*head_tuple, _py)
                    _queue.append([cur_idx, cur_tuple])
                # go to the next index
                if cur_idx - _queue[0][0] < 1:
                    cur_idx += 1
            return list(map(lambda x: x[1], _queue))

        pinyin_case = self.to_pinyin(
            word, method='custom',
            heteronym=heteronym)
        pinyin_candidates = _bfs_crawl(pinyin_case)
        # print('pinyin candidates:', pinyin_candidates)
        hanzi_candidates = []
        for word_pinyin in pinyin_candidates:
            # print('->', word_pinyin)
            if word_pinyin.__len__() == 1:
                cur_case = self.to_hanzi(
                    pinyin_tuple=word_pinyin, method='viterbi')
            else:  # char search -> word search
                cur_case = self.to_hanzi(
                    pinyin_tuple=word_pinyin, method='dag')
            hanzi_candidates.extend(cur_case)
        hanzi_candidates.sort(key=lambda x: -x.score)
        ret = []
        for hc in hanzi_candidates:
            if ret.__len__() == n_candidates:
                break  # early stop
            cur_candidate = ''.join(hc.path)
            if cur_candidate not in ret:
                ret.append(cur_candidate)
        return ret

    def _random_modify(self, sentence, mask=None,
                       n_position=1, n_sample=5, heteronym=True):
        if isinstance(mask, list):
            mask = np.array(mask)
        if mask is None:
            mask = np.ones(sentence.__len__(), dtype=np.int32)
        assert sentence.__len__() == mask.shape[0]

        def check_valid_token(_token):
            py_str = self.to_pinyin(
                _token, method='slug', errors=lambda _p: '$')
            return '$' not in py_str

        mask = mask * np.array(
            list(map(check_valid_token, sentence)),
            dtype=np.int32)
        # print(mask)
        allow_repeat = False
        available_index = np.argwhere(mask).reshape(-1)
        selected_index = np.random.choice(
            available_index, size=n_position, replace=allow_repeat)
        selected_token = list(map(lambda x: sentence[x], selected_index))
        # print(list(zip(selected_index, selected_token)))
        candidates = []
        for token in selected_token:
            hp = self.get_homophones(
                token, n_candidates=n_sample, heteronym=heteronym)
            # print(hp)
            candidates.append(hp)
        # print(list(zip(selected_index, candidates)))
        ret = []
        for _ in range(n_sample):
            cur_sample = [tok for tok in sentence]
            for index, can in zip(selected_index, candidates):
                cur_sample[index] = np.random.choice(can)
            ret.append(cur_sample)
        return ret, selected_index

    def random_modify(self, sentence, mask=None, segmenter=None,
                      n_position=1, n_sample=5, heteronym=True, de_duplication=True):
        if segmenter:
            tokens = self.segmentation(
                sentence=sentence, segmenter=segmenter)
            # print(tokens)
            py_list = self.to_pinyin_list(tokens, segmenter=None)
            mask = [0 if '$' in tok else 1 for tok in py_list]
        else:  # char-wise or token-wise from sentence
            tokens = [tok for tok in sentence]
        sample_list, selected_index = self._random_modify(
            sentence=tokens, mask=mask,
            n_position=n_position, n_sample=n_sample, heteronym=heteronym)
        if de_duplication:
            samples, records = [], []
            for sample in sample_list:
                feature = ''.join(sample)
                if feature not in records:
                    samples.append(sample)
                    records.append(feature)
            sample_list = samples
        return sample_list, selected_index

    def generate_parallel_corpus(self, sentence, n_position=1, n_sample=5, segmenter='jieba'):
        original_tokens = self.segmentation(sentence, segmenter=segmenter)
        candidates, selected_index = self.random_modify(
            sentence=original_tokens,
            n_position=n_position,
            n_sample=n_sample)

        def item_formatter(faulty_tokens, is_modified_sign=1):
            cell_len = faulty_tokens.__len__()
            faulty_mask = np.zeros(cell_len, dtype=np.int32)
            for ind in selected_index:
                faulty_mask[ind] = is_modified_sign
            _item = {}
            _item.update({'original_tokens': original_tokens})
            _item.update({'faulty_tokens': faulty_tokens})
            _item.update({'faulty_mask': faulty_mask})
            _item.update({'cell_len': cell_len})
            return _item
        return [item_formatter(can) for can in candidates]

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pu = PinyinUtils()
    ret_sentences = pu.generate_parallel_corpus(
        sentence='金融市场：今日股价上升！',
        n_position=2, n_sample=5, segmenter=jieba.lcut)
    for r in ret_sentences:
        print(r)

