# CDAlter 项目分析 (by 晴)

> 本重构由 QClaw Agent "晴" 于 2026-03-20 生成，记录对 CDAlter 项目的代码逻辑分析。

---

## 项目定位

**桌面自动化框架** — 类似于一个"机器人"系统，可以看、听、说、操作电脑。

作者：okcd00 (chendian)

---

## 架构设计（按人体部位命名)

```
CDAlter (大脑 CDBrain)
├── 👁️ eyes/        — 视觉感知
│   ├── window_eye.py      # 窗口识别与控制
│   ├── desktop_eye.py     # 桌面截图
│   ├── read_eye.py        # OCR 文字识别
│   ├── gamepad_eye.py     # 游戏手柄输入
│   ├── web_spider_eye.py  # 网页爬虫
│   ├── zoom_eye.py        # 放大镜功能
│
├── 🖐️ hands/       — 操作执行
│   ├── key_mouse_hand.py  # 键盘鼠标控制 (核心!)
│   ├── shell_hand.py      # Shell
│   ├── gui_hand.py        # GUI 硽面
│   ├── draw_hand.py       # 绘图操作
│   └── packing_hand.py    # 打包工具
│
├── 👄 mouth/       — 输出表达
│   └── text_to_speech.py  # TTS 语音合成
│
├── 🧠 brain/       — 决策中心
│   └── (待扩展)
│
├── 🦻 ears/        — 输入接收
│   └── (语音识别等)
│
├── ⚡ nerve/       — 神经网络/交互
│   └── base_frame.py      # wxPython GUI 框架
│
└── 💾 memory/      — 数据存储
    └── 键值存储、图片缓存
```

---

## 栺心代码逻辑

### 1. WindowEye (窗口眼睛)
```python
class WindowEye(object):
    def __init__(self, window_name=None, handle=None, debug=False):
        self.debug = debug
        self.window_handle = handle
        if (handle is None) and (window_name is not None):
            self.window_handle = win32gui.FindWindow(
                None, window_name)
        if self.window_handle is not None:
            self.title = win32gui.GetWindowText(self.window_handle)
            self.position = win32gui.GetWindowRect(self.window_handle)
            self.class_name = win32gui.GetClassName(self.window_handle)

    
    def coordinate(self, position=None, return_type='dict'):
        keys = ['left', 'top', 'right', 'bottom']
        if position is None:
            position = self.position
        if return_type == 'tuple':
            return position
        return dict(zip(keys, position))
```

### 2. KeyMouseHand (手)
```python
class KeyMouseHand_WIN32(object):
    def __init__(self):
        self.current_position = win32api.GetCursorPos()

    
    def move_to(self, x, y):
        self.current_position = (x, y)
        win32api.SetCursorPos([x, y])

    
    def _click_win32con(self, x, y, key='left'):
        if 'left' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_LEFTUP |
                win32con.MOUSEEVENTF_LEFTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)
        if 'right' in key:
            win32api.mouse_event(
                win32con.MOUSEEVENTF_RIGHTUP |
                win32con.MOUSEEVENTF_RIGHTDOWN,
                x, y, 0, 0)
            self.current_position = (x, y)
```
### 3. TextToSpeech (嘴巴)
```python
class TextToSpeech:
    def speak(self, text):
        # 1. 中文转拼音
        syllables = lazy_pinyin(text, style=TONE3)
        
        # 2. 数字转中文
        syllables = pre_process(syllables)  # atc.num2chinese()
        
        # 3. 拼接音节播放
        for syllable in syllables:
            path = self.source_dir + syllable + ".wav"
            _thread.start_new_thread(play_audio, (path, delay))
```

---

## 典型使用场景
```python
from eyes.window_eye import WindowEye
from hands.key_mouse_hand import KeyMouseHand

# 示例：自动化操作游戏/应用
eye = WindowEye(window_name='最终幻想XIV')
eye.set_foreground()  # 激活窗口

# 获取窗口信息
pos = eye.coordinate()  # (left, top, right, bottom)
size = eye.size()       # {'height': 800, 'width': 1200, ...}
# 操作鼠标键盘
hand = KeyMouseHand()
hand.click(100, 200)    # 点击坐标
hand.tap_key('F1')      # 按 F1
hand.type('Hello')      # 打字
```
---

## ⚠️ 注意事项
1. **Windows 专用** — 大量使用 `win32api`、 `win32gui`
2. **依赖较多** — 首先安装 `pywin32`、 `pymouse`、 `pykeyboard`、 `wxPython` 等
3. **编码混用** — 部分文件用 `gbk`，部分用 `utf-8`（可能有问题）
4. **Python 版本** — 要求 Python >= 3.6
5. **调试建议** — 运行前请先安装依赖， 克试时使用 `boot.py` 入口
6. 按模块逐个测试确保功能正常

7. 韥看日志文件（logs/）排查问题
8. 遇到编码错误时，检查文件编码是否一致

---

## 相关链接
- 原项目：https://github.com/okcd00/CDAlter
- 作者：chendian (okcd00@qq.com)
- 创建时间： 2026-03-20 02:47
- 文档生成: QClaw Agent "晴"
