@echo off 
chcp 65001 > nul
cls
title 终极多功能修复工具
mode con cols=80 lines=30

:: 管理员权限检测
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo 请求管理员权限...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
    pushd "%CD%"
    CD /D "%~dp0"

:menu
cls
color 0A
echo.
echo                 ==============================
echo                 终极Windows系统多功能修复工具
echo                 ==============================
echo.
echo              1.网络修复及上网相关设置,修复IE,自定义屏蔽网站
echo.
echo              2.病毒专杀工具，端口关闭工具,关闭自动播放
echo.
echo              3.清除所有多余的自启动项目，修复系统错误
echo.
echo              4.清理系统垃圾,提高启动速度
echo.
echo              Q.退出
echo.
echo.
:cho
set choice=
set /p choice=          请选择:
IF NOT "%choice%"=="" SET choice=%choice:~0,1%
if /i "%choice%"=="1" goto ip
if /i "%choice%"=="2" goto setsave
if /i "%choice%"=="3" goto kaiji
if /i "%choice%"=="4" goto clean
if /i "%choice%"=="Q" goto endd
echo 选择无效，请重新输入
echo.
goto cho

:: 1.网络修复模块
:ip
cls
color 0B
echo.
echo                 ==============================
echo                 网络修复及上网相关设置
echo                 ==============================
echo.
echo              1.重置网络配置
echo              2.修复IE浏览器
echo              3.屏蔽指定网站
echo              4.解除网站屏蔽
echo              5.返回主菜单
echo.
set net_choice=
set /p net_choice=          请选择网络操作:

if "%net_choice%"=="1" (
    echo 正在重置网络配置...
    netsh winsock reset catalog > nul
    netsh int ip reset reset.log > nul
    ipconfig /release > nul
    ipconfig /renew > nul
    ipconfig /flushdns > nul
    echo 网络配置重置完成！
    pause
    goto ip
)

if "%net_choice%"=="2" (
    echo 正在修复IE浏览器...
    regsvr32 /s mshtml.dll
    regsvr32 /s urlmon.dll
    regsvr32 /s shdocvw.dll
    regsvr32 /s browseui.dll
    echo IE浏览器修复完成！
    pause
    goto ip
)

if "%net_choice%"=="3" (
    set /p website=请输入要屏蔽的网站域名(如:www.example.com):
    echo 正在屏蔽 %website%...
    echo.>>%systemroot%\system32\drivers\etc\hosts
    echo 127.0.0.1 %website%>>%systemroot%\system32\drivers\etc\hosts
    echo ::1 %website%>>%systemroot%\system32\drivers\etc\hosts
    ipconfig /flushdns > nul
    echo 网站 %website% 已屏蔽！
    pause
    goto ip
)

if "%net_choice%"=="4" (
    echo 正在解除网站屏蔽...
    copy %systemroot%\system32\drivers\etc\hosts %systemroot%\system32\drivers\etc\hosts.bak > nul
    findstr /v "127.0.0.1" %systemroot%\system32\drivers\etc\hosts.bak > %systemroot%\system32\drivers\etc\hosts
    findstr /v "::1" %systemroot%\system32\drivers\etc\hosts > %systemroot%\system32\drivers\etc\hosts.tmp
    move /y %systemroot%\system32\drivers\etc\hosts.tmp %systemroot%\system32\drivers\etc\hosts > nul
    ipconfig /flushdns > nul
    echo 网站屏蔽已解除(已备份原hosts文件为hosts.bak)！
    pause
    goto ip
)

if "%net_choice%"=="5" (
    goto menu
) else (
    echo 无效选择，请重新输入！
    pause
    goto ip
)

:: 2.安全工具模块
:setsave
cls
color 0C
echo.
echo                 ==============================
echo                 安全工具及系统防护设置
echo                 ==============================
echo.
echo              1.关闭危险端口(135,139,445等)
echo              2.禁用自动播放功能
echo              3.启动Windows Defender
echo              4.返回主菜单
echo.
set safe_choice=
set /p safe_choice=          请选择安全操作:

if "%safe_choice%"=="1" (
    echo 正在关闭危险端口...
    :: 关闭135端口
    reg add "HKLM\SYSTEM\CurrentControlSet\Services\RpcSs\Parameters" /v "TCP/IP Port" /t REG_DWORD /d 0 /f > nul
    :: 关闭139和445端口
    netsh advfirewall firewall add rule name="Close 139" dir=in action=block protocol=TCP localport=139 > nul
    netsh advfirewall firewall add rule name="Close 445" dir=in action=block protocol=TCP localport=445 > nul
    echo 危险端口已关闭！需要重启电脑生效
    pause
    goto setsave
)

