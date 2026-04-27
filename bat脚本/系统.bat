@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul 2>&1

:: ===================== 基础配置 =====================
:: 日志文件（带时间戳，保存修复全过程）
set "FIX_LOG=%~dp0SysFile_Fix_Log_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "FIX_LOG=%FIX_LOG: =0%"  :: 修复时间戳中的空格
set "AUTO_FIX=1"             :: 1=自动修复，0=仅检测不修复
set "RECHECK=1"              :: 1=修复后再次验证，0=不验证

:: ===================== 颜色定义（Win10+支持） =====================
if not defined ESC (for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a")
set "RED=%ESC%[31m" & set "GREEN=%ESC%[32m" & set "YELLOW=%ESC%[33m"
set "BLUE=%ESC%[36m" & set "GRAY=%ESC%[37m" & set "RESET=%ESC%[0m"

:: ===================== 前置校验 =====================
cls
title 系统文件完整性检测与自动修复工具
echo %BLUE%===========================================================================%RESET%
echo %BLUE%                      Windows系统文件修复工具（SFC+DISM）                  %RESET%
echo %BLUE%                      适配系统：Win7/10/11/Server 2008+                   %RESET%
echo %BLUE%===========================================================================%RESET%
echo.

:: 1. 强制管理员权限（无管理员权限无法执行SFC/DISM）
fltmc >nul 2>&1 || (
    echo %RED%[❌] 错误：请以【管理员身份】运行本脚本！%RESET%
    pause >nul & exit /b 1
)
echo %GREEN%[✅] 已获取管理员权限，开始检测系统文件...%RESET%
echo.

:: 2. 初始化日志文件
echo 系统文件修复日志 - %date% %time% > "%FIX_LOG%"
echo 自动修复模式：%AUTO_FIX%（1=开启，0=关闭） >> "%FIX_LOG%"
echo 修复后验证：%RECHECK%（1=开启，0=关闭） >> "%FIX_LOG%"
echo ====================================================== >> "%FIX_LOG%"
echo. >> "%FIX_LOG%"

:: ===================== 步骤1：判断Windows版本 =====================
echo %YELLOW%[📌] 步骤1：检测系统版本...%RESET%
ver | findstr "6.1" >nul 2>&1 && set "IS_WIN7=1" || set "IS_WIN7=0"
if !IS_WIN7! equ 1 (
    echo %GRAY%[信息] 检测到Win7/Server 2008系统，仅支持SFC检测，不支持DISM在线修复%RESET%
    echo 系统版本：Win7/Server 2008（仅SFC） >> "%FIX_LOG%"
) else (
    echo %GRAY%[信息] 检测到Win10/11/Server 2012+系统，支持SFC+DISM修复%RESET%
    echo 系统版本：Win10/11/Server 2012+（SFC+DISM） >> "%FIX_LOG%"
)
echo.

:: ===================== 步骤2：执行SFC检测 =====================
echo %YELLOW%[📌] 步骤2：执行SFC系统文件检测（耗时约5-15分钟）...%RESET%
echo 【SFC检测日志】 >> "%FIX_LOG%"
echo ====================================================== >> "%FIX_LOG%"
:: 执行SFC并记录日志
sfc /scannow >> "%FIX_LOG%" 2>&1
echo. >> "%FIX_LOG%"

:: 解析SFC检测结果
findstr /i "未找到任何完整性冲突 修复成功" "%FIX_LOG%" >nul 2>&1
if !errorlevel! equ 0 (
    echo %GREEN%[✅] SFC检测完成：系统文件无损坏/已自动修复%RESET%
    echo - SFC结果：文件完整 [安全] >> "%FIX_LOG%"
    goto :Fix_Complete
) else (
    echo %RED%[❌] SFC检测发现：系统文件损坏/缺失！%RESET%
    echo - SFC结果：文件损坏 [高危] >> "%FIX_LOG%"
    
    :: ===================== 步骤3：执行DISM修复（仅Win10+） =====================
    if !IS_WIN7! equ 0 (
        if !AUTO_FIX! equ 1 (
            echo %YELLOW%[📌] 步骤3：执行DISM在线修复（需联网，耗时约10-20分钟）...%RESET%
            echo 【DISM修复日志】 >> "%FIX_LOG%"
            echo ====================================================== >> "%FIX_LOG%"
            :: 检查系统映像健康状态
            DISM /Online /Cleanup-Image /CheckHealth >> "%FIX_LOG%" 2>&1
            echo. >> "%FIX_LOG%"
            :: 扫描映像损坏
            DISM /Online /Cleanup-Image /ScanHealth >> "%FIX_LOG%" 2>&1
            echo. >> "%FIX_LOG%"
            :: 修复映像（核心步骤）
            DISM /Online /Cleanup-Image /RestoreHealth >> "%FIX_LOG%" 2>&1
            echo. >> "%FIX_LOG%"

            :: 解析DISM修复结果
            findstr /i "操作成功完成 未检测到组件存储损坏" "%FIX_LOG%" >nul 2>&1
            if !errorlevel! equ 0 (
                echo %GREEN%[✅] DISM修复完成：系统映像已恢复%RESET%
                echo - DISM结果：修复成功 [安全] >> "%FIX_LOG%"
                
                :: 修复后再次执行SFC验证（可选）
                if !RECHECK! equ 1 (
                    echo %YELLOW%[📌] 步骤4：再次执行SFC验证修复结果...%RESET%
                    echo 【SFC二次验证日志】 >> "%FIX_LOG%"
                    echo ====================================================== >> "%FIX_LOG%"
                    sfc /scannow >> "%FIX_LOG%" 2>&1
                    findstr /i "未找到任何完整性冲突" "%FIX_LOG%" >nul 2>&1
                    if !errorlevel! equ 0 (
                        echo %GREEN%[✅] 二次验证完成：系统文件已完全修复%RESET%
                        echo - 二次验证：文件完整 [安全] >> "%FIX_LOG%"
                    ) else (
                        echo %RED%[❌] 二次验证失败：仍有文件未修复（需手动干预）%RESET%
                        echo - 二次验证：修复失败 [高危] >> "%FIX_LOG%"
                    )
                )
            ) else (
                echo %RED%[❌] DISM修复失败：可能网络异常/系统映像损坏严重%RESET%
                echo - DISM结果：修复失败 [高危] >> "%FIX_LOG%"
            )
        ) else (
            echo %YELLOW%[⚠️] 已检测到文件损坏，未执行自动修复（AUTO_FIX=0）%RESET%
            echo - 修复状态：未执行自动修复 [信息] >> "%FIX_LOG%"
        )
    ) else (
        echo %YELLOW%[⚠️] Win7系统不支持DISM在线修复，请按以下步骤手动修复：%RESET%
        echo 1. 插入Win7安装介质（U盘/光盘），确认盘符（如D:）%RESET%
        echo 2. 以管理员运行CMD，执行：sfc /scannow /offbootdir:D:\ /offwindir:D:\Windows%RESET%
        echo - 修复建议：Win7需安装介质手动修复 [信息] >> "%FIX_LOG%"
    )
)

:: ===================== 修复完成 =====================
:Fix_Complete
echo.
echo %BLUE%===========================================================================%RESET%
echo %GREEN%[✅] 系统文件检测/修复流程完成！%RESET%
echo %YELLOW%[📄] 修复日志已保存至：%FIX_LOG%%RESET%
echo %RED%[⚠️] 若修复失败，建议：%RESET%
echo    1. 检查网络（DISM需联网下载文件）%RESET%
echo    2. Win7使用安装介质手动修复%RESET%
echo    3. 严重损坏可执行系统修复/重装%RESET%
echo %BLUE%===========================================================================%RESET%
echo.

:: 可选：自动打开日志文件
:: start "" "%FIX_LOG%"

echo %YELLOW%[📌] 按任意键关闭窗口...%RESET%
pause >nul

endlocal
exit /b 0

pause