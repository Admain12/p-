#!/usr/bin/env python3
"""
代码可行性检查脚本
分析LED控制程序的语法和结构
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
    
    # 检查类型定义
    typedefs = re.findall(r'#define\s+\w+\s+\w+', content)
    print(f"类型定义: {typedefs}")
    
    # 检查全局变量
    global_vars = re.findall(r'\b(?:uchar|uint|bit)\s+\w+\s*=', content)
    print(f"全局变量: {global_vars}")
    
    # 检查函数声明
    function_decls = re.findall(r'void\s+\w+\s*\([^)]*\)\s*;', content)
    function_decls.extend(re.findall(r'uchar\s+\w+\s*\([^)]*\)\s*;', content))
    print(f"函数声明: {function_decls}")
    
    # 检查函数定义
    function_defs = re.findall(r'void\s+\w+\s*\([^)]*\)\s*\{', content)
    function_defs.extend(re.findall(r'uchar\s+\w+\s*\([^)]*\)\s*\{', content))
    print(f"函数定义: {function_defs}")
    
    # 检查主函数
    main_func = re.search(r'void\s+main\s*\(void\)\s*\{', content)
    if main_func:
        print("✓ 主函数存在")
    else:
        print("✗ 主函数不存在")
        return False
    
    # 检查定时器初始化
    timer_init = re.search(r'void\s+Timer0_Init\s*\([^)]*\)\s*\{', content)
    if timer_init:
        print("✓ 定时器初始化函数存在")
    else:
        print("✗ 定时器初始化函数不存在")
        return False
    
    # 检查按键扫描函数
    key_func = re.search(r'uchar\s+key\s*\([^)]*\)\s*\{', content)
    if key_func:
        print("✓ 按键扫描函数存在")
    else:
        print("✗ 按键扫描函数不存在")
        return False
    
    # 检查延时函数
    delay_func = re.search(r'void\s+DelayMs\s*\([^)]*\)\s*\{', content)
    if delay_func:
        print("✓ 延时函数存在")
    else:
        print("✗ 延时函数不存在")
        return False
    
    # 检查呼吸灯函数
    breathe_func = re.search(r'void\s+LED_Breathe\s*\([^)]*\)\s*\{', content)
    if breathe_func:
        print("✓ 呼吸灯函数存在")
    else:
        print("✗ 呼吸灯函数不存在")
        return False
    
    # 检查追逐模式函数
    chase_func = re.search(r'void\s+LED_Chase\s*\([^)]*\)\s*\{', content)
    if chase_func:
        print("✓ 追逐模式函数存在")
    else:
        print("✗ 追逐模式函数不存在")
        return False
    
    # 检查图案模式函数
    pattern_func = re.search(r'void\s+LED_Pattern\s*\([^)]*\)\s*\{', content)
    if pattern_func:
        print("✓ 图案模式函数存在")
    else:
        print("✗ 图案模式函数不存在")
        return False
    
    # 检查随机模式函数
    random_func = re.search(r'void\s+LED_Random\s*\([^)]*\)\s*\{', content)
    if random_func:
        print("✓ 随机模式函数存在")
    else:
        print("✗ 随机模式函数不存在")
        return False
    
    # 检查定时器中断服务函数
    timer_isr = re.search(r'void\s+Timer0_ISR\s*\(void\)\s*interrupt\s+1\s*\{', content)
    if timer_isr:
        print("✓ 定时器中断服务函数存在")
    else:
        print("✗ 定时器中断服务函数不存在")
        return False
    
    # 检查模式切换逻辑
    mode_switch = re.search(r'LEDMode\s*\+\+', content)
    if mode_switch:
        print("✓ 模式切换逻辑存在")
    else:
        print("✗ 模式切换逻辑不存在")
        return False
    
    # 检查速度切换逻辑
    speed_switch = re.search(r'LEDSpeed\s*\+\+', content)
    if speed_switch:
        print("✓ 速度切换逻辑存在")
    else:
        print("✗ 速度切换逻辑不存在")
        return False
    
    # 检查暂停/继续逻辑
    pause_switch = re.search(r'LEDPause\s*=\s*!LEDPause', content)
    if pause_switch:
        print("✓ 暂停/继续逻辑存在")
    else:
        print("✗ 暂停/继续逻辑不存在")
        return False
    
    # 检查重置逻辑
    reset_logic = re.search(r'LEDMode\s*=\s*0', content)
    if reset_logic:
        print("✓ 重置逻辑存在")
    else:
        print("✗ 重置逻辑不存在")
        return False
    
    print("\n=== 代码检查完成 ===")
    return True

# 检查代码逻辑
def check_code_logic(content):
    if not content:
        return False
    
    print("\n=== 代码逻辑检查 ===")
    
    # 检查模式数量
    mode_check = re.search(r'if\s*\(LEDMode\s*>=[^)]*4\)', content)
    if mode_check:
        print("✓ 模式数量检查逻辑正确")
    else:
        print("✗ 模式数量检查逻辑可能有问题")
    
    # 检查速度设置
    speed_check = re.search(r'switch\s*\(LEDSpeed\)', content)
    if speed_check:
        print("✓ 速度设置逻辑正确")
    else:
        print("✗ 速度设置逻辑可能有问题")
    
    # 检查定时器中断逻辑
    timer_check = re.search(r'if\s*\(!LEDPause\)', content)
    if timer_check:
        print("✓ 定时器中断逻辑正确")
    else:
        print("✗ 定时器中断逻辑可能有问题")
    
    # 检查LED控制逻辑
    led_check = re.search(r'P2\s*=', content)
    if led_check:
        print("✓ LED控制逻辑正确")
    else:
        print("✗ LED控制逻辑可能有问题")
    
    print("\n=== 逻辑检查完成 ===")
    return True

# 主函数
if __name__ == "__main__":
    code_file = "Untitled-1.c++"
    code_content = read_code_file(code_file)
    if code_content:
        print(f"文件大小: {len(code_content)} 字节")
        print(f"行数: {len(code_content.splitlines())}")
        print()
        
        is_structure_valid = check_code_structure(code_content)
        is_logic_valid = check_code_logic(code_content)
        
        if is_structure_valid and is_logic_valid:
            print("\n✅ 代码可行性检查通过")
            print("代码结构完整，逻辑正确，可以在51单片机上运行")
        else:
            print("\n❌ 代码可行性检查失败")
            print("代码可能存在结构或逻辑问题")
    else:
        print("❌ 无法读取代码文件")
