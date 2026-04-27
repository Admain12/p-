@echo off
chcp 65001 >nul 2>&1
title Windows系统管理工具箱 - 管理员模式
color 0A
mode con cols=90 lines=30

:main_menu
cls
echo ==============================================================
echo                  🔧 Windows系统管理工具箱 (最终版)
echo ==============================================================
echo 1. 系统信息查看 (硬件/系统/激活)
echo 2. 网络工具 (WiFi/IP/ping)
echo 3. 系统设置 (UAC/hosts/注册表/上帝模式)
echo 4. 实用工具 (哈希/启动项/软件卸载)
echo 5. 系统维护与优化 (清理/重置/碎片整理)
echo 6. 安全与监控 (驱动/服务/用户/还原点)
echo 7. 文件操作 (批量重命名/加密压缩/快速访问)
echo 0. 退出工具箱
echo ==============================================================
set /p choice=请输入功能分类编号: 

if "%choice%"=="1" call :sub_systeminfo
if "%choice%"=="2" call :sub_network
if "%choice%"=="3" call :sub_settings
if "%choice%"=="4" call :sub_tools
if "%choice%"=="5" call :sub_maintenance
if "%choice%"=="6" call :sub_security
if "%choice%"=="7" call :sub_fileops
if "%choice%"=="0" exit /b 0
echo 输入无效，请重新选择！
pause >nul
goto main_menu


:: 子菜单1：系统信息查看
:sub_systeminfo
cls
echo ==============================================================
echo                  🖥️  系统信息查看
echo ==============================================================
echo 1. 查看硬件信息 (CPU/内存/磁盘)
echo 2. 查看系统版本与激活状态
echo 3. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    echo 【CPU信息】
    wmic cpu get Name,NumberOfCores,MaxClockSpeed
    echo.
    echo 【内存信息】
    wmic memorychip get Capacity,Speed
    echo.
    echo 【磁盘信息】
    wmic logicaldisk where DriveType=3 get DeviceID,Size,FreeSpace
    pause >nul
    goto sub_systeminfo
)

if "%sub_choice%"=="2" (
    cls
    echo 【系统版本】
    winver
    echo.
    echo 【激活状态】
    slmgr /dli
    pause >nul
    goto sub_systeminfo
)

if "%sub_choice%"=="3" goto main_menu
echo 输入无效！
pause >nul
goto sub_systeminfo


:: 子菜单2：网络工具
:sub_network
cls
echo ==============================================================
echo                  🌐  网络工具集
echo ==============================================================
echo 1. 查看已连接WiFi密码
echo 2. 查看IP与网卡信息
echo 3. ping测试 (输入目标地址)
echo 4. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    netsh wlan show profiles
    set /p wifiname=请输入要查看的WiFi名称: 
    netsh wlan show profile name="%wifiname%" key=clear
    pause >nul
    goto sub_network
)

if "%sub_choice%"=="2" (
    cls
    ipconfig /all
    pause >nul
    goto sub_network
)

if "%sub_choice%"=="3" (
    cls
    set /p target=请输入ping目标（IP/域名）: 
    ping %target% -t
    pause >nul
    goto sub_network
)

if "%sub_choice%"=="4" goto main_menu
echo 输入无效！
pause >nul
goto sub_network


:: 子菜单3：系统设置
:sub_settings
cls
echo ==============================================================
echo                  ⚙️  系统设置工具
echo ==============================================================
echo 1. 调整UAC用户账户控制
echo 2. 编辑hosts文件
echo 3. 打开注册表编辑器
echo 4. 创建上帝模式文件夹
echo 5. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    echo 选择UAC级别：
    echo 1. 始终通知（最高安全）
    echo 2. 默认通知
    echo 3. 从不通知（低安全）
    set /p uac=输入编号: 
    if "%uac%"=="1" reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f & reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 2 /f
    if "%uac%"=="2" reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 5 /f
    if "%uac%"=="3" reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
    echo UAC设置已更新，需重启生效
    pause >nul
    goto sub_settings
)

