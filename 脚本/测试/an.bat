@echo off
chcp 65001 >nul
echo 正在检查并修复系统文件...
sfc /scannow
echo 正在优化磁盘（SSD跳过此步骤）...
defrag %systemdrive% /o
echo 系统优化完成！
pause