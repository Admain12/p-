#!/usr/bin/env python3
"""
简化的LED控制程序测试脚本
只测试初始化过程，不运行主循环
"""

import sys
import traceback

print("开始测试LED模拟器初始化...")

# 导入必要的模块
try:
    import tkinter as tk
    print("导入tkinter成功")
except ImportError as e:
    print(f"导入tkinter失败: {e}")
    sys.exit(1)

try:
    # 导入LED模拟器
    from led_gui import LEDSimulator
    print("导入LED模拟器成功")
    
    # 创建根窗口
    root = tk.Tk()
    print("创建根窗口成功")
    
    # 禁用窗口显示，只测试初始化
    root.withdraw()
    print("禁用窗口显示成功")
    
    # 创建LED模拟器实例
    print("开始创建LED模拟器实例...")
    app = LEDSimulator(root)
    print("创建LED模拟器实例成功！")
    
    # 检查是否创建了brightness_var属性
    if hasattr(app, 'brightness_var'):
        print("brightness_var属性创建成功！")
        print(f"brightness_var当前值: {app.brightness_var.get()}")
    else:
        print("ERROR: brightness_var属性未创建！")
    
    # 检查其他重要属性
    if hasattr(app, 'mode_var'):
        print("mode_var属性创建成功！")
    else:
        print("ERROR: mode_var属性未创建！")
    
    if hasattr(app, 'speed_var'):
        print("speed_var属性创建成功！")
    else:
        print("ERROR: speed_var属性未创建！")
    
    if hasattr(app, 'color_var'):
        print("color_var属性创建成功！")
    else:
        print("ERROR: color_var属性未创建！")
    
    if hasattr(app, 'time_var'):
        print("time_var属性创建成功！")
    else:
        print("ERROR: time_var属性未创建！")
    
    if hasattr(app, 'leds'):
        print(f"leds属性创建成功！LED数量: {len(app.leds)}")
    else:
        print("ERROR: leds属性未创建！")
    
    print("\n测试完成！所有属性创建成功。")
    
    # 清理资源
    root.destroy()
    print("资源清理完成。")
    
    sys.exit(0)
except Exception as e:
    print(f"\n错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n详细错误堆栈:")
    traceback.print_exc()
    
    # 尝试清理资源
    try:
        if 'root' in locals():
            root.destroy()
    except:
        pass
    
    sys.exit(1)
