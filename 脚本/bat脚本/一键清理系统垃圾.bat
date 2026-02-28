@echo off
chcp 65001>nul
:: 管理员权限检测（必须管理员才能清理系统级文件）
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo 请右键以【管理员身份】运行此脚本！
    pause
    exit /b
)

:: 定义颜色和标题
color 0A
title Windows 7/10 系统垃圾一键清理工具

echo ==============================================
echo          Windows 7/10 系统垃圾清理
echo ==============================================
echo 清理范围：
echo 1. 系统临时文件（%temp%）
echo 2. 系统更新缓存（SoftwareDistribution）
echo 3. 回收站文件
echo 4. 浏览器缓存（Edge/Chrome/IE）
echo 5. 日志文件、崩溃转储文件
echo 6. 预读取文件、休眠文件（可选）
echo ==============================================
pause

:: 1. 清理用户临时文件
echo.
echo [1/8] 清理用户临时文件...
del /f /s /q "%temp%\*.*"
rd /s /q "%temp%" 2>nul
md "%temp%" 2>nul  :: 重建temp目录（避免系统报错）

:: 2. 清理系统临时文件
echo [2/8] 清理系统临时文件...
del /f /s /q "%systemroot%\temp\*.*"
rd /s /q "%systemroot%\temp" 2>nul
md "%systemroot%\temp" 2>nul

:: 3. 清理回收站文件（全盘符）
echo [3/8] 清理回收站文件...
for /d %%i in (C:,D:,E:,F:) do (
    if exist "%%i\$Recycle.Bin\" (
        del /f /s /q "%%i\$Recycle.Bin\*.*"
    )
)

:: 4. 清理系统更新缓存（Win7/10通用）
echo [4/8] 清理系统更新缓存...
net stop wuauserv 2>nul
del /f /s /q "%systemroot%\SoftwareDistribution\Download\*.*"
net start wuauserv 2>nul

:: 5. 清理浏览器缓存
echo [5/8] 清理浏览器缓存...
:: Edge浏览器
if exist "%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data\Default\Cache\" (
    del /f /s /q "%USERPROFILE%\AppData\Local\Microsoft\Edge\User Data\Default\Cache\*.*"
)
:: Chrome浏览器
if exist "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Cache\" (
    del /f /s /q "%USERPROFILE%\AppData\Local\Google\Chrome\User Data\Default\Cache\*.*"
)
:: IE浏览器
del /f /s /q "%USERPROFILE%\AppData\Local\Microsoft\Windows\Temporary Internet Files\*.*"

:: 6. 清理日志和崩溃文件
echo [6/8] 清理日志/崩溃文件...
del /f /s /q "%systemroot%\*.log" 2>nul
del /f /s /q "%systemroot%\*.dmp" 2>nul
del /f /s /q "%systemroot%\Minidump\*.*" 2>nul

:: 7. 清理预读取文件（提升启动速度）
echo [7/8] 清理预读取文件...
del /f /s /q "%systemroot%\Prefetch\*.*" 2>nul

:: 8. 可选：清理休眠文件（Win10/7需管理员，释放内存大小的空间）
echo.
set /p choice="是否清理休眠文件（释放大量空间，重启后生效，Y/N）？"
if /i "%choice%"=="Y" (
    echo [8/8] 清理休眠文件...
    powercfg -h off 2>nul
    echo 休眠文件已禁用，如需恢复请执行：powercfg -h on
) else (
    echo [8/8] 跳过休眠文件清理
)

:: 完成提示
echo.
echo ==============================================
echo 垃圾清理完成！建议重启电脑以释放全部占用空间
echo ==============================================
pause

