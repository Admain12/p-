#!/usr/bin/env python3
"""
只测试led_gui模块的导入
"""

import sys
import traceback

try:
    print("尝试导入led_gui模块...")
    import led_gui
    print("导入led_gui模块成功！")
    print(f"模块名称: {led_gui.__name__}")
    print(f"模块文件路径: {led_gui.__file__}")
    print("测试成功完成！")
    sys.exit(0)
except Exception as e:
    print(f"错误类型: {type(e).__name__}")
    print(f"错误信息: {e}")
    print("详细错误堆栈:")
    traceback.print_exc()
    sys.exit(1)
