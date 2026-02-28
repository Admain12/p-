#!/usr/bin/env python3
"""
简化版汉字显示测试
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class SimpleCharDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("汉字显示测试")
        self.root.geometry("600x300")
        
        # 初始化变量
        self.current_char = "中"
        self.char_index = 0
        self.char_matrix = []
        self.P2 = 0x00
        self.running = True
        
        # LED颜色
        self.led_color = "#ffff00"  # 黄色
        self.led_off_color = "#333333"  # 熄灭颜色
        
        # 汉字点阵数据
        self.char_matrices = {
            "中": [
                0x18, 0x18, 0x3C, 0x3C, 0x7E, 0xFF, 0x7E, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00
            ]
        }
        
        # 创建界面
        self.create_widgets()
        
        # 启动显示线程
        self.thread = threading.Thread(target=self.simulate, daemon=True)
        self.thread.start()
    
    def create_widgets(self):
        """创建界面"""
        # 状态栏
        status_frame = ttk.Frame(self.root, padding=10)
        status_frame.pack(fill=tk.X)
        
        ttk.Label(status_frame, text="当前汉字: ", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(status_frame, text=self.current_char, font=('Arial', 10)).grid(row=0, column=1, sticky=tk.W, padx=10)
        
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
            
            ttk.Label(led_container, text=f"P2.{7-i}", font=('Arial', 9)).pack(side=tk.LEFT, padx=10)
    
    def simulate(self):
        """模拟汉字显示"""
        # 生成汉字点阵
        self.generate_char_matrix(self.current_char)
        
        while self.running:
            if self.char_matrix:
                # 显示当前行
                if self.char_index < len(self.char_matrix):
                    self.P2 = self.char_matrix[self.char_index]
                    self.update_leds()
                    self.char_index += 1
                else:
                    self.char_index = 0
                
                # 延时，让每一行都能清晰可见
                time.sleep(1.0)
    
    def generate_char_matrix(self, char):
        """生成汉字点阵"""
        if char in self.char_matrices:
            self.char_matrix = self.char_matrices[char]
        else:
            self.char_matrix = [0x00] * 16
    
    def update_leds(self):
        """更新LED显示"""
        for i in range(8):
            if (self.P2 & (1 << i)) != 0:
                # LED亮
                self.leds[7-i].configure(background=self.led_color)
            else:
                # LED灭
                self.leds[7-i].configure(background=self.led_off_color)
    
    def on_closing(self):
        """关闭窗口"""
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCharDisplay(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()