@echo off
:: ============== 核心修复：解决中文乱码 ==============
:: 1. 设置CMD代码页为UTF-8（强制）
chcp 936 >nul 2>&1
:: 2. 强制CMD使用UTF-8输出（Win10+支持，兼容Win7）
set "PYTHONIOENCODING=utf-8"
set "LC_ALL=zh_CN.UTF-8"

:: ============== 原有配置 ==============
set "ScriptName=文件修复脚本.bat"  :: 替换为你的脚本名
set "WindowTitle=文件自动修复"    :: 替换为脚本窗口标题

:: 1. 检测是否已有同名脚本运行（通过窗口标题+进程路径）
:: 修复：findstr添加 /utf8 参数（Win10+），兼容Win7去掉/utf8
tasklist /v /fi "WINDOWTITLE eq %WindowTitle%" /fi "IMAGENAME eq cmd.exe" | findstr /i /utf8 "%ScriptName%" >nul 2>&1
:: 兼容Win7（Win7的findstr无/utf8参数，注释上面一行，启用下面一行）
:: tasklist /v /fi "WINDOWTITLE eq %WindowTitle%" /fi "IMAGENAME eq cmd.exe" | findstr /i "%ScriptName%" >nul 2>&1

if %errorlevel% equ 0 (
    echo 【提示】%ScriptName% 已在运行中！
    echo 正在尝试结束残留进程...
    :: 强制结束匹配的进程
    taskkill /f /fi "WINDOWTITLE eq %WindowTitle%" /fi "IMAGENAME eq cmd.exe" >nul 2>&1
    timeout /t 2 /nobreak >nul
    echo 残留进程已清理，重新运行脚本...
)

:: 2. 设置当前窗口标题（用于后续检测）
title %WindowTitle%

:: 3. 执行实际的修复命令（替换为正确的系统/工具命令）
echo 开始执行文件修复...
:: 示例1：系统文件修复（Windows内置）
sfc /scannow
:: 示例2：第三方工具修复（替换为你的工具路径）
:: "D:\修复工具\FileRepair.exe" /auto

:: 4. 执行完成后重置窗口标题
title cmd
echo 修复完成！
pause