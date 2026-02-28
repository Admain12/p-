#!/usr/bin/env python3
import random
import sys
import time
import os

# 终端大小设置
WIDTH, HEIGHT = 80, 25

# 颜色定义
GREEN = '\033[92m'
LIGHT_GREEN = '\033[96m'
RESET = '\033[0m'

# 初始化雨滴位置
drops = [0 for _ in range(WIDTH)]

# 主循环
try:
    while True:
        # 清屏  
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 创建空屏幕
        screen = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
        # 绘制数字雨
        for i in range(WIDTH):
            # 随机字符
            char = chr(random.randint(33, 126))
            # 雨滴位置
            y = drops[i]
            
            # 绘制当前字符
            if 0 <= y < HEIGHT:
                screen[y][i] = char
            
            # 绘制拖影效果
            for j in range(1, 10):
                shadow_y = y - j
                if 0 <= shadow_y < HEIGHT:
                    if random.random() > 0.3:  # 拖影逐渐消失
                        screen[shadow_y][i] = '░'  # 半透明效果
                    else:
                        break
            
            # 重置雨滴位置
            if y >= HEIGHT + random.randint(0, 50) and random.random() > 0.975:
                drops[i] = 0
            else:
                drops[i] += 1
        
        # 打印屏幕
        for row in screen:
            line = ''.join(row)
            # 随机颜色
            color = GREEN if random.random() > 0.1 else LIGHT_GREEN
            print(color + line + RESET)
        
        # 控制速度
        time.sleep(0.1)
        
except KeyboardInterrupt:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[92mMatrix 数字雨已停止\033[0m")
    sys.exit(0)


