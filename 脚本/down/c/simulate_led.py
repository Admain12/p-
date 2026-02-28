#!/usr/bin/env python3
"""
LED控制程序模拟器
模拟51单片机LED控制程序的运行
"""

import time
import random

# 模拟全局变量
keyNum = 0  # 按键键值
LEDMode = 0  # LED模式：0=左移， 1=右移， 2=闪烁， 3=呼吸灯， 4=追逐， 5=图案， 6=随机
LEDSpeed = 1  # LED速度：1=慢， 2=中， 3=快
speedDelay = 25  # 速度对应的延时计数
LEDPause = False  # LED暂停标志：False=运行，True=暂停
chasePos = 0  # 追逐模式位置
patternIndex = 0  # 图案模式索引

# 模拟P2端口
P2 = 0xfe  # 初始状态：P2.0亮，其他灭（1111 1110）

# 模拟按键状态
P3_1 = 1  # k1
P3_0 = 1  # k2
P3_2 = 1  # k3
P3_3 = 1  # k4

# 预设图案数组
patterns = [
    0x00, # 全灭
    0xff, # 全亮
    0x55, # 交替亮灭
    0xaa, # 交替灭亮
    0x0f, # 前4个亮
    0xf0, # 后4个亮
    0x81, # 两边亮
    0x42, # 中间两边亮
    0x24, # 中间亮
    0x18  # 中间两边亮
]

# 呼吸灯相关变量
brightness = 0  # 亮度值：0-10
direction = False  # 方向：False=变亮，True=变暗
breath_cnt = 0  # 呼吸灯计数器

# 随机数种子
randSeed = 12345

# 模拟延时函数
def DelayMs(ms):
    """模拟延时函数"""
    time.sleep(ms / 1000)

# 模拟按键扫描函数
def key():
    """模拟按键扫描函数"""
    global P3_1, P3_0, P3_2, P3_3
    keyNum = 0
    
    # 检测k1 (P3.1)
    if P3_1 == 0:
        DelayMs(20)  # 消抖延时
        while P3_1 == 0:
            pass  # 等待按键释放
        DelayMs(20)  # 释放消抖
        keyNum = 1
    
    # 检测k2 (P3.0)
    if P3_0 == 0:
        DelayMs(20)  # 消抖延时
        while P3_0 == 0:
            pass  # 等待按键释放
        DelayMs(20)  # 释放消抖
        keyNum = 2
    
    # 检测k3 (P3.2)
    if P3_2 == 0:
        DelayMs(20)  # 消抖延时
        while P3_2 == 0:
            pass  # 等待按键释放
        DelayMs(20)  # 释放消抖
        keyNum = 3
    
    # 检测k4 (P3.3)
    if P3_3 == 0:
        DelayMs(20)  # 消抖延时
        while P3_3 == 0:
            pass  # 等待按键释放
        DelayMs(20)  # 释放消抖
        keyNum = 4
    
    return keyNum

# 模拟呼吸灯效果函数
def LED_Breathe():
    """模拟呼吸灯效果函数"""
    global brightness, direction, breath_cnt, P2
    
    breath_cnt += 1
    if breath_cnt >= 10:  # 每个亮度级别持续10个周期
        breath_cnt = 0
        
        if direction is False:  # 变亮
            brightness += 1
            if brightness >= 10:
                direction = True  # 开始变暗
        else:  # 变暗
            brightness -= 1
            if brightness <= 0:
                direction = False  # 开始变亮
    
    # 根据亮度控制LED
    if brightness == 0:
        P2 = 0xff  # 全灭
    elif brightness == 10:
        P2 = 0x00  # 全亮
    else:
        # 使用软件PWM实现亮度控制
        P2 = 0x00  # 点亮
        DelayMs(brightness)
        P2 = 0xff  # 熄灭
        DelayMs(10 - brightness)

# 模拟追逐模式函数
def LED_Chase():
    """模拟追逐模式函数"""
    global chasePos, P2
    # 追逐效果：单个LED从左到右移动
    P2 = 0xff  # 全灭
    P2 &= ~(0x01 << chasePos)  # 点亮当前位置
    
    chasePos += 1
    if chasePos >= 8:  # 8个LED
        chasePos = 0

# 模拟图案模式函数
def LED_Pattern():
    """模拟图案模式函数"""
    global patternIndex, P2
    P2 = patterns[patternIndex]
    
    patternIndex += 1
    if patternIndex >= len(patterns):
        patternIndex = 0

# 模拟随机模式函数
def LED_Random():
    """模拟随机模式函数"""
    global randSeed, P2
    # 简单的线性同余生成器
    randSeed = (randSeed * 1103515245 + 12345) % 32768
    
    # 使用随机数控制LED
    P2 = randSeed % 256  # 0-255的随机值