if "%safe_choice%"=="2" (
    echo 正在禁用自动播放功能...
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoDriveTypeAutoRun" /t REG_DWORD /d 255 /f > nul
    reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v "NoDriveTypeAutoRun" /t REG_DWORD /d 255 /f > nul
    echo 自动播放功能已禁用！
    pause
    goto setsave
)

if "%safe_choice%"=="3" (
    echo 正在启动Windows Defender...
    sc config WinDefend start= auto > nul
    net start WinDefend > nul
    echo Windows Defender已启动！
    pause
    goto setsave
)

if "%safe_choice%"=="4" (
    goto menu
) else (
    echo 无效选择，请重新输入！
    pause
    goto setsave
)

:: 3.启动项管理模块
:kaiji
cls
color 0D
echo.
echo                 ==============================
echo                 启动项管理及系统错误修复
echo                 ==============================
echo.
echo              1.清理注册表启动项
echo              2.清理任务计划启动项
echo              3.系统文件检查修复
echo              4.DISM系统修复
echo              5.返回主菜单
echo.
set start_choice=
set /p start_choice=          请选择启动项操作:

if "%start_choice%"=="1" (
    echo 正在清理注册表启动项...
    :: 清理常见启动项位置
    reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /va /f > nul 2>&1
    reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /va /f > nul 2>&1
    reg delete "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run" /va /f > nul 2>&1
    echo 注册表启动项清理完成！
    pause
    goto kaiji
)

if "%start_choice%"=="2" (
    echo 正在清理任务计划启动项...
    schtasks /query /fo csv | findstr /i "autostart" > "%temp%\tasks.txt" 2>&1
    for /f "tokens=1 delims=," %%a in (%temp%\tasks.txt) do (
        schtasks /delete /tn %%a /f > nul 2>&1
    )
    del "%temp%\tasks.txt" > nul 2>&1
    echo 任务计划启动项清理完成！
    pause
    goto kaiji
)

if "%start_choice%"=="3" (
    echo 正在进行系统文件检查...
    sfc /scannow
    echo 系统文件检查完成！
    pause
    goto kaiji
)

if "%start_choice%"=="4" (
    echo 正在进行DISM系统修复...
    DISM /Online /Cleanup-Image /CheckHealth > nul
    DISM /Online /Cleanup-Image /ScanHealth > nul
    DISM /Online /Cleanup-Image /RestoreHealth > nul
    echo DISM系统修复完成！
    pause
    goto kaiji
)

if "%start_choice%"=="5" (
    goto menu
) else (
    echo 无效选择，请重新输入！
    pause
    goto kaiji
)

:: 4.系统垃圾清理模块
:clean
cls
color 0E
echo.
echo                 ==============================
echo                 系统垃圾清理工具
echo                 ==============================
echo.
echo              1.清理临时文件
echo              2.清理回收站
echo              3.清理日志文件
echo              4.全面清理(所有垃圾)
echo              5.返回主菜单
echo.
set clean_choice=
set /p clean_choice=          请选择清理操作:

:: 定义清理函数
:clean_temp
echo 正在清理临时文件...
del /f /s /q %systemroot%\temp\*.* > nul
del /f /s /q %temp%\*.* > nul
del /f /s /q %userprofile%\appdata\local\temp\*.* > nul
rd /s /q %systemroot%\temp > nul 2>&1
md %systemroot%\temp > nul 2>&1
echo 临时文件清理完成！
goto :eof

:clean_recycle
echo 正在清理回收站...
rd /s /q %systemroot%\$Recycle.Bin > nul 2>&1
md %systemroot%\$Recycle.Bin > nul 2>&1
for /d %%a in (C:\,D:\,E:\,F:\) do (
    rd /s /q %%a\$Recycle.Bin > nul 2>&1
    md %%a\$Recycle.Bin > nul 2>&1
)
echo 回收站清理完成！
goto :eof

:clean_log
echo 正在清理日志文件...
del /f /s /q %systemroot%\*.log > nul
del /f /s /q %systemroot%\*.bak > nul
del /f /s /q %systemroot%\*.old > nul
echo 日志文件清理完成！
goto :eof

:: 执行清理操作
if "%clean_choice%"=="1" (
    call :clean_temp
    pause
    goto clean
)

if "%clean_choice%"=="2" (
    call :clean_recycle
    pause
    goto clean
)

if "%clean_choice%"=="3" (
    call :clean_log
    pause
    goto clean
)

if "%clean_choice%"=="4" (
    call :clean_temp
    call :clean_recycle
    call :clean_log
    echo 全面清理完成！
    pause
    goto clean
)

if "%clean_choice%"=="5" (
    goto menu
) else (
    echo 无效选择，请重新输入！
    pause
    goto clean
)

:: 退出程序
:endd
cls
echo 感谢使用终极多功能修复工具！
echo 程序即将退出...
timeout /t 3 /nobreak > nul
exit