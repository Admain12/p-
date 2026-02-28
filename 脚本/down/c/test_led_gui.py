#!/usr/bin/env python3
"""
测试LED控制程序的脚本
用于捕获和显示详细的错误信息
"""

import tkinter as tk
import sys
import traceback

try:
    # 导入LED模拟器
    from led_gui import LEDSimulator
    
    print("正在初始化LED模拟器...")
    
    # 创建根窗口
    root = tk.Tk()
    
    print("创建LED模拟器实例...")
    
    # 创建LED模拟器实例
    app = LEDSimulator(root)
    
    print("LED模拟器初始化成功！")
    print("运行主循环...")
    
    # 运行主循环
    root.mainloop()
    
    print("程序正常退出。")
    
    sys.exit(0)
except Exception as e:
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n详细错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
