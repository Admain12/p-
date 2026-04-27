@echo off
chcp 65001 >nul
echo ==============================================
echo 正在恢复Windows自动更新...
echo 请确保以【管理员身份】运行此脚本！
echo ==============================================
pause

:: 1. 启用并启动Windows Update服务
echo.
echo [1/6] 启用并启动Windows Update服务...
sc config wuauserv start= auto >nul 2>&1
net start wuauserv >nul 2>&1

:: 2. 启用并启动BITS服务
echo [2/6] 启用并启动BITS服务...
sc config bits start= auto >nul 2>&1
net start bits >nul 2>&1

:: 3. 启用并启动Delivery Optimization服务
echo [3/6] 启用并启动Delivery Optimization服务...
sc config dosvc start= auto >nul 2>&1
net start dosvc >nul 2>&1

:: 4. 恢复自动更新注册表项
echo [4/6] 恢复自动更新注册表项...
reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" /v NoAutoUpdate /t REG_DWORD /d 0 /f >nul 2>&1
reg delete "HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" /v DisableWUfBScan /f >nul 2>&1
reg add "HKLM\SYSTEM\CurrentControlSet\Services\wuauserv" /v Start /t REG_DWORD /d 2 /f >nul 2>&1

:: 5. 启用Windows更新计划任务
echo [5/6] 启用Windows更新计划任务...
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Scheduled Start" /enable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Automatic App Update" /enable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Automatic Updates" /enable >nul 2>&1
schtasks /change /tn "Microsoft\Windows\WindowsUpdate\Scheduled Updates" /enable >nul 2>&1

:: 6. 重置Windows更新组件（可选）
echo [6/6] 重置Windows更新组件...
wuauclt /resetauthorization /detectnow >nul 2>&1

echo.
echo ==============================================
echo Windows更新已恢复完成！
echo 系统将在下次检查更新时恢复自动更新。
echo ==============================================
pause