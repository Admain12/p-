@echo off
chcp 65001 > nul
set var=500
rem ************循环开始了
:continue
echo 第%var%次循环
set /a var-=1
if %var% gtr 0 goto continue
rem ************循环结束了
echo 循环执行完毕
pause
