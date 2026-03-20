# -*- coding: utf-8 -*-
"""
CDAlter - 桌面自动化框架

本框架按人体部位命名模块，提供看、听、说、操作电脑等自动化功能。

使用示例：
    from boot import CDBrain

    brain = CDBrain()
    brain.use_eyes['window_eye'].set_foreground()
    brain.use_hands['key_mouse_hand'].click(100, 200)

模块说明：
    - eyes: 视觉感知（窗口识别、截图、OCR）
    - hands: 操作执行（键鼠控制、Shell命令）
    - mouth: 输出表达（语音合成）
    - brain: 决策中心
    - ears: 输入接收（语音识别）
    - nerve: GUI 交互
    - memory: 数据存储
"""

from __future__ import annotations

from utils import PROJECT_PATH

# 延迟导入，按需加载
_use_eyes = {}
_use_hands = {}


class CDBrain:
    """
    大脑 - 控制和协调各个模块

    作为中央控制器，管理眼睛、手等模块。

    Attributes:
        use_eyes: 可用的视觉模块
        use_hands: 可用的操作模块

    使用示例：
        brain = CDBrain()
        brain.use_eyes['window_eye'].set_foreground()
    """

    @property
    def use_eyes(self) -> dict:
        """获取可用的视觉模块"""
        if not _use_eyes:
            from eyes.window_eye import WindowEye
            _use_eyes['window_eye'] = WindowEye()
        return _use_eyes

    @property
    def use_hands(self) -> dict:
        """获取可用的操作模块"""
        if not _use_hands:
            from hands.key_mouse_hand import KeyMouseHand
            _use_hands['key_mouse_hand'] = KeyMouseHand()
        return _use_hands

    def __repr__(self) -> str:
        return f"<CDBrain eyes={list(self.use_eyes.keys())} hands={list(self.use_hands.keys())}>"

    def __str__(self) -> str:
        return "CDBrain - Desktop Automation Framework"


# 兼容旧代码的类属性
CDBrain.USE_EYES = property(lambda self: self.use_eyes)
CDBrain.USE_HANDS = property(lambda self: self.use_hands)


def main():
    """主入口函数"""
    print("=" * 50)
    print("CDAlter - Desktop Automation Framework")
    print("=" * 50)
    print(f"Project Path: {PROJECT_PATH}")
    print()

    # 初始化大脑
    brain = CDBrain()
    print(f"Brain: {brain}")

    # 测试眼睛
    print("\n=== Testing Eyes ===")
    window_eye = brain.use_eyes['window_eye']
    print(f"WindowEye: {window_eye}")

    # 测试手
    print("\n=== Testing Hands ===")
    hand = brain.use_hands['key_mouse_hand']
    print(f"Hand: {hand}")
    print(f"Current position: {hand.current_position}")

    print("\n=== All modules loaded successfully ===")


if __name__ == '__main__':
    main()
