#!/usr/bin/env python3
"""
基本GUI测试
"""

import tkinter as tk
from tkinter import ttk

class BasicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("基本GUI测试")
        self.root.geometry("300x200")
        
        # 创建标签
        label = ttk.Label(root, text="Hello World!")
        label.pack(pady=20)
        
        # 创建按钮
        button = ttk.Button(root, text="点击我", command=self.on_button_click)
        button.pack(pady=10)
    
    def on_button_click(self):
        print("按钮被点击了！")

if __name__ == "__main__":
    root = tk.Tk()
    app = BasicGUI(root)
    root.mainloop()