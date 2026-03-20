# hands - 操作执行模块

本模块提供键盘鼠标控制、Shell命令执行、GUI操作等功能。

## 模块组成

| 文件 | 功能 | 主要类/函数 |
|------|------|------------|
| `key_mouse_hand.py` | 键盘鼠标控制 (核心) | `KeyMouseHand`, |
| `shell_hand.py` | Shell 命令执行 | `ShellHand` |
| `gui_hand.py` | GUI 自动化 (PyAutoGUI) | `PAGHand` |
| `draw_hand.py` | 绘图工具 (Turtle) | `DrawHand` |
| `packing_hand.py` | 程序打包工具 | `packing_with_pi()`, `packing_with_cx()` |
| `vk_codes.py` | 虚拟键码映射表 | `VK_CODE` |

## 快速开始

### 錮盘鼠标操作

```python
from hands.key_mouse_hand import KeyMouseHand

hand = KeyMouseHand()

# 鼠标操作
hand.click(100, 200)  # 点击坐标
hand.double_click(100, 200)  # 双击
hand.move_to(300, 400)  # 移动鼠标

hand.right_click()  # 右键点击
hand.middle_click()  # 中键点击
hand.scroll(100)  # 滚轮

# 键盘操作
hand.tap_key('a')  # 按键
hand.type('Hello World')  # 输入文字
hand.tap_comb('C', 'ctrl')  # Ctrl+C 组合键
hand.press_key(['ctrl', 'shift', 'a'])  # 复杂组合键
```

### GUI 自动化
```python
from hands.gui_hand import PAGHand

gui = PAGHand()

# 戍览器操作
gui.move_to(500, 300)
gui.click(200, 200)
gui.drag(100, 50)

gui.scroll(5)

# 截图查找
gui.locate_on_screen('button.png')  # 查找图片位置
gui.click_image('button.png')  # 点击图片
```

### Shell 命令
```python
from hands.shell_hand import ShellHand

shell = ShellHand()

# 执行命令
output = shell.run('dir')  # 列出目录内容
output = shell.run('echo hello')  # 输出 hello
output = shell.run('python script.py')  # 执行 Python 脚本
```

## 依赖说明
| 依赖包 | 用途 | 安装命令 |
|--------|------|---------|
| `pywin32` | Windows API | `pip install pywin32` |
| `pymouse` | 鼠标控制 | `pip install pymouse` |
| `pykeyboard` | 键盘控制 | `pip install pykeyboard` |
| `pynput` | 键盘监听 | `pip install pynput` |
| `pyautogui` | GUI 自动化 | `pip install pyautogui` |

## 重构说明

本次重构主要改进：
1. **编码统一**: 从 `gbk` 改为 `utf-8`
2. **类型注解**: 添加类型提示
3. **文档字符串**: 添加详细说明
4. **错误处理**: 改进异常提示

5. **代码复用**: 添加更多实用方法

---

*重构时间: 2026-03-20*
*重构工具: QClaw Agent "晴"*
