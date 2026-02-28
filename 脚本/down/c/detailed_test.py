#!/usr/bin/env python3
"""
详细的LED控制程序测试脚本
尝试捕获更多的错误信息
"""

import sys
import traceback
import os

print(f"Python版本: {sys.version}")
print(f"当前工作目录: {os.getcwd()}")
print(f"led_gui.py文件是否存在: {os.path.exists('led_gui.py')}")

# 尝试读取led_gui.py文件内容
if os.path.exists('led_gui.py'):
    print("\n尝试读取led_gui.py文件内容:")
    try:
        with open('led_gui.py', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"文件大小: {len(content)} 字节")
        print(f"文件行数: {len(content.splitlines())}")
        print("\n文件前100行:")
        lines = content.splitlines()
        for i, line in enumerate(lines[:100]):
            print(f"{i+1}: {line}")
    except Exception as e:
        print(f"读取文件失败: {e}")

try:
    # 导入LED模拟器
    print("\n尝试导入LED模拟器...")
    import led_gui
    print("导入led_gui模块成功！")
    
    # 检查模块属性
    print("\n检查led_gui模块属性:")
    print(f"LEDSimulator类是否存在: {hasattr(led_gui, 'LEDSimulator')}")
    
    if hasattr(led_gui, 'LEDSimulator'):
        print(f"LEDSimulator类类型: {type(led_gui.LEDSimulator)}")
        print(f"LEDSimulator.__init__方法是否存在: {hasattr(led_gui.LEDSimulator, '__init__')}")
        print(f"LEDSimulator.create_widgets方法是否存在: {hasattr(led_gui.LEDSimulator, 'create_widgets')}")
        print(f"LEDSimulator.load_config方法是否存在: {hasattr(led_gui.LEDSimulator, 'load_config')}")
        
        # 检查LEDSimulator类的属性
        print("\n检查LEDSimulator类的属性:")
        import inspect
        src = inspect.getsource(led_gui.LEDSimulator)
        print(f"LEDSimulator类源代码行数: {len(src.splitlines())}")
        
        # 检查是否包含brightness_var的定义
        if 'brightness_var' in src:
            print("brightness_var在LEDSimulator类中定义")
        else:
            print("ERROR: brightness_var不在LEDSimulator类中定义")
    
    sys.exit(0)
except Exception as e:
    print(f"\n错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("\n详细错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
