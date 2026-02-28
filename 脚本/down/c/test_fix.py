#!/usr/bin/env python3
"""
测试修复是否成功
"""

import tkinter as tk
from tkinter import ttk
import time
import threading

class TestFix:
    def __init__(self, root):
        self.root = root
        self.root.title("测试修复")
        self.root.geometry("300x200")
        
        # 初始化变量
        self.LEDSpeed = 1
        
        # 创建界面
        ttk.Label(self.root, text="测试LEDSpeed变量", font=('Arial', 12, 'bold')).pack(pady=20)
        
        # 测试按钮
        ttk.Button(self.root, text="测试LEDSpeed", command=self.test_led_speed).pack(pady=10)
        
        # 状态显示
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.root, textvariable=self.status_var, font=('Arial', 10)).pack(pady=10)
    
    def test_led_speed(self):
        """测试LEDSpeed变量"""
        try:
            # 测试之前出错的代码逻辑
            delay = 0.8  # 慢
            if self.LEDSpeed == 2:
                delay = 0.5  # 中
            elif self.LEDSpeed == 3:
                delay = 0.3  # 快
            
            self.status_var.set(f"测试成功！LEDSpeed = {self.LEDSpeed}, delay = {delay}")
        except Exception as e:
            self.status_var.set(f"测试失败: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TestFix(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
