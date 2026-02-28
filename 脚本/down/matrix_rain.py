import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 屏幕参数（可修改）
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix 数字雨")

# 颜色定义
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)

# 字体设置（选系统自带的等宽字体，也可换其他字体）
font = pygame.font.SysFont("Consolas", 18)

# 数字雨列的参数
columns = int(WIDTH / 20)  # 列数，20是字符宽度
drops = [0 for _ in range(columns)]  # 每列雨滴的起始位置

# 主循环
clock = pygame.time.Clock()
running = True
while running:
    # 控制帧率（可修改，数值越小速度越慢）
    clock.tick(30)

    # 处理退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 填充背景（半透明黑色，实现拖影效果）
    screen.fill((0, 0, 0, 15))

    # 绘制数字雨
    for i in range(columns):
        # 随机字符（可替换成中文、符号等）
        char = chr(random.randint(33, 126))
        # 绘制字符
        text = font.render(char, True, GREEN if random.random() > 0.1 else LIGHT_GREEN)
        screen.blit(text, (i * 20, drops[i] * 20))
        # 重置雨滴位置
        if drops[i] * 20 > HEIGHT and random.random() > 0.975:
            drops[i] = 0
        # 下移雨滴
        drops[i] += 1

    # 更新屏幕
    pygame.display.flip()

# 退出程序
pygame.quit()
sys.exit()