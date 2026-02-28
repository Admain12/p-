@echo off
chcp 65001 >nul 2>&1
title 恢复Edge可卸载权限
echo =====================================================
echo 正在恢复Edge浏览器卸载权限...
echo =====================================================

:: 检查是否以管理员权限运行
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 错误：请以管理员权限运行此脚本！
    echo 请右键点击此脚本文件，选择"以管理员身份运行"
    pause
    exit /b 1
)

:: 定义Edge相关路径
set "edgePath=C:\Program Files (x86)\Microsoft\Edge\Application"
set "edgeUpdatePath=C:\Program Files (x86)\Microsoft\EdgeUpdate"

:: 恢复Edge文件夹删除权限
echo 正在恢复Edge文件夹权限...
if exist "%edgePath%" (
    takeown /f "%edgePath%" /r /d y >nul 2>&1
    icacls "%edgePath%" /remove:d Everyone >nul 2>&1
    icacls "%edgePath%" /grant Everyone:(OI)(CI)F >nul 2>&1
)

:: 恢复EdgeUpdate文件夹权限
if exist "%edgeUpdatePath%" (
    takeown /f "%edgeUpdatePath%" /r /d y >nul 2>&1
    icacls "%edgeUpdatePath%" /remove:d Everyone >nul 2>&1
    icacls "%edgeUpdatePath%" /grant Everyone:(OI)(CI)F >nul 2>&1
)

:: 恢复Edge卸载注册表项
echo 正在恢复注册表权限...
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /v "NoRemove" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /v "NoRemove" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge Update" /v "NoRemove" /f >nul 2>&1

:: 解锁Edge快捷方式
echo 正在解锁Edge快捷方式...
for %%i in ("%Public%\Desktop\Microsoft Edge.lnk" "%USERPROFILE%\Desktop\Microsoft Edge.lnk") do (
    if exist "%%i" (
        attrib -r -s "%%i" >nul 2>&1
    )
)

echo =====================================================
echo Edge浏览器卸载权限恢复完成！
echo 现在可以正常卸载Edge浏览器了
echo.
echo 提示：如需卸载Edge，可使用之前提供的命令行卸载方法
echo =====================================================

pause