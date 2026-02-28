#!/usr/bin/env python3
"""
使用ast模块检查led_gui.py文件的语法
"""

import ast
import sys

try:
    print("开始检查led_gui.py文件的语法...")
    
    # 打开文件
    with open('led_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"文件大小: {len(content)} 字节")
    
    # 使用ast模块解析文件
    tree = ast.parse(content)
    print("文件语法解析成功！")
    
    # 打印文件中的类和函数
    print("\n文件中的类和函数:")
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            print(f"类: {node.name}")
        elif isinstance(node, ast.FunctionDef):
            print(f"函数: {node.name}")
    
    print("\n语法检查成功完成！")
    sys.exit(0)
except SyntaxError as e:
    print(f"语法错误: {e}")
    print(f"错误位置: 第{e.lineno}行，第{e.offset}列")
    sys.exit(1)
except Exception as e:
    print(f"其他错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
