# Matrix Rain 动态壁纸

这是一个增强版的 Matrix 数字雨效果程序，支持全屏幕显示，适合用作动态壁纸。

## 功能特点

- ✨ **全屏幕显示**：自动适应显示器分辨率
- 🎨 **增强视觉效果**：渐变拖影、随机颜色
- 🌐 **中英文支持**：自动检测并使用中文字体
- ⌨️ **快捷键控制**：ESC退出，空格键暂停/继续
- 🖥️ **无窗口边框**：纯黑背景，沉浸式体验
- ⚡ **高性能**：优化的渲染算法，低资源占用

## 安装依赖

### Windows 系统
1. 安装 Python 3.7+
2. 安装 pygame：
   ```bash
   pip install pygame
   ```

### Linux 系统
1. 安装 Python 和 pygame：
   ```bash
   sudo apt install python3-pygame
   ```
   或
   ```bash
   pip install pygame
   ```

## 运行方法

### 直接运行
```bash
python matrix_rain_wallpaper.py
```

### 后台运行（Linux）
```bash
python matrix_rain_wallpaper.py &
```

## 操作说明

- **ESC 键**：退出程序
- **空格键**：暂停/继续动画
- **鼠标点击**：无响应（全屏模式）

## 设置为动态壁纸

### Windows 系统

1. **方法一：使用 Wallpaper Engine**
   - 安装 [Wallpaper Engine](https://store.steampowered.com/app/431960/Wallpaper_Engine/)
   - 将本程序导入为 "应用程序" 类型壁纸
   - 调整设置并应用

2. **方法二：使用 Rainmeter**
   - 安装 [Rainmeter](https://www.rainmeter.net/)
   - 创建一个新的皮肤，添加 WebParser 或 RunCommand 插件
   - 配置插件运行此程序

3. **方法三：使用 AutoHotkey**
   - 安装 [AutoHotkey](https://www.autohotkey.com/)
   - 创建脚本：
     ```autohotkey
     Run, python "D:\path\to\matrix_rain_wallpaper.py"
     WinWait, Matrix Rain Wallpaper
     Winset, Bottom,, A
     ```
   - 将脚本设置为开机启动

### Linux 系统

1. **方法一：使用 Xfce 桌面**
   - 安装 x11-apps：
     ```bash
     sudo apt install x11-apps
     ```
   - 运行程序并设置为桌面背景：
     ```bash
     python matrix_rain_wallpaper.py &
     sleep 2
     xprop -f _NET_WM_STATE 32a -set _NET_WM_STATE _NET_WM_STATE_BELOW
     ```

2. **方法二：使用 GNOME 桌面**
   - 安装 [GNOME Shell 扩展](https://extensions.gnome.org/extension/2986/live-wallpaper/)
   - 或使用 [mpv](https://mpv.io/) 和 [gnome-wallpaper-changer](https://github.com/harshadgavali/gnome-wallpaper-changer)

3. **方法三：使用 KDE 桌面**
   - 安装 [KWin 脚本](https://store.kde.org/p/1187170/)
   - 或使用 [plasma5-wallpapers-dynamic](https://github.com/zzag/plasma5-wallpapers-dynamic)

### macOS 系统

1. **方法一：使用 Wallpaper Engine**
   - 安装 Steam 版 Wallpaper Engine
   - 导入程序作为应用程序壁纸

2. **方法二：使用 NerdTool**
   - 安装 [NerdTool](https://github.com/schwarzeck/nerdtool)
   - 创建新的 "Shell" 项目，运行 Python 脚本

## 配置选项

可以修改程序中的以下参数来自定义效果：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `font_size` | 字符大小 | 20 |
| `fps` | 帧率 | 30 |
| `trail_length` | 拖影长度 | 20 |
| `surf.fill((0, 0, 0, 20))` | 拖影透明度（20） | 20 |

### 示例：修改字符大小为 24
```python
self.font_size = 24
self.font = pygame.font.SysFont("Consolas", self.font_size)
```

### 示例：增加拖影长度
```python
self.trail_length = 30
```

## 高级设置

### 自定义颜色
```python
self.GREEN = (0, 255, 100)  # 更亮的绿色
self.LIGHT_GREEN = (50, 255, 150)  # 更亮的浅绿色
```

### 自定义字符集
```python
# 只使用数字和字母
char = random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
```

## 故障排除

### 中文字体显示问题
- 确保系统已安装中文字体（如 SimHei、Microsoft YaHei）
- 在 Windows 10+ 中，启用 "Windows 显示语言"

### 性能问题
- 降低 `font_size` 值
- 减少 `trail_length` 值
- 降低 `fps` 值

### 程序无法退出
- 使用任务管理器/活动监视器结束 Python 进程
- 或按 Ctrl+C （在命令行启动的情况下）

## 系统要求

- Python 3.7+
- Pygame 2.0+
- 支持 OpenGL 加速的图形卡
- 至少 2GB 内存

## 注意事项

1. 作为动态壁纸运行时，程序会在后台持续运行
2. 某些系统可能会限制全屏应用的壁纸设置
3. 电池供电设备上建议降低帧率以节省电量
4. 定期检查程序是否正常运行

## 替代方案

如果本程序无法满足需求，可以尝试以下替代方案：

- **Wallpaper Engine**（Steam）：内置 Matrix 数字雨效果
- **Lively Wallpaper**（Windows）：开源动态壁纸软件
- **Plasma Dynamic Wallpaper**（KDE）：支持视频和动画壁纸
- **xwinwrap**（Linux）：将任何 X 应用作为桌面背景

## 许可证

本程序采用 MIT 许可证，可自由使用和修改。

---

**享受你的 Matrix 数字雨动态壁纸！** 🎉
inhttps://www.chromium.org/chromium-projects/