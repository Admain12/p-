@echo off
title 恢复Edge可卸载
echo 正在恢复Edge浏览器卸载权限...

:: 检查管理员权限
NET SESSION >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo 请以管理员权限运行！
    pause
    exit /b 1
)

:: 恢复文件夹权限
icacls "C:\Program Files (x86)\Microsoft\Edge\Application" /remove:d Everyone >nul 2>&1
icacls "C:\Program Files (x86)\Microsoft\EdgeUpdate" /remove:d Everyone >nul 2>&1

:: 恢复注册表
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge" /v "NoRemove" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge Update" /v "NoRemove" /f >nul 2>&1

:: 解锁快捷方式
for %%i in ("%Public%\Desktop\Microsoft Edge.lnk" "%USERPROFILE%\Desktop\Microsoft Edge.lnk") do (
    if exist "%%i" (
        attrib -r -s -h "%%i" >nul 2>&1
    )
)

echo Edge浏览器卸载权限已恢复！
pause