if "%sub_choice%"=="2" (
    notepad C:\Windows\System32\drivers\etc\hosts
    goto sub_settings
)

if "%sub_choice%"=="3" (
    regedit
    goto sub_settings
)

if "%sub_choice%"=="4" (
    mkdir "%~dp0GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}"
    echo 已在工具目录创建“上帝模式”文件夹
    pause >nul
    goto sub_settings
)

if "%sub_choice%"=="5" goto main_menu
echo 输入无效！
pause >nul
goto sub_settings


:: 子菜单4：实用工具
:sub_tools
cls
echo ==============================================================
echo                  🛠️  实用工具集
echo ==============================================================
echo 1. 计算文件哈希值（MD5/SHA1）
echo 2. 管理开机启动项
echo 3. 卸载软件
echo 4. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    set /p file_path=请拖入文件（或输入路径）: 
    echo MD5哈希：
    certutil -hashfile "%file_path%" MD5
    echo.
    echo SHA1哈希：
    certutil -hashfile "%file_path%" SHA1
    pause >nul
    goto sub_tools
)

if "%sub_choice%"=="2" (
    cls
    msconfig
    goto sub_tools
)

if "%sub_choice%"=="3" (
    cls
    echo ==============================================================
    echo                  🗑️  软件卸载工具
    echo ==============================================================
    echo 正在获取已安装软件列表...
    wmic product get Name,Version,InstallDate /value > "%temp%\installed_software.txt"
    echo 请选择要卸载的软件（输入软件名称中的关键词）:
    findstr /i /v "Name=" "%temp%\installed_software.txt" | findstr /i /v "Version=" | findstr /i /v "InstallDate=" | findstr /i /v "Description=" | findstr /i /v "InstallLocation=" | sort > "%temp%\software_list.txt"
    type "%temp%\software_list.txt"
    set /p software_name=输入软件名称关键词:
    for /f "tokens=*" %%a in ('findstr /i "%software_name%" "%temp%\software_list.txt"') do (
        set "selected_software=%%a"
        goto uninstall_confirm
    )
    echo 未找到匹配的软件！
    pause >nul
    goto sub_tools

    :uninstall_confirm
    echo 确认卸载：%selected_software%
    echo 注意：卸载过程可能需要管理员权限！
    set /p confirm=是否继续卸载？(Y/N):
    if /i "%confirm%"=="Y" (
        for /f "tokens=*" %%a in ('findstr /i "%selected_software%" "%temp%\installed_software.txt"') do (
            set "uninstall_string=%%a"
            set "uninstall_string=!uninstall_string:Name=!"
            set "uninstall_string=!uninstall_string:=!"
            set "uninstall_string=!uninstall_string:  =!"
            wmic product where "Name='!uninstall_string!'" call Uninstall >nul
            echo 正在卸载...
            timeout /t 2 /nobreak >nul
        )
        echo 软件卸载完成！
    ) else (
        echo 已取消卸载
    )
    del "%temp%\installed_software.txt" 2>nul
    del "%temp%\software_list.txt" 2>nul
    pause >nul
    goto sub_tools
)

if "%sub_choice%"=="4" goto main_menu
echo 输入无效！
pause >nul
goto sub_tools


:: 子菜单5：系统维护与优化
:sub_maintenance
cls
echo ==============================================================
echo                  🔄  系统维护与优化
echo ==============================================================
echo 1. 清理系统垃圾文件
echo 2. 清理DNS缓存
echo 3. 重置网络设置
echo 4. 整理磁盘碎片 (仅HDD)
echo 5. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    echo 正在清理系统垃圾...
    cleanmgr /sageset:1 >nul
    cleanmgr /sagerun:1 >nul
    echo 系统垃圾清理完成！
    pause >nul
    goto sub_maintenance
)

if "%sub_choice%"=="2" (
    cls
    ipconfig /flushdns
    echo DNS缓存已清理！
    pause >nul
    goto sub_maintenance
)

