#!/usr/bin/env python3
"""
测试汉字显示功能
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class CharDisplayTest:
    def __init__(self, root):
        self.root = root
        self.root.title("汉字显示测试")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # 初始化变量
        self.char_index = 0
        self.char_matrix = []
        
        # 汉字点阵数据 - 使用更明显的"中"字
        self.char_matrices = {
            "中": [
                0x00,  # ........
                0x18,  # ....##..
                0x18,  # ....##..
                0x3C,  # ...####.
                0x3C,  # ...####.
                0x7E,  # ..######
                0xFF,  # ########
                0xFF,  # ########
                0xFF,  # ########
                0x7E,  # ..######
                0x3C,  # ...####.
                0x3C,  # ...####.
                0x18,  # ....##..
                0x18,  # ....##..
                0x00,  # ........
                0x00   # ........
            ]
        }
        
        # LED颜色
        self.led_color = "#ffff00"
        self.led_off_color = "#333333"
        
        # 运行状态
        self.running = True
        
        # 创建界面
        self.create_widgets()
        
        # 启动显示线程
        self.thread = threading.Thread(target=self.simulate, daemon=True)
        self.thread.start()
    
    def create_widgets(self):
        """创建界面"""
        # 标题
        ttk.Label(self.root, text="汉字显示测试 - 中", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # LED显示区域
        led_frame = ttk.Frame(self.root, padding=20, relief=tk.RAISED, borderwidth=2)
        led_frame.pack(fill=tk.BOTH, expand=True)
        
        # LED灯
        self.leds = []
        led_container = ttk.Frame(led_frame)
        led_container.pack(fill=tk.X, pady=10)
        
        for i in range(8):
            led_box = ttk.Frame(led_container, width=40, height=40, relief=tk.RAISED, borderwidth=2)
            led_box.pack(side=tk.LEFT, padx=5)
            
            led = ttk.Label(led_box, width=4, height=2, background=self.led_off_color, relief=tk.RAISED, borderwidth=3)
            led.pack(fill=tk.BOTH, expand=True)
            self.leds.append(led)
        
        # 状态信息
        self.status_var = tk.StringVar(value="正在显示 '中' 字...")
        ttk.Label(self.root, textvariable=self.status_var, font=('Arial', 10)).pack(pady=10)
    
    def simulate(self):
        """模拟汉字显示"""
        # 加载"中"字点阵
        self.char_matrix = self.char_matrices["中"]
        
        while self.running:
            # 显示当前行
            if self.char_index < len(self.char_matrix):
                row_data = self.char_matrix[self.char_index]
                self.update_leds(row_data)
                self.status_var.set(f"显示第 {self.char_index + 1}/16 行")
                self.char_index += 1
            else:
                self.char_index = 0
                self.status_var.set(f"显示完成，重新开始")
            
            # 延时，让每一行都能清晰可见
            time.sleep(0.5)
    
    def update_leds(self, row_data):
        """更新LED显示"""
        for i in range(8):
            if (row_data & (1 << i)) != 0:
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
    try:
        root = tk.Tk()
        app = CharDisplayTest(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
