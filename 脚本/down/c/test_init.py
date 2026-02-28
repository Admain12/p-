#!/usr/bin/env python3
"""
测试LED模拟器的初始化过程
"""

import sys
import traceback

try:
    print("开始测试LED模拟器初始化...")
    
    # 导入必要的模块
    import tkinter as tk
    print("导入tkinter成功")
    
    # 导入LED模拟器
    import led_gui
    print("导入led_gui成功")
    
    # 创建根窗口
    root = tk.Tk()
    print("创建根窗口成功")
    
    # 禁用窗口显示
    root.withdraw()
    print("禁用窗口显示成功")
    
    # 创建LED模拟器实例
    print("创建LED模拟器实例...")
    app = led_gui.LEDSimulator(root)
    print("创建LED模拟器实例成功！")
    
    # 检查brightness_var属性
    if hasattr(app, 'brightness_var'):
        print(f"brightness_var属性存在，值为: {app.brightness_var.get()}")
    else:
        print("ERROR: brightness_var属性不存在！")
    
    # 检查其他属性
    if hasattr(app, 'mode_var'):
        print(f"mode_var属性存在，值为: {app.mode_var.get()}")
    else:
        print("ERROR: mode_var属性不存在！")
    
    if hasattr(app, 'speed_var'):
        print(f"speed_var属性存在，值为: {app.speed_var.get()}")
    else:
        print("ERROR: speed_var属性不存在！")
    
    if hasattr(app, 'color_var'):
        print(f"color_var属性存在，值为: {app.color_var.get()}")
    else:
        print("ERROR: color_var属性不存在！")
    
    if hasattr(app, 'time_var'):
        print(f"time_var属性存在，值为: {app.time_var.get()}")
    else:
        print("ERROR: time_var属性不存在！")
    
    if hasattr(app, 'leds'):
        print(f"leds属性存在，长度为: {len(app.leds)}")
    else:
        print("ERROR: leds属性不存在！")
    
    # 清理资源
    root.destroy()
    print("清理资源成功")
    
    print("测试成功完成！")
    sys.exit(0)
except Exception as e:
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("详细错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
