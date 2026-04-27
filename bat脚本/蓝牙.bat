@echo off
chcp 65001 >nul
title 修复蓝牙鼠标重启后无法连接
color 0A

:: 检查管理员权限
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo [31m请右键以管理员身份运行！[0m
    pause >nul
    exit /b 1
)

:: 1. 设置蓝牙服务为延迟自动启动
echo 1. 优化蓝牙服务启动方式...
sc config bthserv start= delayed-auto >nul
sc config BluetoothUserService start= auto >nul
sc stop bthserv >nul & sc start bthserv >nul

:: 2. 彻底禁用蓝牙电源管理
echo 2. 禁用蓝牙适配器省电模式...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{e0cbf06c-cd8b-4647-bb8a-263b43f0f974}\0000" /v PowerManagementEnabled /t REG_DWORD /d 0 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{36FC9E60-C465-11CF-8056-444553540000}\0000" /v PowerDownEnable /t REG_DWORD /d 0 /f >nul 2>&1

:: 3. 清理旧配对缓存
echo 3. 清理蓝牙配对缓存...
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices" /f >nul 2>&1

echo.
echo [32m优化完成！请重新配对蓝牙鼠标，重启电脑测试。[0m
echo 若仍无效，建议更新蓝牙驱动或关闭Windows快速启动。
pause >nul