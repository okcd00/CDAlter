# utils - 工具函数模块

全局工具函数和基础配置，为其他模块提供基础支持。

## 模块组成

| 文件 | 功能 | 主要类/函数 |
|------|------|------------|
| `__init__.py` | 模块初始化，全局路径配置 | `PROJECT_PATH` |
| `atc.py` | 数字转中文 (Arabic To Chinese) | `num2chinese()` |
| `pinyin_utils.py` | 拼音转换工具 | `PinyinUtils`, `Hz2PyUtils`, `Py2HzUtils` |

## 快速开始

### 数字转中文

```python
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
```

### 拼音转换

```python
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
corpus = pu.generate_parallel_corpus("金融市场：今日股价上升！")
```

## 依赖说明

| 依赖包 | 用途 | 安装命令 |
|--------|------|---------|
| `pypinyin` | 拼音转换 | `pip install pypinyin` |
| `Pinyin2Hanzi` | 拼音转汉字 | `pip install Pinyin2Hanzi` |
| `jieba` | 中文分词 | `pip install jieba` |
| `numpy` | 数值计算 | `pip install numpy` |

## API 参考

### atc.num2chinese()

```python
def num2chinese(
    num: Union[int, float, str],
    big: bool = False,      # 使用财务大写字符
    simp: bool = True,      # 使用简体中文
    o: bool = False,        # 使用"〇"表示零
    twoalt: bool = False    # 使用"两"代替"二"
) -> str
```

### PinyinUtils

```python
class PinyinUtils:
    def to_pinyin(word: str, method: str = 'lazy', **kwargs) -> List[str]
    def to_hanzi(pinyin_tuple: Tuple[str, ...], method: str = 'viterbi join') -> List[str]
    def get_homophones(word: str, n_candidates: int = 5) -> List[str]
    def segmentation(sentence: str, segmenter: str = 'jieba') -> List[str]
    def generate_parallel_corpus(sentence: str, n_position: int = 1, n_sample: int = 5) -> List[Dict]
```

## 重构说明

本次重构主要改进：

1. **编码统一**: 从 `gbk` 改为 `utf-8`
2. **类型注解**: 添加完整的类型提示
3. **文档字符串**: 添加详细的 docstring
4. **代码风格**: 符合 PEP 8 规范
5. **错误处理**: 改进异常提示

---

*重构时间: 2026-03-20*
*重构工具: QClaw Agent "晴"*
