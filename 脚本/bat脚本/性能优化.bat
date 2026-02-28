@echo off
chcp 65001 > nul 
REM 性能优化示例
setlocal enabledelayedexpansion

set start_time=%time%
echo 脚本开始时间: !start_time!

REM 优化技巧1：减少磁盘IO
set file_list=
for /f "delims=" %%F in ('dir /b /s *.txt') do set file_list=!file_list! "%%F"

REM 优化技巧2：批量处理
echo 批量处理文件...
for %%F in (!file_list!) do (
    REM 使用临时变量减少磁盘访问
    set filename=%%~nF
    set filepath=%%~dpF
    echo 处理: !filename! 路径: !filepath!
)

REM 优化技巧3：避免不必要的命令调用
set end_time=%time%
echo 脚本结束时间: !end_time!

echo 执行完成！
s
pause