if "%sub_choice%"=="3" (
    cls
    netsh winsock reset
    netsh int ip reset
    echo 网络设置已重置！请重启电脑生效。
    pause >nul
    goto sub_maintenance
)

if "%sub_choice%"=="4" (
    cls
    wmic logicaldisk where DriveType=3 get DeviceID
    set /p drive=请输入要整理的盘符（如C:）: 
    defrag %drive% /O
    echo 磁盘碎片整理完成！
    pause >nul
    goto sub_maintenance
)

if "%sub_choice%"=="5" goto main_menu
echo 输入无效！
pause >nul
goto sub_maintenance


:: 子菜单6：安全与监控
:sub_security
cls
echo ==============================================================
echo                  🔒  安全与监控
echo ==============================================================
echo 1. 查看已安装的驱动程序
echo 2. 查看正在运行的服务
echo 3. 查看当前登录的用户和用户组
echo 4. 创建系统还原点
echo 5. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    driverquery /v
    pause >nul
    goto sub_security
)

if "%sub_choice%"=="2" (
    cls
    services.msc
    pause >nul
    goto sub_security
)

if "%sub_choice%"=="3" (
    cls
    echo 【本地用户】
    net user
    echo.
    echo 【本地用户组】
    net localgroup
    pause >nul
    goto sub_security
)

if "%sub_choice%"=="4" (
    cls
    set /p point_name=请输入还原点名称: 
    wmic.exe /Namespace:\\root\default Path SystemRestore Call CreateRestorePoint "%point_name%", 100, 7
    echo 系统还原点已创建！
    pause >nul
    goto sub_security
)

if "%sub_choice%"=="5" goto main_menu
echo 输入无效！
pause >nul
goto sub_security


:: 子菜单7：文件操作
:sub_fileops
cls
echo ==============================================================
echo                  📁  文件操作工具
echo ==============================================================
echo 1. 文件批量重命名
echo 2. 创建加密压缩包
echo 3. 快速打开常用目录
echo 4. 返回主菜单
echo ==============================================================
set /p sub_choice=请输入功能编号: 

if "%sub_choice%"=="1" (
    cls
    set /p folder_path=请输入要操作的文件夹路径（或拖入）: 
    set /p prefix=请输入要添加的前缀: 
    set /p suffix=请输入要添加的后缀（无则留空）: 
    setlocal enabledelayedexpansion
    for %%f in ("!folder_path!\*") do (
        ren "%%f" "!prefix!%%~nf!suffix!%%~xf"
    )
    endlocal
    echo 文件批量重命名完成！
    pause >nul
    goto sub_fileops
)

if "%sub_choice%"=="2" (
    cls
    set /p file_path=请拖入要压缩的文件或文件夹: 
    set /p zip_password=请输入压缩包密码: 
    powershell -Command "$securePassword = ConvertTo-SecureString '%zip_password%' -AsPlainText -Force; Compress-Archive -Path '%file_path%' -DestinationPath '%file_path%.zip' -Password $securePassword"
    echo 加密压缩包已创建！
    pause >nul
    goto sub_fileops
)

if "%sub_choice%"=="3" (
    cls
    echo ==============================================================
    echo                  🗂️  快速访问目录
    echo ==============================================================
    echo 1. 我的文档
    echo 2. 下载文件夹
    echo 3. 桌面
    echo 4. 开始菜单程序
    echo 5. 控制面板
    echo 6. 返回主菜单
    echo ==============================================================
    set /p dir_choice=请输入目录编号: 
    if "%dir_choice%"=="1" explorer %USERPROFILE%\Documents
    if "%dir_choice%"=="2" explorer %USERPROFILE%\Downloads
    if "%dir_choice%"=="3" explorer %USERPROFILE%\Desktop
    if "%dir_choice%"=="4" explorer shell:Programs
    if "%dir_choice%"=="5" control
    if "%dir_choice%"=="6" goto main_menu
    echo 输入无效！
    pause >nul
    goto sub_fileops
)

if "%sub_choice%"=="4" goto main_menu
echo 输入无效！
pause >nul
goto sub_fileops