@echo off
chcp 65001 >nul
echo ==============================================
echo 正在暂停Windows自动更新...
echo 请确保以【管理员身份】运行此脚本！
echo ==============================================
pause

:: 1. 停止并禁用Windows Update服务
echo.
echo [1/6] 停止并禁用Windows Update服务...
sc config wuauserv start= disabled >nul 2>&1
net stop wuauserv /y >nul 2>&1

:: 2. 停止并禁用Background Intelligent Transfer Service (BITS)
echo [2/6] 停止并禁用BITS服务...
sc config bits start= disabled >nul 2>&1
net stop bits /y >nul 2>&1

:: 3. 停止并禁用Delivery Optimization服务
echo [3/6] 停止并禁用Delivery Optimization服务...
sc config dosvc start= disabled >nul 2>&1
net stop dosvc /y >nul 2>&1

:: 4. 修改组策略注册表项（禁用自动更新）
echo [4/6] 修改自动更新注册表项...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" /v DisableWUfBScan /t REG_DWORD /d 1 /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\wuauserv" /v Start /t REG_DWORD /d 4 /f >nul 2>&1

:: 5. 禁用Windows更新计划任务
echo [5/6] 禁用Windows更新计划任务...
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Scheduled Start" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Automatic App Update" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Automatic Updates" /disable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Scheduled Updates" /disable >nul 2>&1

:: 6. 清空Windows更新缓存
echo [6/6] 清空Windows更新缓存...
rd /s /q "C:\Windows\SoftwareDistribution\Download" >nul 2>&1
md "C:\Windows\SoftwareDistribution\Download" >nul 2>&1

echo.
echo ==============================================
echo Windows更新已长期暂停完成！
echo 如需恢复更新，请运行恢复脚本。
echo ==============================================
pause