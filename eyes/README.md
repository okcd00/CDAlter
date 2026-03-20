# eyes - 视觉感知模块

提供屏幕捕获、窗口识别、OCR识别等视觉功能。

## 模块组成

| 文件 | 功能 | 主要类/函数 |
|------|------|------------|
| `window_eye.py` | 窗口识别与控制 | `WindowEye` |
| `desktop_eye.py` | 桌面截图捕获 | `DesktopEye` |
| `read_eye.py` | 文件读取工具 | `ReadEye` |
| `visual_residue.py` | 视觉记忆（截图缓存）| `see_and_remember()` |
| `zoom_eye.py` | 局部放大镜 | `ZoomEye` |
| `web_spider_eye.py` | 网页爬虫 | `SpiderEye` |
| `web_spider_eye_selenium.py` | Selenium 爬虫 | - |
| `excel_eye.py` | Excel 文件处理 | - |
| `gamepad_eye.py` | 游戏手柄输入 | - |

## 快速开始

### 窗口控制

```python
from eyes.window_eye import WindowEye

# 通过名称获取窗口
eye = WindowEye(window_name='记事本')
print(eye.coordinate())  # (left, top, right, bottom)

# 激活窗口
eye.set_foreground()

# 获取窗口信息
print(eye.size())
print(eye.get_child_windows())
```

### 桌面截图

```python
from eyes.desktop_eye import DesktopEye

desktop = DesktopEye()

# 全屏截图
desktop.screenshot()

# 按窗口名截图
desktop.capture('记事本')

# 列出所有窗口
desktop.show_all_hwnd()
```

### 文件读取

```python
from eyes.read_eye import ReadEye

reader = ReadEye()

# 读取 JSON 文件
data = reader.read('data.json')

# 读取目录下的所有文件
files = reader.read('./data_dir')
```

## 系统要求

- **操作系统**: Windows
- **依赖**: pywin32 >= 220, Pillow

## API 参考

### WindowEye

```python
class WindowEye:
    def __init__(self, window_name: str = None, handle: int = None)
    def coordinate(self) -> Dict[str, int]    # 获取窗口坐标
    def size(self) -> Dict[str, int]          # 获取窗口尺寸
    def set_foreground(self) -> None          # 激活窗口
    def appear(self) -> None                  # 显示窗口
    def minimize(self) -> None                # 最小化
    def maximize(self) -> None                # 最大化
    def close(self) -> None                   # 关闭窗口
    def get_child_windows(self) -> List[int]  # 获取子窗口
```

### DesktopEye

```python
class DesktopEye:
    def screenshot(self, save_dir: str = None) -> str    # 全屏截图
    def capture(self, name_or_handle) -> str             # 窗口截图
    def capture_by_name(self, window_name: str) -> str   # 按名称截图
    def capture_by_handle(self, handle: int) -> str      # 按句柄截图
    def show_all_hwnd(self) -> Dict[int, str]            # 列出所有窗口
```

### ReadEye

```python
class ReadEye:
    def read(self, file_path: str) -> Any              # 读取文件
    def run_multiprocess(self, target_func, data_loader)  # 多进程读取
```

## 重构说明

本次重构主要改进：

1. **编码统一**: 从 `gbk` 改为 `utf-8`
2. **类型注解**: 添加完整的类型提示
3. **文档字符串**: 添加详细的 docstring
4. **代码风格**: 符合 PEP 8 规范
5. **错误处理**: 改进异常处理
6. **新增方法**: WindowEye 增加 minimize, maximize, close, is_valid 等方法

---

*重构时间: 2026-03-20*
*重构工具: QClaw Agent "晴"*
