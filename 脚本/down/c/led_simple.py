#!/usr/bin/env python3
"""
简化版LED屏幕模拟器
具有汉字显示功能
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class LEDSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("LED屏幕模拟器")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # 初始化变量
        self.LEDMode = 7  # 默认设置为汉字显示模式
        self.LEDSpeed = 1  # 速度：1=慢
        self.LEDPause = False  # 暂停标志
        self.P2 = 0x00  # LED状态
        
        # 汉字显示相关
        self.current_char = "中"  # 当前显示的汉字
        self.char_index = 0  # 汉字显示索引
        self.char_matrix = []  # 汉字点阵矩阵
        
        # 汉字点阵数据字典
        self.char_matrices = {
            "中": [
                0x18, 0x18, 0x3C, 0x3C, 0x7E, 0xFF, 0x7E, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00
            ]
        }
        
        # LED颜色
        self.led_color = "#ffff00"  # 黄色
        self.led_off_color = "#333333"  # 熄灭颜色
        
        # 运行状态
        self.running = True
        
        # 创建界面
        self.create_widgets()
        
        # 启动模拟线程
        self.thread = threading.Thread(target=self.simulate, daemon=True)
        self.thread.start()
    
    def create_widgets(self):
        """创建界面"""
        # 顶部状态栏
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(fill=tk.X)
        
        # 模式显示
        ttk.Label(status_frame, text="模式: ", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="汉字显示")
        ttk.Label(status_frame, textvariable=self.mode_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=10)
        
        # 状态显示
        ttk.Label(status_frame, text="状态: ", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W)
        self.status_var = tk.StringVar(value="运行")
        ttk.Label(status_frame, textvariable=self.status_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=10)
        
        # 颜色显示
        ttk.Label(status_frame, text="颜色: ", font=('Arial', 10, 'bold')).grid(row=0, column=4, sticky=tk.W)
        self.color_var = tk.StringVar(value="黄色")
        ttk.Label(status_frame, textvariable=self.color_var, width=10).grid(row=0, column=5, sticky=tk.W, padx=10)
        
        # 汉字显示提示
        ttk.Label(status_frame, text="当前汉字: ", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(status_frame, text=self.current_char, width=10).grid(row=1, column=1, sticky=tk.W, padx=10)
        
        # LED显示区域
        led_frame = ttk.Frame(self.root, padding=20, relief=tk.RAISED, borderwidth=2)
        led_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(led_frame, text="LED状态模拟", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=10)
        
        # LED灯
        self.leds = []
        led_container = ttk.Frame(led_frame)
        led_container.pack(fill=tk.X, pady=10)
        
        for i in range(8):
            led_box = ttk.Frame(led_container, width=60, height=60, relief=tk.RAISED, borderwidth=2)
            led_box.pack(side=tk.LEFT, padx=10)
            
            led = ttk.Label(led_box, width=6, height=3, background=self.led_off_color, relief=tk.RAISED, borderwidth=3)
            led.pack(fill=tk.BOTH, expand=True)
            self.leds.append(led)
            
            ttk.Label(led_container, text=f"P2.{7-i}", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="切换模式 (K1)", command=self.toggle_mode, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="暂停/继续 (K3)", command=self.toggle_pause, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="重置 (K4)", command=self.reset, width=15).pack(side=tk.LEFT, padx=10)
        
        # 底部信息
        info_frame = ttk.Frame(self.root, padding=10)
        info_frame.pack(fill=tk.X)
        
        ttk.Label(info_frame, text="按1键切换模式 | 按3键或空格键暂停/继续 | 按4键重置", font=('Arial', 9)).pack(anchor=tk.W)
    
    def toggle_mode(self):
        """切换模式"""
        self.LEDMode = (self.LEDMode + 1) % 8
        mode_names = ["左移", "右移", "闪烁", "呼吸灯", "追逐", "图案", "随机", "汉字显示"]
        self.mode_var.set(mode_names[self.LEDMode])
        
        # 重置状态
        self.char_index = 0
        self.char_matrix = []
    
    def toggle_pause(self):
        """暂停/继续"""
        self.LEDPause = not self.LEDPause
        if self.LEDPause:
            self.status_var.set("暂停")
        else:
            self.status_var.set("运行")
    
    def reset(self):
        """重置"""
        self.LEDMode = 7  # 重置为汉字显示模式
        self.LEDSpeed = 1
        self.LEDPause = False
        self.P2 = 0x00
        self.char_index = 0
        self.char_matrix = []
        
        # 更新显示
        self.mode_var.set("汉字显示")
        self.status_var.set("运行")
        self.update_leds()
    
    def simulate(self):
        """模拟LED显示"""
        while self.running:
            if not self.LEDPause:
                if self.LEDMode == 7:  # 汉字显示
                    if not self.char_matrix:
                        # 生成汉字点阵
                        self.generate_char_matrix(self.current_char)
                    
                    # 显示当前帧
                    if self.char_index < len(self.char_matrix):
                        self.P2 = self.char_matrix[self.char_index]
                        self.char_index += 1
                    else:
                        self.char_index = 0
                    
                    # 更新LED显示
                    self.update_leds()
                    
                    # 延时，让每一行都能清晰可见
                    time.sleep(0.5)
                else:
                    # 其他模式的简单实现
                    self.P2 = (self.P2 + 1) % 256
                    self.update_leds()
                    time.sleep(0.2)
            else:
                time.sleep(0.1)
    
    def generate_char_matrix(self, char):
        """生成汉字点阵矩阵"""
        if char in self.char_matrices:
            self.char_matrix = self.char_matrices[char]
        else:
            # 默认显示"中"字
            self.char_matrix = self.char_matrices.get("中", [0x00] * 16)
    
    def update_leds(self):
        """更新LED显示"""
        for i in range(8):
            if (self.P2 & (1 << i)) != 0:
                # LED亮
                self.leds[7-i].configure(background=self.led_color)
            else:
                # LED灭
                self.leds[7-i].configure(background=self.led_off_color)
    
    def on_key_press(self, event):
        """键盘事件处理"""
        key = event.char.lower()
        if key == '1':
            self.toggle_mode()
        elif key == '3' or event.keysym == 'space':
            self.toggle_pause()
        elif key == '4':
            self.reset()
    
    def on_closing(self):
        """关闭窗口时的处理"""
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LEDSimulator(root)
        
        # 绑定键盘事件
        root.bind('<Key>', app.on_key_press)
        
        # 绑定关闭事件
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
