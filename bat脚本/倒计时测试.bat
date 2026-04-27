@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title 倒计时测试

call :start_timer

pause
exit

::-------------------------------------------------------------
:start_timer
rem 设置倒计时总秒数
set /a count=120

:countdown
cls
echo 初始化剩余：!count! 秒
title 倒计时测试 - 剩余!count!秒
rem 递减1秒
set /a count-=1
rem 等待1秒后继续
if !count! GEQ 0 (
    timeout /t 1 > nul
    goto countdown
)

cls
title 倒计时完成
echo 初始化完成！
exit /b
::-------------------------------------------------------------
