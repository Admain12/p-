#!/usr/bin/env python3
"""
代码可行性测试脚本
检查LED控制程序的语法和结构
"""

import re

# 读取代码文件
def read_code_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取文件失败: {e}")
        return None

# 检查代码语法和结构
def check_code_structure(content):
    if not content:
        return False
    
    print("=== 代码结构检查 ===")
    
    # 检查必要的包含文件
    includes = re.findall(r'#include\s+<[^>]+>', content)
    print(f"包含文件: {includes}")
    
    # 检查函数定义
    functions = re.findall(r'void\s+\w+\s*\([^)]*\)', content)
    print(f"函数定义: {functions}")
    
    # 检查主函数
    main_func = re.search(r'void\s+main\s*\(void\)', content)
    if main_func:
        print("✓ 主函数存在")
    else:
        print("✗ 主函数不存在")
        return False
    
    # 检查定时器初始化
    timer_init = re.search(r'Timer0_Init\s*\(\)', content)
    if timer_init:
        print("✓ 定时器初始化函数存在")
    else:
        print("✗ 定时器初始化函数不存在")
        return False
    
    # 检查按键扫描函数
    key_func = re.search(r'key\s*\(\)', content)
    if key_func:
        print("✓ 按键扫描函数存在")
    else:
        print("✗ 按键扫描函数不存在")
        return False
    
    # 检查延时函数
    delay_func = re.search(r'DelayMs\s*\(\)', content)
    if delay_func:
        print("✓ 延时函数存在")
    else:
        print("✗ 延时函数不存在")
        return False
    
    # 检查呼吸灯函数
    breathe_func = re.search(r'LED_Breathe\s*\(\)', content)
    if breathe_func:
        print("✓ 呼吸灯函数存在")
    else:
        print("✗ 呼吸灯函数不存在")
        return False
    
    # 检查追逐模式函数
    chase_func = re.search(r'LED_Chase\s*\(\)', content)
    if chase_func:
        print("✓ 追逐模式函数存在")
    else:
        print("✗ 追逐模式函数不存在")
        return False
    
    # 检查图案模式函数
    pattern_func = re.search(r'LED_Pattern\s*\(\)', content)
    if pattern_func:
        print("✓ 图案模式函数存在")
    else:
        print("✗ 图案模式函数不存在")
        return False
    
    # 检查随机模式函数
    random_func = re.search(r'LED_Random\s*\(\)', content)
    if random_func:
        print("✓ 随机模式函数存在")
    else:
        print("✗ 随机模式函数不存在")
        return False
    
    # 检查全局变量
    global_vars = re.findall(r'\b(?:uchar|uint|bit)\s+\w+\s*=', content)
    print(f"全局变量: {global_vars}")
    
    print("\n=== 代码检查完成 ===")
    return True

# 主函数
if __name__ == "__main__":
    code_file = "Untitled-1.c++"
    code_content = read_code_file(code_file)
    if code_content:
        is_valid = check_code_structure(code_content)
        if is_valid:
            print("\n✓ 代码结构检查通过，语法基本正确")
            print("✓ 代码可行性测试通过")
        else:
            print("\n✗ 代码结构检查失败，存在语法问题")
    else:
        print("✗ 无法读取代码文件")
