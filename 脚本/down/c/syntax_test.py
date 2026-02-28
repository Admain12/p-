#!/usr/bin/env python3
"""
只测试LED控制程序的语法和导入
不涉及tkinter的实际初始化
"""

import sys
import traceback

print("开始测试LED模拟器的语法和导入...")

try:
    # 只导入模块，不创建实例
    import led_gui
    print("导入led_gui模块成功！")
    
    # 检查模块是否包含LEDSimulator类
    if hasattr(led_gui, 'LEDSimulator'):
        print("LEDSimulator类存在！")
    else:
        print("ERROR: LEDSimulator类不存在！")
    
    # 检查LEDSimulator类是否有__init__方法
    if hasattr(led_gui.LEDSimulator, '__init__'):
        print("LEDSimulator.__init__方法存在！")
    else:
        print("ERROR: LEDSimulator.__init__方法不存在！")
    
    # 检查LEDSimulator类是否有create_widgets方法
    if hasattr(led_gui.LEDSimulator, 'create_widgets'):
        print("LEDSimulator.create_widgets方法存在！")
    else:
        print("ERROR: LEDSimulator.create_widgets方法不存在！")
    
    # 检查LEDSimulator类是否有load_config方法
    if hasattr(led_gui.LEDSimulator, 'load_config'):
        print("LEDSimulator.load_config方法存在！")
    else:
        print("ERROR: LEDSimulator.load_config方法不存在！")
    
    print("\n语法和导入测试完成！")
    sys.exit(0)
except Exception as e:
    print(f"\n错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n详细错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
