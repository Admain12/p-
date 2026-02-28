@echo off
chcp 65001 >nul 2>&1
echo 正在恢复文件关联备份...
reg import "D:\Backup\txt_assoc.reg"
reg import "D:\Backup\txt_fex.reg"
echo 重启资源管理器生效...
taskkill /f /im explorer.exe & start explorer.exe
echo 已恢复，建议立即扫描恶意软件！

pause