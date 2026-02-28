#!/usr/bin/env python3
import pygame
import random
import sys

class MatrixRain:
    def __init__(self):
        # 初始化Pygame
        pygame.init()
        
        # 获取屏幕信息
        info = pygame.display.Info()
        self.WIDTH = info.current_w
        self.HEIGHT = info.current_h
        
        # 创建全屏幕窗口
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.NOFRAME | pygame.FULLSCREEN)
        pygame.display.set_caption("Matrix Rain Wallpaper")
        
        # 颜色定义
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.LIGHT_GREEN = (100, 255, 100)
        self.TRANSPARENT = (0, 0, 0, 0)
        
        # 字体设置
        self.font_size = 20
        self.font = pygame.font.SysFont("Consolas", self.font_size)
        
        # 加载中文字体支持
        try:
            self.chinese_font = pygame.font.SysFont("SimHei", self.font_size)
            self.use_chinese = True
        except:
            self.use_chinese = False
        
        # 数字雨参数
        self.columns = int(self.WIDTH / self.font_size)
        self.drops = [0 for _ in range(self.columns)]
        
        # 主循环控制
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 30
        
        # 拖影长度
        self.trail_length = 25
        
    def run(self):
        while self.running:
            # 控制帧率
            self.clock.tick(self.fps)
            
            # 处理事件
            self.handle_events()
            
            # 绘制背景（半透明黑色实现拖影）
            self.draw_background()
            
            # 绘制数字雨
            self.draw_rain()
            
            # 更新屏幕
            pygame.display.flip()
        
        # 退出程序
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # ESC键退出
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # 空格键暂停/继续
                elif event.key == pygame.K_SPACE:
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            break
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                            self.running = False
                            return
    
    def draw_background(self):
        # 半透明黑色填充实现拖影效果
        surf = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 20))  # 20是透明度值，0-255
        self.screen.blit(surf, (0, 0))
    
    def draw_rain(self):
        for i in range(self.columns):
            # 随机字符
            if self.use_chinese and random.random() > 0.5:
                # 中文字符范围
                char = chr(random.randint(0x4e00, 0x9fa5))
                font = self.chinese_font
            else:
                # ASCII字符范围
                char = chr(random.randint(33, 126))
                font = self.font
            
            # 随机颜色
            color = self.GREEN if random.random() > 0.1 else self.LIGHT_GREEN
            
            # 绘制当前字符
            text = font.render(char, True, color)
            x = i * self.font_size
            y = self.drops[i] * self.font_size
            self.screen.blit(text, (x, y))
            
            # 绘制拖影效果
            self.draw_trail(i, y, color, font)
            
            # 更新雨滴位置
            if y > self.HEIGHT and random.random() > 0.975:
                self.drops[i] = 0
            else:
                self.drops[i] += 1
    
    def draw_trail(self, column, y, color, font):
        for j in range(1, self.trail_length):
            trail_y = y - j * self.font_size
            if trail_y < 0:
                break
            
            # 拖影透明度逐渐降低
            alpha = max(0, 255 - j * 15)
            trail_color = (color[0], color[1], color[2], alpha)
            
            # 随机字符（可选不同字符）
            if self.use_chinese and random.random() > 0.5:
                trail_char = chr(random.randint(0x4e00, 0x9fa5))
            else:
                trail_char = chr(random.randint(33, 126))
            
            # 绘制拖影字符
            trail_text = font.render(trail_char, True, trail_color)
            trail_text.set_alpha(alpha)
            x = column * self.font_size
            self.screen.blit(trail_text, (x, trail_y))

if __name__ == "__main__":
    matrix_rain = MatrixRain()
    matrix_rain.run()
