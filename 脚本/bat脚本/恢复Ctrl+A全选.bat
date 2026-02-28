@echo off
chcp 65001 >nul
echo ==============================================
echo  恢复 Ctrl+A 为默认全选功能
echo  说明：本脚本仅重置系统级快捷键关联，需手动关闭第三方软件的 Ctrl+A 截屏绑定
echo ==============================================
pause

:: 管理员权限检测
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo 请以管理员身份运行本脚本！
    pause
    exit /b 1
)

:: 重置键盘布局相关注册表（修复系统级快捷键异常）
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout" /v "Scancode Map" /t REG_BINARY /d 00000000000000000000000000000000 /f >nul 2>&1

:: 提示关闭第三方截屏软件
echo.
echo 系统级快捷键已重置！
echo 请手动关闭以下软件的 Ctrl+A 截屏绑定：
echo 1. 微信：设置 > 快捷按键 > 取消“截取屏幕”的 Ctrl+A 绑定
echo 2. QQ：设置 > 热键 > 取消“截图”的 Ctrl+A 绑定
echo 3. Snipaste/ShareX 等截屏工具：在软件设置中修改截屏快捷键
echo.
echo 操作完成后重启电脑生效！
pause