@echo off
:: 开启延迟扩展，解决循环中变量实时更新问题
setlocal enabledelayedexpansion
:: 切换编码为UTF-8，并重定向输出到nul（屏蔽chcp的提示）
chcp 65001>nul
:: 定义变量（等号两侧无空格）
set var=1080
rem **********************循环开始了
:continue
:: 延迟扩展下用!var!获取实时变量值
echo 第!var!次循环
:: 变量自减1
set /a var-=1
:: 比较运算符修正为geq（大于等于）
if !var! geq 0 goto continue
rem **********************循环结束了
echo 循环执行完毕
pause
:: 关闭延迟扩展（可选，脚本结束会自动关闭）
endlocal