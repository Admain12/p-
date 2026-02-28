#!/usr/bin/env python3
"""
测试Python环境是否正常工作
"""

import sys
import tkinter as tk

print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")

# 测试tkinter
print("\n测试tkinter...")
try:
    root = tk.Tk()
    print("创建tkinter根窗口成功")
    root.destroy()
    print("销毁tkinter根窗口成功")
except Exception as e:
    print(f"测试tkinter失败: {e}")

print("\n环境测试完成！")
sys.exit(0)
