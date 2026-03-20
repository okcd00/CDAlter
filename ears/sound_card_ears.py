# coding: utf-8
# ==========================================================================
#   Copyright (C) since 2026 All rights reserved.
#
#   filename : sound_card_ears.py
#   author   : chendian / okcd00@qq.com
#   feat     : https://b23.tv/rmE4VF8
#   date     : 2026/01/19 22:04:18
#   desc     : soundcard, PySide6, https://aka.ms/vs/17/release/vc_redist.x64.exe
#              
# ==========================================================================

import os, sys, time, json
import configparser
import math
import numpy as np

if sys.platform == "win32":
    import ctypes
    ole32 = ctypes.windll.ole32  # This works on Windows
    print(ole32)
else:
    raise OSError("This feature is only supported on Windows.")

import soundcard as sc
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt, QTimer, QThread, Signal, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QPolygonF

import warnings
warnings.filterwarnings("ignore", category=sc.SoundcardRuntimeWarning)

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "设置.ini")
DEVICE_LOG_PATH = os.path.join(BASE_DIR, "设备列表.txt")


def load_config():
    config = configparser.ConfigParser()
    # 默认值
    default_cfg = {
        '音频设置': {'设备索引': '0', '环境净化强度': '0.005', '采样块大小': '512'},
        '算法参数': {'箭头平滑度': '0.92', '圆弧平滑度': '0.82', '聚合阈值': '0.3', '锁定门槛': '0.006'},
        '视觉设置': {'画布大小': '500', '圆环半径': '85', '箭头半径': '120', '圆弧厚度': '7', '显示增益': '3500'},
        '颜色设置': {'圆弧颜色': '255,60,60,200', '箭头颜色': '0,255,255,220', '圆环颜色': '200,200,200,60'}
    }

    # 1. 智能读取：如果文件存在，先读入现有配置
    if os.path.exists(CONFIG_PATH):
        try:
            config.read(CONFIG_PATH, encoding='utf-8')
        except:
            pass  # 防止文件损坏导致崩溃

    # 2. 增量补全：只补缺失，不覆盖已有
    updated = False
    for sec, opts in default_cfg.items():
        if not config.has_section(sec):
            config.add_section(sec)
            updated = True
        for k, v in opts.items():
            if not config.has_option(sec, k):
                config.set(sec, k, v)
                updated = True

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        config.write(f)

    return config


def log_devices():
    try:
        mics = sc.all_microphones(include_loopback=True)
        with open(DEVICE_LOG_PATH, 'w', encoding='utf-8') as f:
            f.write("=== 音频输出设备列表 ===\n")
            for i, m in enumerate(mics):
                f.write(f"索引 [{i}]: {m.name}\n")
    except:
        pass


cfg = load_config()
log_devices()


# ===================== 🚀 音频核心 =====================
class AudioThread(QThread):
    data_signal = Signal(float, float, np.ndarray)

    def __init__(self, index):
        super().__init__()
        self.index = index;
        self.running = True
        self.chunk = cfg.getint('音频设置', '采样块大小', fallback=512)
        angles = np.radians([330, 30, 0, 0, 210, 150, 270, 90])
        self.vec_x, self.vec_y = np.sin(angles), np.cos(angles)
        self.vec_y[3] = 0

    def run(self):
        try:
            mics = sc.all_microphones(include_loopback=True)
            if self.index >= len(mics): return
            with mics[self.index].recorder(samplerate=44100) as rec:
                gate = cfg.getfloat('音频设置', '环境净化强度', fallback=0.005)
                while self.running:
                    raw = rec.record(numframes=self.chunk)
                    energies = np.sqrt(np.mean(np.square(raw), axis=0))
                    energies = np.where(energies > gate, energies, 0.0)
                    if len(energies) < 8:
                        if len(energies) == 2:
                            fl, fr = energies[0], energies[1]
                            energies = np.array([fl, fr, 0, 0, fl * 0.5, fr * 0.5, fl * 0.7, fr * 0.7])
                        else:
                            energies = np.pad(energies, (0, 8 - len(energies)))
                    vx, vy = np.dot(energies, self.vec_x), np.dot(energies, self.vec_y)
                    total_e = np.sum(energies)
                    angle = math.degrees(math.atan2(vx, vy)) if total_e > 1e-6 else 0.0
                    self.data_signal.emit(angle, total_e, energies)
        except:
            pass


