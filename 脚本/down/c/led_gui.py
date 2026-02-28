#!/usr/bin/env python3
"""
LED控制程序模拟器
使用tkinter实现LED控制程序的图形化模拟
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import json
import os
import random

class LEDSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("LED控制程序模拟器")
        self.root.geometry("800x550")
        self.root.resizable(False, False)
        
        # 设置窗口图标
        # 全局变量
        self.LEDMode = 0  # 模式：0=左移，1=右移，2=闪烁，3=呼吸灯，4=追逐，5=图案，6=随机，7=汉字显示
        self.LEDSpeed = 1  # 速度：1=慢，2=中，3=快
        self.LEDPause = False  # 暂停标志
        self.chasePos = 0  # 追逐模式位置
        self.patternIndex = 0  # 图案模式索引
        self.P2 = 0xfe  # LED状态
        
        # 呼吸灯相关
        self.brightness = 0
        self.direction = False
        self.breath_cnt = 0
        
        # 随机数种子
        self.randSeed = 12345
        
        # 汉字显示相关
        self.current_char = "中"  # 当前显示的汉字
        self.char_index = 0  # 汉字显示索引
        self.char_delay = 0  # 汉字显示延时
        self.char_matrix = []  # 汉字点阵矩阵
        self.char_display_mode = 0  # 汉字显示模式：0=静态，1=滚动
        self.current_char_var = None  # 当前汉字显示变量
        # 汉字点阵数据字典
        self.char_matrices = {
            "中": [
                0x00, 0x18, 0x18, 0x3C, 0x3C, 0x7E, 0xFF, 0xFF, 0xFF, 0x7E, 0x3C, 0x3C, 0x18, 0x18, 0x00, 0x00
            ],
            "国": [
                0x7E, 0xFF, 0xFF, 0xC3, 0xC3, 0xC3, 0xC3, 0xFF, 0xFF, 0xC3, 0xC3, 0xC3, 0xC3, 0xFF, 0x7E, 0x00
            ],
            "你": [
                0x08, 0x08, 0x1C, 0x1C, 0x2A, 0x2A, 0x7F, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x00, 0x00
            ],
            "好": [
                0x00, 0x00, 0x1F, 0x1F, 0x01, 0x01, 0x01, 0x7F, 0x01, 0x01, 0x01, 0x01, 0x1F, 0x1F, 0x00, 0x00
            ]
        }
        
        # LED颜色
        self.led_color = "#ff0000"  # 默认黄色
        self.led_off_color = "#333333"  # 熄灭颜色
        self.led_brightness = 100  # LED亮度（0-100）
        
        # 提前初始化必要的属性，避免属性未定义错误
        self.brightness_var = None
        self.brightness_label = None
        self.mode_var = None
        self.speed_var = None
        self.status_var = None
        self.color_var = None
        self.time_var = None
        self.leds = []
        
        # 预设图案
        self.patterns = [
            0x00, # 全灭
            0xff, # 全亮
            0x55, # 交替亮灭
            0xaa, # 交替灭亮
            0x0f, # 前4个亮
            0xf0, # 后4个亮
            0x81, # 两边亮
            0x42, # 中间两边亮
            0x24, # 中间亮
            0x18, # 中间两边亮
            0x3c, # 双箭头
            0x66, # 双竖线
            0x99, # 双横线
            0xe7, # 倒三角
            0x7e, # 正三角
            0x18, # 中间两个
            0xc3, # 两边两个
            0x03  # 最右边两个
        ]
        
        # 模式名称
        self.mode_names = ["左移", "右移", "闪烁", "呼吸灯", "追逐", "图案", "随机", "汉字显示"]
        
        # 速度名称
        self.speed_names = ["", "慢", "中", "快"]
        
        # 颜色选项
        self.color_options = {
            "红色": "#ff0000",
            "绿色": "#00ff00",
            "蓝色": "#0000ff",
            "黄色": "#ffff00",
            "紫色": "#ff00ff",
            "青色": "#00ffff",
            "橙色": "#ff8000",
            "粉色": "#ff69b4",
            "浅绿色": "#90ee90",
            "天蓝色": "#87ceeb"
        }
        
        # 主题设置
        self.themes = {
            "light": {
                "theme_color": "#4a7abc",
                "accent_color": "#ff6b6b",
                "bg_color": "#f0f0f0",
                "frame_bg": "#ffffff",
                "text_color": "#333333",
                "status_bg": "#f0f0f0",
                "info_bg": "#e9ecef"
            },
            "dark": {
                "theme_color": "#2c3e50",
                "accent_color": "#e74c3c",
                "bg_color": "#1a1a1a",
                "frame_bg": "#2d2d2d",
                "text_color": "#ffffff",
                "status_bg": "#2d2d2d",
                "info_bg": "#3d3d3d"
            }
        }
        # 默认亮色主题
        self.theme = "light"
        # 当前主题颜色
        self.theme_color = self.themes[self.theme]["theme_color"]
        self.accent_color = self.themes[self.theme]["accent_color"]
        
        # 配置文件路径
        self.config_file = "led_config.json"
        
        # 运行时间
        self.run_time = 0
        self.start_time = time.time()
        
        # 初始化运行状态
        self.running = True
        
        # 绑定键盘事件
        self.root.bind('<Key>', self.on_key_press)
        
        # 绑定鼠标事件（预留）
        # self.root.bind('<Button-1>', self.on_mouse_click)
        
        # 设置窗口背景
        self.root.configure(bg=self.themes[self.theme]["bg_color"])
        
        # 提前创建必要的属性，确保load_config能访问到它们
        self.brightness_var = tk.IntVar(value=self.led_brightness)
        self.brightness_label = None
        self.mode_var = tk.StringVar(value=self.mode_names[self.LEDMode])
        self.speed_var = tk.StringVar(value=self.speed_names[self.LEDSpeed])
        self.status_var = tk.StringVar(value="运行")
        self.color_var = tk.StringVar(value="黄色")
        self.time_var = tk.StringVar(value="00:00:00")
        self.leds = []
        
        # 创建界面
        self.create_widgets()
        
        # 加载配置
        self.load_config()
        
        # 启动模拟线程
        self.thread = threading.Thread(target=self.simulate, daemon=True)
        self.thread.start()
    
    def create_widgets(self):
        try:
            # 确保必要的属性被初始化
            if not hasattr(self, 'brightness_var'):
                self.brightness_var = tk.IntVar(value=self.led_brightness)
            if not hasattr(self, 'brightness_label'):
                self.brightness_label = None
            if not hasattr(self, 'mode_var'):
                self.mode_var = tk.StringVar(value=self.mode_names[self.LEDMode])
            if not hasattr(self, 'speed_var'):
                self.speed_var = tk.StringVar(value=self.speed_names[self.LEDSpeed])
            if not hasattr(self, 'status_var'):
                self.status_var = tk.StringVar(value="运行")
            if not hasattr(self, 'color_var'):
                self.color_var = tk.StringVar(value="红色")
            if not hasattr(self, 'time_var'):
                self.time_var = tk.StringVar(value="00:00:00")
            if not hasattr(self, 'leds'):
                self.leds = []
            
            # 创建样式
            self.create_styles()
            
            # 创建菜单栏
            menubar = tk.Menu(self.root, bg=self.theme_color, fg="white", activebackground=self.accent_color, activeforeground="white")
            self.root.config(menu=menubar)
            
            # 文件菜单
            file_menu = tk.Menu(menubar, tearoff=0, bg="#f0f0f0", fg="#333333")
            menubar.add_cascade(label="文件", menu=file_menu, font=('Arial', 10))
            file_menu.add_command(label="保存配置", command=self.save_config, font=('Arial', 9))
            file_menu.add_command(label="加载配置", command=self.load_config, font=('Arial', 9))
            file_menu.add_separator()
            file_menu.add_command(label="退出", command=self.on_closing, font=('Arial', 9))
            
            # 选项菜单
            option_menu = tk.Menu(menubar, tearoff=0, bg="#f0f0f0", fg="#333333")
            menubar.add_cascade(label="选项", menu=option_menu, font=('Arial', 10))
            
            # 颜色子菜单
            color_menu = tk.Menu(option_menu, tearoff=0, bg="#f0f0f0", fg="#333333")
            option_menu.add_cascade(label="LED颜色", menu=color_menu, font=('Arial', 9))
            for color_name, color_value in self.color_options.items():
                color_menu.add_command(label=color_name, command=lambda c=color_value: self.change_led_color(c), font=('Arial', 9))
            
            # 主题子菜单
            theme_menu = tk.Menu(option_menu, tearoff=0, bg="#f0f0f0", fg="#333333")
            option_menu.add_cascade(label="主题", menu=theme_menu, font=('Arial', 9))
            theme_menu.add_command(label="亮色主题", command=lambda: self.change_theme("light"), font=('Arial', 9))
            theme_menu.add_command(label="暗色主题", command=lambda: self.change_theme("dark"), font=('Arial', 9))
            
            # 汉字编辑子菜单
            char_menu = tk.Menu(option_menu, tearoff=0, bg="#f0f0f0", fg="#333333")
            option_menu.add_cascade(label="汉字编辑", menu=char_menu, font=('Arial', 9))
            char_menu.add_command(label="编辑汉字", command=self.open_char_editor, font=('Arial', 9))
            char_menu.add_command(label="更改显示汉字", command=self.change_display_char, font=('Arial', 9))
            
            # 帮助菜单
            help_menu = tk.Menu(menubar, tearoff=0, bg="#f0f0f0", fg="#333333")
            menubar.add_cascade(label="帮助", menu=help_menu, font=('Arial', 10))
            help_menu.add_command(label="使用说明", command=self.show_help, font=('Arial', 9))
            help_menu.add_command(label="关于", command=self.show_about, font=('Arial', 9))
            
            # 顶部状态栏
            status_frame = ttk.Frame(self.root, padding=(15, 10), style="StatusFrame.TFrame")
            status_frame.pack(fill=tk.X, pady=(10, 0))
            
            # 模式显示
            ttk.Label(status_frame, text="模式: ", style="StatusLabel.TLabel").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
            self.mode_var = tk.StringVar(value=self.mode_names[self.LEDMode])
            mode_label = ttk.Label(status_frame, textvariable=self.mode_var, width=10, style="StatusValue.TLabel")
            mode_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
            
            # 速度显示
            ttk.Label(status_frame, text="速度: ", style="StatusLabel.TLabel").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
            self.speed_var = tk.StringVar(value=self.speed_names[self.LEDSpeed])
            speed_label = ttk.Label(status_frame, textvariable=self.speed_var, width=10, style="StatusValue.TLabel")
            speed_label.grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
            
            # 状态显示
            ttk.Label(status_frame, text="状态: ", style="StatusLabel.TLabel").grid(row=0, column=4, sticky=tk.W, padx=(0, 5))
            self.status_var = tk.StringVar(value="运行")
            status_label = ttk.Label(status_frame, textvariable=self.status_var, width=10, style="StatusValue.TLabel")
            status_label.grid(row=0, column=5, sticky=tk.W, padx=(0, 20))
            
            # LED颜色显示
            ttk.Label(status_frame, text="颜色: ", style="StatusLabel.TLabel").grid(row=0, column=6, sticky=tk.W, padx=(0, 5))
            self.color_var = tk.StringVar(value="红色")
            color_label = ttk.Label(status_frame, textvariable=self.color_var, width=10, style="StatusValue.TLabel")
            color_label.grid(row=0, column=7, sticky=tk.W)
            
            # LED亮度显示和调节
            ttk.Label(status_frame, text="亮度: ", style="StatusLabel.TLabel").grid(row=0, column=8, sticky=tk.W, padx=(20, 5))
            self.brightness_var = tk.IntVar(value=self.led_brightness)
            brightness_scale = ttk.Scale(status_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=self.brightness_var, length=100, command=self.on_brightness_change)
            brightness_scale.grid(row=0, column=9, sticky=tk.W)
            self.brightness_label = ttk.Label(status_frame, text=f"{self.led_brightness}%", width=5, style="StatusValue.TLabel")
            self.brightness_label.grid(row=0, column=10, sticky=tk.W, padx=(5, 20))
            
            # 运行时间显示
            ttk.Label(status_frame, text="运行时间: ", style="StatusLabel.TLabel").grid(row=0, column=11, sticky=tk.W, padx=(0, 5))
            self.time_var = tk.StringVar(value="00:00:00")
            time_label = ttk.Label(status_frame, textvariable=self.time_var, width=10, style="StatusValue.TLabel")
            time_label.grid(row=0, column=12, sticky=tk.W)
            

            
            # LED显示区域
            led_frame = ttk.Frame(self.root, padding=(20, 20), style="LEDFRAME.TFrame")
            led_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # LED标题
            title_frame = ttk.Frame(led_frame)
            title_frame.pack(fill=tk.X, pady=(0, 20))
            ttk.Label(title_frame, text="LED状态模拟", style="Title.TLabel").pack(side=tk.LEFT)
            
            # 汉字显示提示
            if self.LEDMode == 7:
                self.char_status_var = tk.StringVar(value=f"正在显示 '{self.current_char}' 字 - 第 1/16 行")
                ttk.Label(title_frame, textvariable=self.char_status_var, style="LEDLabel.TLabel").pack(side=tk.RIGHT)
            
            # LED灯
            self.leds = []
            leds_frame = ttk.Frame(led_frame, style="LEDSFrame.TFrame")
            leds_frame.pack()
            
            # LED标签
            for i in range(7, -1, -1):
                ttk.Label(leds_frame, text=f"P2.{i}", style="LEDLabel.TLabel").grid(row=1, column=7-i, padx=10, pady=(0, 5))
            
            # LED灯
            for i in range(7, -1, -1):  # 从P2.7到P2.0
                # 创建LED灯容器
                led_container = ttk.Frame(leds_frame, padding=(5, 5), style="LEDContainer.TFrame")
                led_container.grid(row=0, column=7-i, padx=10, pady=10)
                
                # 创建LED灯 - 使用更真实的形状
                led = ttk.Label(led_container, text="", style="LED.TLabel")
                led.pack(fill=tk.BOTH, expand=True)
                self.leds.append(led)
            
            # 按键区域
            buttons_frame = ttk.Frame(self.root, padding=(10, 10), style="ButtonsFrame.TFrame")
            buttons_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
            
            # 按键1：切换模式
            mode_button = ttk.Button(buttons_frame, text="切换模式 (K1)", command=self.toggle_mode, style="Primary.TButton")
            mode_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)
            mode_button.bind('<Enter>', lambda e: self.show_tooltip(e, "切换LED模式\n当前模式: " + self.mode_names[self.LEDMode]))
            mode_button.bind('<Leave>', self.hide_tooltip)
            
            # 按键2：切换速度
            speed_button = ttk.Button(buttons_frame, text="切换速度 (K2)", command=self.toggle_speed, style="Secondary.TButton")
            speed_button.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
            speed_button.bind('<Enter>', lambda e: self.show_tooltip(e, "切换LED速度\n当前速度: " + self.speed_names[self.LEDSpeed]))
            speed_button.bind('<Leave>', self.hide_tooltip)
            
            # 按键3：暂停/继续
            pause_button = ttk.Button(buttons_frame, text="暂停/继续 (K3)", command=self.toggle_pause, style="Accent.TButton")
            pause_button.grid(row=0, column=2, padx=5, pady=5, sticky=tk.EW)
            pause_button.bind('<Enter>', lambda e: self.show_tooltip(e, "暂停或继续LED动画\n当前状态: " + ("暂停" if self.LEDPause else "运行")))
            pause_button.bind('<Leave>', self.hide_tooltip)
            
            # 按键4：重置
            reset_button = ttk.Button(buttons_frame, text="重置 (K4)", command=self.reset, style="Danger.TButton")
            reset_button.grid(row=0, column=3, padx=5, pady=5, sticky=tk.EW)
            reset_button.bind('<Enter>', lambda e: self.show_tooltip(e, "重置LED到初始状态\n包括模式、速度和运行时间"))
            reset_button.bind('<Leave>', self.hide_tooltip)
            
            # 底部信息栏
            info_frame = ttk.Frame(self.root, padding=(15, 8), style="InfoFrame.TFrame")
            info_frame.pack(fill=tk.X, side=tk.BOTTOM)
            
            ttk.Label(info_frame, text="按1-4键模拟按键操作 | 按空格键暂停/继续", style="InfoLabel.TLabel").pack(side=tk.LEFT)
            ttk.Label(info_frame, text="LED控制程序模拟器 v2.0", style="InfoLabel.TLabel").pack(side=tk.RIGHT)
            
            # 设置列权重
            for i in range(4):
                buttons_frame.columnconfigure(i, weight=1)
            
            # 启动时间更新线程
            self.time_thread = threading.Thread(target=self.update_time, daemon=True)
            self.time_thread.start()
        except Exception as e:
            print(f"创建控件时出错: {e}")
            # 确保brightness_var被创建，即使其他控件创建失败
            if not hasattr(self, 'brightness_var'):
                self.brightness_var = tk.IntVar(value=self.led_brightness)
    
    def toggle_mode(self):
        """切换模式"""
        self.LEDMode = (self.LEDMode + 1) % 8
        self.mode_var.set(self.mode_names[self.LEDMode])
        self.chasePos = 0
        self.patternIndex = 0
        self.update_leds()
    
    def toggle_speed(self):
        """切换速度"""
        self.LEDSpeed = (self.LEDSpeed + 1) % 4
        if self.LEDSpeed == 0:
            self.LEDSpeed = 1
        self.speed_var.set(self.speed_names[self.LEDSpeed])
    
    def toggle_pause(self):
        """暂停/继续"""
        self.LEDPause = not self.LEDPause
        if self.LEDPause:
            self.status_var.set("暂停")
            # 对于汉字显示模式，不强制设置全灭，保持当前显示
            if self.LEDMode != 7:
                self.P2 = 0xff  # 暂停时全灭
        else:
            self.status_var.set("运行")
            self.P2 = 0xfe  # 继续时从初始状态开始
        self.update_leds()
    
    def reset(self):
        """重置"""
        self.LEDMode = 0
        self.LEDSpeed = 1
        self.LEDPause = False
        self.chasePos = 0
        self.patternIndex = 0
        self.P2 = 0xfe
        self.brightness = 0
        self.direction = False
        self.breath_cnt = 0
        self.randSeed = 12345
        
        # 重置运行时间
        self.start_time = time.time()
        self.time_var.set("00:00:00")
        
        # 更新显示
        self.mode_var.set(self.mode_names[self.LEDMode])
        self.speed_var.set(self.speed_names[self.LEDSpeed])
        self.status_var.set("运行")
        self.update_leds()
    
    def create_styles(self):
        """创建自定义样式"""
        style = ttk.Style()
        
        # 获取当前主题颜色
        current_theme = self.themes[self.theme]
        
        # 状态栏样式
        style.configure("StatusFrame.TFrame", background=current_theme["status_bg"])
        style.configure("StatusLabel.TLabel", font=('Arial', 10, 'bold'), foreground=current_theme["text_color"], background=current_theme["status_bg"])
        style.configure("StatusValue.TLabel", font=('Arial', 10), foreground=current_theme["theme_color"], background=current_theme["status_bg"], relief=tk.SUNKEN, padding=(5, 2))
        
        # LED区域样式
        style.configure("LEDFRAME.TFrame", background=current_theme["frame_bg"], relief=tk.RAISED, borderwidth=2)
        style.configure("LEDSFrame.TFrame", background=current_theme["frame_bg"])
        style.configure("Title.TLabel", font=('Arial', 14, 'bold'), foreground=current_theme["theme_color"], background=current_theme["frame_bg"])
        style.configure("LEDLabel.TLabel", font=('Arial', 9), foreground=current_theme["text_color"], background=current_theme["frame_bg"])
        
        # LED容器样式 - 模拟LED底座
        style.configure("LEDContainer.TFrame", background=current_theme["frame_bg"], relief=tk.RAISED, borderwidth=2)
        
        # LED灯样式 - 更真实的LED形状
        style.configure("LED.TLabel", background="#333333", relief=tk.RAISED, borderwidth=3, padding=(15, 15), width=5, height=3)
        
        # 按钮区域样式
        style.configure("ButtonsFrame.TFrame", background=current_theme["status_bg"])
        
        # 按钮样式
        style.configure("TButton", padding=(10, 5), font=('Arial', 10), relief=tk.RAISED)
        style.configure("Primary.TButton", background=current_theme["theme_color"], foreground="white")
        style.map("Primary.TButton", background=[('active', current_theme["accent_color"])])
        style.configure("Secondary.TButton", background="#6c757d", foreground="white")
        style.map("Secondary.TButton", background=[('active', "#5a6268")])
        style.configure("Accent.TButton", background="#28a745", foreground="white")
        style.map("Accent.TButton", background=[('active', "#218838")])
        style.configure("Danger.TButton", background="#dc3545", foreground="white")
        style.map("Danger.TButton", background=[('active', "#c82333")])
        
        # 信息栏样式
        style.configure("InfoFrame.TFrame", background=current_theme["info_bg"])
        style.configure("InfoLabel.TLabel", font=('Arial', 9), foreground=current_theme["text_color"], background=current_theme["info_bg"])
        
        # 工具提示样式
        style.configure("Tooltip.TFrame", background="#333333")
        style.configure("Tooltip.TLabel", font=('Arial', 9), foreground="white", background="#333333")
    
    def update_leds(self):
        """更新LED显示"""
        # 根据亮度计算当前的LED颜色
        base_color = self.hex_to_rgb(self.led_color)
        off_color = self.hex_to_rgb(self.led_off_color)
        
        # 计算亮度调整后的颜色
        r = int(base_color[0] * (self.led_brightness / 100))
        g = int(base_color[1] * (self.led_brightness / 100))
        b = int(base_color[2] * (self.led_brightness / 100))
        current_led_color = self.rgb_to_hex(r, g, b)
        
        for i in range(8):
            if (self.P2 & (1 << i)) != 0:
                # LED亮
                if self.leds[7-i].cget('background') != current_led_color:
                    # 添加动画效果
                    self.animate_led(7-i, self.led_off_color, current_led_color)
            else:
                # LED灭
                if self.leds[7-i].cget('background') != self.led_off_color:
                    # 添加动画效果
                    self.animate_led(7-i, current_led_color, self.led_off_color)
    
    def animate_led(self, index, from_color, to_color):
        """LED动画过渡效果"""
        # 简单的颜色过渡动画
        steps = 5
        for step in range(steps + 1):
            # 计算当前颜色
            r1, g1, b1 = self.hex_to_rgb(from_color)
            r2, g2, b2 = self.hex_to_rgb(to_color)
            r = int(r1 + (r2 - r1) * step / steps)
            g = int(g1 + (g2 - g1) * step / steps)
            b = int(b1 + (b2 - b1) * step / steps)
            current_color = self.rgb_to_hex(r, g, b)
            
            # 更新LED颜色
            def update_color(c, idx=index):
                if idx < len(self.leds):
                    self.leds[idx].configure(background=c)
            
            self.root.after(int(step * 20), update_color, current_color)
    
    def hex_to_rgb(self, hex_color):
        """将十六进制颜色转换为RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r, g, b):
        """将RGB颜色转换为十六进制"""
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def on_brightness_change(self, value):
        """处理亮度调节事件"""
        self.led_brightness = int(float(value))
        self.brightness_label.config(text=f"{self.led_brightness}%")
        # 更新LED显示
        self.update_leds()
    
    def change_theme(self, theme):
        """切换主题"""
        if theme != self.theme:
            self.theme = theme
            # 更新主题颜色
            self.theme_color = self.themes[theme]["theme_color"]
            self.accent_color = self.themes[theme]["accent_color"]
            
            # 更新窗口背景
            self.root.configure(bg=self.themes[theme]["bg_color"])
            
            # 重新创建样式
            self.create_styles()
            
            # 更新LED显示
            self.update_leds()
            
            # 保存主题设置
            self.save_config()
            
            messagebox.showinfo("成功", f"已切换到{"亮色" if theme == "light" else "暗色"}主题")
    
    def show_tooltip(self, event, text):
        """显示工具提示"""
        # 创建工具提示窗口
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)  # 无标题栏
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")  # 位置
        
        # 设置工具提示样式
        tooltip_frame = ttk.Frame(self.tooltip, padding=(10, 5), style="Tooltip.TFrame")
        tooltip_frame.pack()
        
        # 添加提示文本
        ttk.Label(tooltip_frame, text=text, style="Tooltip.TLabel").pack()
        
        # 设置工具提示为临时窗口
        self.tooltip.attributes('-topmost', True)
    
    def hide_tooltip(self, event):
        """隐藏工具提示"""
        if hasattr(self, 'tooltip') and self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
    
    def update_time(self):
        """更新运行时间"""
        while self.running:
            if not self.LEDPause:
                elapsed = int(time.time() - self.start_time)
                hours = elapsed // 3600
                minutes = (elapsed % 3600) // 60
                seconds = elapsed % 60
                time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                # 使用线程安全的方式更新GUI
                def update_time_gui():
                    try:
                        if hasattr(self, 'time_var'):
                            self.time_var.set(time_str)
                    except Exception:
                        pass
                
                # 尝试使用after方法更新GUI
                try:
                    if hasattr(self, 'root'):
                        self.root.after(0, update_time_gui)
                except Exception:
                    pass
            time.sleep(1)
    
    def simulate(self):
        """模拟LED控制程序"""
        while self.running:
            if not self.LEDPause:
                # 根据模式更新LED
                if self.LEDMode == 0:  # 左移
                    self.P2 = ((self.P2 << 1) | (self.P2 >> 7)) & 0xff
                elif self.LEDMode == 1:  # 右移
                    self.P2 = ((self.P2 >> 1) | (self.P2 << 7)) & 0xff
                elif self.LEDMode == 2:  # 闪烁
                    self.P2 = ~self.P2 & 0xff
                elif self.LEDMode == 3:  # 呼吸灯
                    self.breath_cnt += 1
                    if self.breath_cnt >= 20:  # 增加呼吸灯的平滑度
                        self.breath_cnt = 0
                        if not self.direction:
                            self.brightness += 1
                            if self.brightness >= 20:  # 增加亮度级别
                                self.direction = True
                        else:
                            self.brightness -= 1
                            if self.brightness <= 0:
                                self.direction = False
                    # 根据亮度更新LED
                    if self.brightness == 0:
                        self.P2 = 0xff
                    elif self.brightness == 20:
                        self.P2 = 0x00
                    else:
                        # 实现平滑的亮度渐变效果
                        # 根据亮度计算当前的颜色
                        base_color = self.hex_to_rgb(self.led_color)
                        off_color = self.hex_to_rgb(self.led_off_color)
                        
                        # 计算当前亮度对应的颜色，考虑用户设置的亮度级别
                        r = int(base_color[0] * (self.brightness / 20) * (self.led_brightness / 100) + off_color[0] * (1 - self.brightness / 20))
                        g = int(base_color[1] * (self.brightness / 20) * (self.led_brightness / 100) + off_color[1] * (1 - self.brightness / 20))
                        b = int(base_color[2] * (self.brightness / 20) * (self.led_brightness / 100) + off_color[2] * (1 - self.brightness / 20))
                        
                        # 更新所有LED的颜色
                        for i in range(8):
                            self.leds[i].configure(background=self.rgb_to_hex(r, g, b))
                        
                        # 跳过默认的update_leds调用，因为我们已经手动更新了LED颜色
                        continue
                elif self.LEDMode == 4:  # 追逐
                    self.P2 = 0xff
                    self.P2 &= ~(0x01 << self.chasePos)
                    self.chasePos = (self.chasePos + 1) % 8
                elif self.LEDMode == 5:  # 图案
                    self.P2 = self.patterns[self.patternIndex]
                    self.patternIndex = (self.patternIndex + 1) % len(self.patterns)
                elif self.LEDMode == 6:  # 随机
                    self.randSeed = (self.randSeed * 1103515245 + 12345) % 32768
                    self.P2 = self.randSeed % 256
                elif self.LEDMode == 7:  # 汉字显示
                    if not self.char_matrix:
                        # 生成汉字点阵
                        self.generate_char_matrix(self.current_char)
                    
                    # 显示当前帧
                    if self.char_index < len(self.char_matrix):
                        self.P2 = self.char_matrix[self.char_index]
                        # 更新汉字显示状态提示
                        if hasattr(self, 'char_status_var'):
                            self.char_status_var.set(f"正在显示 '{self.current_char}' 字 - 第 {self.char_index + 1}/16 行")
                        self.char_index += 1
                    else:
                        self.char_index = 0
                        # 更新汉字显示状态提示
                        if hasattr(self, 'char_status_var'):
                            self.char_status_var.set(f"正在显示 '{self.current_char}' 字 - 第 1/16 行")
                        # 不清空点阵数据，而是重新开始显示，实现持续显示效果
                
                # 更新LED显示
                self.root.after(0, self.update_leds)
            else:
                # 即使在暂停状态下，对于汉字显示模式也需要初始化和显示
                if self.LEDMode == 7:
                    if not self.char_matrix:
                        # 生成汉字点阵
                        self.generate_char_matrix(self.current_char)
                    
                    # 显示第一帧
                    if self.char_matrix:
                        self.P2 = self.char_matrix[0]
                        self.char_index = 1
                        # 更新LED显示
                        self.root.after(0, self.update_leds)
            
            # 根据速度设置延时
            if self.LEDMode == 7:  # 汉字显示模式
                # 为汉字显示设置适中的速度，让每一行都能清晰可见
                delay = 0.8  # 慢
                if self.LEDSpeed == 2:
                    delay = 0.5  # 中
                elif self.LEDSpeed == 3:
                    delay = 0.3  # 快
            else:
                delay = 0.5  # 慢
                if self.LEDSpeed == 2:
                    delay = 0.2  # 中
                elif self.LEDSpeed == 3:
                    delay = 0.1  # 快
            
            time.sleep(delay)
    
    def on_closing(self):
        """关闭窗口时的处理"""
        self.running = False
        self.save_config()  # 退出时自动保存配置
        # 给线程时间停止
        time.sleep(0.1)
        self.root.destroy()
    
    def save_config(self):
        """保存配置"""
        try:
            config = {
                "LEDMode": self.LEDMode,
                "LEDSpeed": self.LEDSpeed,
                "led_color": self.led_color,
                "led_brightness": self.led_brightness,
                "theme": self.theme
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("成功", "配置保存成功！")
        except Exception as e:
            messagebox.showerror("错误", f"配置保存失败: {e}")
    
    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.LEDMode = config.get("LEDMode", 0)
                self.LEDSpeed = config.get("LEDSpeed", 1)
                self.led_color = config.get("led_color", "#ff0000")
                self.led_brightness = config.get("led_brightness", 100)
                # 确保主题值有效
                theme_from_config = config.get("theme", "light")
                if theme_from_config in self.themes:
                    self.theme = theme_from_config
                else:
                    self.theme = "light"
                
                # 更新主题颜色
                self.theme_color = self.themes[self.theme]["theme_color"]
                self.accent_color = self.themes[self.theme]["accent_color"]
                
                # 更新窗口背景
                self.root.configure(bg=self.themes[self.theme]["bg_color"])
                
                # 确保brightness_var存在
                if not hasattr(self, 'brightness_var') or self.brightness_var is None:
                    self.brightness_var = tk.IntVar(value=self.led_brightness)
                else:
                    # 更新亮度控件
                    self.brightness_var.set(self.led_brightness)
                
                # 重新创建样式
                self.create_styles()
                
                # 确保brightness_label存在
                if hasattr(self, 'brightness_label') and self.brightness_label is not None:
                    self.brightness_label.config(text=f"{self.led_brightness}%")
                
                # 确保mode_var存在
                if not hasattr(self, 'mode_var') or self.mode_var is None:
                    self.mode_var = tk.StringVar(value=self.mode_names[self.LEDMode])
                else:
                    # 更新显示
                    self.mode_var.set(self.mode_names[self.LEDMode])
                
                # 确保speed_var存在
                if not hasattr(self, 'speed_var') or self.speed_var is None:
                    self.speed_var = tk.StringVar(value=self.speed_names[self.LEDSpeed])
                else:
                    self.speed_var.set(self.speed_names[self.LEDSpeed])
                
                # 确保color_var存在
                if not hasattr(self, 'color_var') or self.color_var is None:
                    self.color_var = tk.StringVar(value="红色")
                else:
                    # 更新颜色名称
                    for color_name, color_value in self.color_options.items():
                        if color_value == self.led_color:
                            self.color_var.set(color_name)
                            break
                    else:
                        self.color_var.set("红色")
                
                # 确保leds存在
                if not hasattr(self, 'leds'):
                    self.leds = []
                
                # 检查update_leds方法是否存在且leds不为空
                if hasattr(self, 'update_leds') and self.leds:
                    self.update_leds()
                messagebox.showinfo("成功", "配置加载成功！")
            else:
                messagebox.showinfo("提示", "配置文件不存在，使用默认配置。")
        except Exception as e:
            messagebox.showerror("错误", f"配置加载失败: {e}")
    
    def change_led_color(self, color):
        """更改LED颜色"""
        self.led_color = color
        # 更新颜色名称
        for color_name, color_value in self.color_options.items():
            if color_value == color:
                self.color_var.set(color_name)
                break
        self.update_leds()
    
    def on_key_press(self, event):
        """键盘事件处理"""
        key = event.keysym
        if key == '1':
            self.toggle_mode()
        elif key == '2':
            self.toggle_speed()
        elif key == '3':
            self.toggle_pause()
        elif key == '4':
            self.reset()
        elif key == 'space':
            self.toggle_pause()
        elif key == 'F1':
            # 直接切换到汉字显示模式
            self.LEDMode = 7
            self.mode_var.set(self.mode_names[self.LEDMode])
            self.char_index = 0
            self.char_matrix = []
            self.update_leds()
    
    def show_help(self):
        """显示使用说明"""
        help_text = "使用说明：\n\n"
        help_text += "1. 按键操作：\n"
        help_text += "   K1 (或数字键1)：切换LED模式\n"
        help_text += "   K2 (或数字键2)：切换速度等级\n"
        help_text += "   K3 (或数字键3)：暂停/继续\n"
        help_text += "   K4 (或数字键4)：重置为初始状态\n"
        help_text += "   空格键：快速暂停/继续\n\n"
        help_text += "2. 模式说明：\n"
        help_text += "   0: 左移 - LED从右向左移动\n"
        help_text += "   1: 右移 - LED从左向右移动\n"
        help_text += "   2: 闪烁 - LED全部闪烁\n"
        help_text += "   3: 呼吸灯 - LED亮度渐变\n"
        help_text += "   4: 追逐 - 单个LED追逐移动\n"
        help_text += "   5: 图案 - 显示预设图案\n"
        help_text += "   6: 随机 - 随机点亮LED\n"
        help_text += "   7: 汉字显示 - 显示汉字\n\n"
        help_text += "3. 快捷键说明：\n"
        help_text += "   F1键: 直接切换到汉字显示模式\n\n"
        help_text += "3. 速度说明：\n"
        help_text += "   1: 慢 - 0.5秒间隔\n"
        help_text += "   2: 中 - 0.2秒间隔\n"
        help_text += "   3: 快 - 0.1秒间隔\n\n"
        help_text += "4. 其他功能：\n"
        help_text += "   文件菜单：保存/加载配置\n"
        help_text += "   选项菜单：更改LED颜色\n"
        help_text += "   帮助菜单：使用说明和关于信息"
        messagebox.showinfo("使用说明", help_text)
    
    def generate_char_matrix(self, char):
        """生成汉字点阵矩阵"""
        # 获取对应汉字的点阵数据
        if char in self.char_matrices:
            self.char_matrix = self.char_matrices[char]
        else:
            # 默认显示"中"字
            self.char_matrix = self.char_matrices.get("中", [0x00] * 16)
    
    def open_char_editor(self):
        """打开汉字编辑器"""
        # 创建汉字编辑器窗口
        editor_window = tk.Toplevel(self.root)
        editor_window.title("汉字编辑器")
        editor_window.geometry("400x400")
        editor_window.resizable(False, False)
        editor_window.transient(self.root)
        editor_window.grab_set()
        
        # 设置窗口背景
        current_theme = self.themes[self.theme]
        editor_window.configure(bg=current_theme["bg_color"])
        
        # 创建标题
        title_frame = ttk.Frame(editor_window, padding=(10, 10))
        title_frame.pack(fill=tk.X)
        ttk.Label(title_frame, text="汉字点阵编辑器", font=('Arial', 12, 'bold'), foreground=current_theme["theme_color"]).pack()
        
        # 创建输入区域
        input_frame = ttk.Frame(editor_window, padding=(10, 10))
        input_frame.pack(fill=tk.X)
        ttk.Label(input_frame, text="输入汉字:", foreground=current_theme["text_color"]).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        char_var = tk.StringVar(value=self.current_char)
        char_entry = ttk.Entry(input_frame, textvariable=char_var, width=10, font=('Arial', 10))
        char_entry.grid(row=0, column=1, sticky=tk.W)
        
        # 创建点阵编辑区域
        editor_frame = ttk.Frame(editor_window, padding=(10, 10))
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建16x16点阵编辑器
        matrix_buttons = []
        matrix = [[0 for _ in range(8)] for _ in range(16)]  # 16行8列
        
        # 加载当前汉字的点阵
        if self.current_char:
            self.generate_char_matrix(self.current_char)
            if self.char_matrix:
                for i in range(min(16, len(self.char_matrix))):
                    row_data = self.char_matrix[i]
                    for j in range(8):
                        matrix[i][j] = 1 if (row_data & (1 << (7 - j))) else 0
        
        # 创建点阵按钮
        for i in range(16):
            row_buttons = []
            for j in range(8):
                btn = ttk.Button(
                    editor_frame, 
                    width=3, 
                    style="LED.TLabel"
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                
                # 设置初始状态
                if matrix[i][j]:
                    btn.configure(background=self.led_color)
                else:
                    btn.configure(background=self.led_off_color)
                
                # 绑定点击事件
                def toggle_dot(i=i, j=j, btn=btn):
                    matrix[i][j] = 1 - matrix[i][j]
                    if matrix[i][j]:
                        btn.configure(background=self.led_color)
                    else:
                        btn.configure(background=self.led_off_color)
                
                btn.bind('<Button-1>', lambda e, i=i, j=j, btn=btn: toggle_dot(i, j, btn))
                row_buttons.append(btn)
            matrix_buttons.append(row_buttons)
        
        # 创建按钮区域
        buttons_frame = ttk.Frame(editor_window, padding=(10, 10))
        buttons_frame.pack(fill=tk.X)
        
        def save_char():
            """保存汉字点阵"""
            char = char_var.get().strip()
            if not char:
                messagebox.showerror("错误", "请输入汉字")
                return
            
            # 生成点阵数据
            new_matrix = []
            for i in range(16):
                row_data = 0
                for j in range(8):
                    if matrix[i][j]:
                        row_data |= (1 << (7 - j))
                new_matrix.append(row_data)
            
            # 更新当前汉字和点阵
            self.current_char = char
            self.char_matrix = new_matrix
            # 保存到字典中，实现持久化
            self.char_matrices[char] = new_matrix
            
            # 如果当前是汉字模式，立即更新显示
            if self.LEDMode == 7:
                self.char_index = 0
                self.update_leds()
            
            messagebox.showinfo("成功", f"汉字'{char}'的点阵已保存")
            editor_window.destroy()
        
        def load_char():
            """加载汉字点阵"""
            char = char_var.get().strip()
            if not char:
                messagebox.showerror("错误", "请输入汉字")
                return
            
            # 生成汉字点阵
            self.generate_char_matrix(char)
            if self.char_matrix:
                # 更新矩阵和按钮
                for i in range(min(16, len(self.char_matrix))):
                    row_data = self.char_matrix[i]
                    for j in range(8):
                        matrix[i][j] = 1 if (row_data & (1 << (7 - j))) else 0
                        if matrix[i][j]:
                            matrix_buttons[i][j].configure(background=self.led_color)
                        else:
                            matrix_buttons[i][j].configure(background=self.led_off_color)
                messagebox.showinfo("成功", f"已加载汉字'{char}'的点阵")
            else:
                messagebox.showinfo("提示", f"汉字'{char}'的点阵不存在，使用默认值")
        
        # 按钮
        ttk.Button(buttons_frame, text="加载", command=load_char, style="Secondary.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="保存", command=save_char, style="Primary.TButton").pack(side=tk.RIGHT, padx=5)
    
    def change_display_char(self):
        """更改显示的汉字"""
        # 创建输入对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("更改显示汉字")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 设置窗口背景
        current_theme = self.themes[self.theme]
        dialog.configure(bg=current_theme["bg_color"])
        
        # 创建输入区域
        input_frame = ttk.Frame(dialog, padding=(20, 20))
        input_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(input_frame, text="请输入要显示的汉字:", foreground=current_theme["text_color"]).pack(pady=(0, 10))
        
        char_var = tk.StringVar(value=self.current_char)
        char_entry = ttk.Entry(input_frame, textvariable=char_var, width=20, font=('Arial', 10))
        char_entry.pack(pady=(0, 20))
        char_entry.focus_set()
        
        # 创建按钮
        def confirm():
            char = char_var.get().strip()
            if not char:
                messagebox.showerror("错误", "请输入汉字")
                return
            
            self.current_char = char
            # 重置汉字显示索引
            self.char_index = 0
            self.char_matrix = []
            
            # 如果当前是汉字模式，立即更新显示
            if self.LEDMode == 7:
                self.generate_char_matrix(char)
                self.update_leds()
            
            messagebox.showinfo("成功", f"已更改为显示汉字'{char}'")
            dialog.destroy()
        
        buttons_frame = ttk.Frame(dialog, padding=(10, 10))
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="确定", command=confirm, style="Primary.TButton").pack(side=tk.RIGHT, padx=5)
        ttk.Button(buttons_frame, text="取消", command=dialog.destroy, style="Secondary.TButton").pack(side=tk.RIGHT, padx=5)
    
    def show_about(self):
        """显示关于信息"""
        about_text = "LED控制程序模拟器 v2.0\n\n"
        about_text += "这是一个基于Python tkinter的51单片机LED控制程序模拟器。\n\n"
        about_text += "功能特点：\n"
        about_text += "- 8种LED模式\n"
        about_text += "- 3级速度控制\n"
        about_text += "- 暂停/继续功能\n"
        about_text += "- 颜色自定义（10种颜色）\n"
        about_text += "- 配置保存/加载\n"
        about_text += "- 键盘快捷键支持\n"
        about_text += "- 运行时间显示\n"
        about_text += "- 美观的图形界面\n"
        about_text += "- 汉字显示功能\n\n"
        about_text += "作者：LED Control Team\n"
        about_text += "日期：2026-01-21"
        messagebox.showinfo("关于", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = LEDSimulator(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