# 模拟定时器中断服务函数
def Timer0_ISR():
    """模拟定时器中断服务函数"""
    global P2, LEDMode, LEDPause, chasePos, patternIndex
    
    # 检查是否暂停
    if not LEDPause:
        # 根据模式控制LED流动
        if LEDMode == 0:  # 模式0:左移
            P2 = ((P2 << 1) | (P2 >> 7)) & 0xff  # 循环左移一位
        elif LEDMode == 1:  # 模式1:右移
            P2 = ((P2 >> 1) | (P2 << 7)) & 0xff  # 循环右移一位
        elif LEDMode == 2:  # 模式2:闪烁
            P2 = ~P2 & 0xff  # 取反，实现闪烁效果
        elif LEDMode == 3:  # 模式3:呼吸灯
            LED_Breathe()  # 调用呼吸灯函数
        elif LEDMode == 4:  # 模式4:追逐
            LED_Chase()  # 调用追逐模式函数
        elif LEDMode == 5:  # 模式5:图案
            LED_Pattern()  # 调用图案模式函数
        elif LEDMode == 6:  # 模式6:随机
            LED_Random()  # 调用随机模式函数

# 打印LED状态
def print_led_status():
    """打印LED状态"""
    global P2, LEDMode, LEDSpeed, LEDPause
    
    # 转换P2值为LED状态
    led_state = []
    for i in range(8):
        if (P2 & (1 << i)) == 0:
            led_state.append('●')  # 亮
        else:
            led_state.append('○')  # 灭
    
    # 模式名称
    mode_names = ["左移", "右移", "闪烁", "呼吸灯", "追逐", "图案", "随机"]
    mode_name = mode_names[LEDMode] if LEDMode < len(mode_names) else "未知"
    
    # 速度名称
    speed_names = ["", "慢", "中", "快"]
    speed_name = speed_names[LEDSpeed] if LEDSpeed < len(speed_names) else "未知"
    
    # 暂停状态
    pause_state = "暂停" if LEDPause else "运行"
    
    # 打印状态
    print(f"模式: {mode_name} | 速度: {speed_name} | 状态: {pause_state} | LED: {' '.join(led_state[::-1])}")

# 模拟主函数
def main():
    """模拟主函数"""
    global keyNum, LEDMode, LEDSpeed, speedDelay, LEDPause, chasePos, patternIndex, P2
    global P3_1, P3_0, P3_2, P3_3
    
    print("=== LED控制程序模拟器 ===")
    print("操作说明:")
    print("1: 切换模式")
    print("2: 切换速度")
    print("3: 暂停/继续")
    print("4: 重置")
    print("q: 退出")
    print("======================")
    
    # 初始状态
    P2 = 0xfe  # 初始状态：P2.0亮，其他灭（1111 1110）
    print_led_status()
    
    # 模拟主循环
    while True:
        # 模拟按键输入
        key_input = input("请输入按键 (1-4, q): ")
        
        if key_input == 'q':
            print("退出模拟器")
            break
        elif key_input == '1':
            # 模拟k1按键按下
            P3_1 = 0
            time.sleep(0.1)
            P3_1 = 1
        elif key_input == '2':
            # 模拟k2按键按下
            P3_0 = 0
            time.sleep(0.1)
            P3_0 = 1
        elif key_input == '3':
            # 模拟k3按键按下
            P3_2 = 0
            time.sleep(0.1)
            P3_2 = 1
        elif key_input == '4':
            # 模拟k4按键按下
            P3_3 = 0
            time.sleep(0.1)
            P3_3 = 1
        else:
            print("无效输入，请重新输入")
            continue
        
        # 模拟按键扫描
        keyNum = key()
        
        # 处理按键输入
        if keyNum:
            if keyNum == 1:  # 如果k1按键按下：切换模式
                LEDMode += 1
                if LEDMode >= 7:  # 0-6七种模式
                    LEDMode = 0
                # 模式切换时重置相关参数
                chasePos = 0
                patternIndex = 0
            elif keyNum == 2:  # 如果k2按键按下：切换速度
                LEDSpeed += 1
                if LEDSpeed >= 4:  # 1-3三种速度
                    LEDSpeed = 1
                # 根据速度设置延时
                if LEDSpeed == 1:
                    speedDelay = 25  # 慢：500ms
                elif LEDSpeed == 2:
                    speedDelay = 10  # 中：200ms
                elif LEDSpeed == 3:
                    speedDelay = 5   # 快：100ms
            elif keyNum == 3:  # 如果k3按键按下：暂停/继续
                LEDPause = not LEDPause
                if LEDPause:
                    P2 = 0xff  # 暂停时全灭
                else:
                    P2 = 0xfe  # 继续时从初始状态开始
            elif keyNum == 4:  # 如果k4按键按下：重置
                LEDMode = 0  # 重置为初始模式
                LEDSpeed = 1  # 重置为初始速度
                LEDPause = False  # 重置为运行状态
                speedDelay = 25  # 重置延时
                chasePos = 0  # 重置追逐位置
                patternIndex = 0  # 重置图案索引
                P2 = 0xfe  # 重置为初始状态
        
        # 模拟定时器中断
        Timer0_ISR()
        
        # 打印LED状态
        print_led_status()

if __name__ == "__main__":
    main()