# ===================== 🎨 UI 修正版 =====================
class RadarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 强制偶数画布防止像素偏移
        sz = cfg.getint('视觉设置', '画布大小', fallback=500)
        sz = sz if sz % 2 == 0 else sz + 1
        self.resize(sz, sz)

        self.angle, self.energy, self.chs = 0.0, 0.0, np.zeros(8)
        self.thread = AudioThread(cfg.getint('音频设置', '设备索引', fallback=0))
        self.thread.data_signal.connect(self.update_state)
        self.thread.start()
        self.timer = QTimer();
        self.timer.timeout.connect(self.update);
        self.timer.start(16)

    def update_state(self, a, e, chs_array):
        sm_a = cfg.getfloat('算法参数', '箭头平滑度', fallback=0.92)
        sm_r = cfg.getfloat('算法参数', '圆弧平滑度', fallback=0.82)
        if e > cfg.getfloat('算法参数', '锁定门槛', fallback=0.006):
            diff = (a - self.angle + 180) % 360 - 180
            self.angle += diff * (1 - sm_a)
        self.energy = self.energy * sm_a + e * (1 - sm_a)
        self.chs = self.chs * sm_r + chs_array * (1 - sm_r)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 核心对齐修复：获取中心浮点数，不使用整数 center()
        cx, cy = self.width() / 2.0, self.height() / 2.0

        v = cfg['视觉设置']
        r_rad = v.getfloat('圆环半径', fallback=85.0)
        a_rad = v.getfloat('箭头半径', fallback=120.0)
        thick = v.getfloat('圆弧厚度', fallback=7.0)
        gain = v.getfloat('显示增益', fallback=3500.0)

        # 1. 背景虚线圆环 (使用 QRectF 确保亚像素级居中)
        bg_pen = QPen(self.get_color('圆环颜色'), 1.5, Qt.DashLine)
        painter.setPen(bg_pen)
        rect_bg = QRectF(cx - r_rad, cy - r_rad, r_rad * 2, r_rad * 2)
        painter.drawEllipse(rect_bg)

        # 2. 记忆箭头
        arrow_c = self.get_color('箭头颜色')
        alpha = min(255, max(100, int(self.energy * gain * 2) + 100))
        arrow_c.setAlpha(alpha)
        painter.setPen(QPen(arrow_c, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(arrow_c)

        rad = math.radians(self.angle)
        tip = QPointF(cx + a_rad * math.sin(rad), cy - a_rad * math.cos(rad))
        base = QPointF(cx + (a_rad - 35) * math.sin(rad), cy - (a_rad - 35) * math.cos(rad))
        painter.drawLine(base, tip)

        w = 13
        p2 = QPointF(tip.x() + w * math.sin(rad + 2.6), tip.y() - w * math.cos(rad + 2.6))
        p3 = QPointF(tip.x() + w * math.sin(rad - 2.6), tip.y() - w * math.cos(rad - 2.6))
        painter.drawPolygon(QPolygonF([tip, p2, p3]))

        # 3. 智能聚合圆弧 (逻辑同前)
        arc_base_c = self.get_color('圆弧颜色')
        draw_list = []
        gate_e, merge_t = 0.002, cfg.getfloat('算法参数', '聚合阈值', fallback=0.3)

        # 判定
        fl, fr = self.chs[0], self.chs[1]
        if fl > gate_e and fr > gate_e and abs(fl - fr) / max(fl, fr, 0.001) < merge_t:
            draw_list.append((0, (fl + fr) / 2))
        else:
            if fl > gate_e: draw_list.append((-30, fl));
            if fr > gate_e: draw_list.append((30, fr))
        rl, rr = self.chs[4], self.chs[5]
        if rl > gate_e and rr > gate_e and abs(rl - rr) / max(rl, rr, 0.001) < merge_t:
            draw_list.append((180, (rl + rr) / 2))
        else:
            if rl > gate_e: draw_list.append((-150, rl));
            if rr > gate_e: draw_list.append((150, rr))
        if self.chs[6] > gate_e: draw_list.append((-90, self.chs[6]))
        if self.chs[7] > gate_e: draw_list.append((90, self.chs[7]))

        for ang, en in draw_list:
            span = min(15 + en * gain * 0.1, 45)
            c = QColor(arc_base_c);
            c.setAlpha(min(255, int(en * gain * 5) + 60))
            painter.setPen(QPen(c, thick, Qt.SolidLine, Qt.RoundCap))
            qt_ang = (90 - ang) - span / 2
            painter.drawArc(rect_bg, int(qt_ang * 16), int(span * 16))

    def get_color(self, key):
        c_str = cfg.get('颜色设置', key, fallback='255,255,255,255')
        c = [int(x) for x in c_str.split(',')]
        return QColor(c[0], c[1], c[2], c[3])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadarApp()
    screen_geo = app.primaryScreen().geometry()
    window.move(screen_geo.center().x() - window.width() // 2,
                screen_geo.center().y() - window.height() // 2)
    window.show()
    sys.exit(app.exec())