@echo off
chcp 65001 >nul 2>&1
title Boot检测修复工具
mode con cols=85 lines=35
fltmc >nul 2>&1 || (echo 请以管理员身份运行！&pause>nul&exit/b1)
set "R=D:\BootRepair"&set "U=%R%\UEFI"&set "B=%R%\bcd"&set "T=%TEMP%\BR_Temp"
md "%T%" >nul 2>&1
:M
cls&echo.
echo ==============================================
echo          Boot/UEFI/BIOS检测修复工具
echo ==============================================
echo 1. 检测CMOS电池
echo 2. 检测启动模式
echo 3. 检测启动项
echo 4. 修复UEFI引导
echo 5. 修复BIOS引导
echo 6. 退出
echo ==============================================
set "C="&set /p "C=输入序号："
if "%C%"=="1" goto C1
if "%C%"=="2" goto C2
if "%C%"=="3" goto C3
if "%C%"=="4" goto C4
if "%C%"=="5" goto C5
if "%C%"=="6" goto X
echo 输入无效！&timeout/t2>nul&goto M

:C1
cls&echo.
echo ========== CMOS检测 ==========
for /f "tokens=1" %%a in ('date/t') do if %%a gtr 2020 (echo √ 时间正常) else (echo × 电池可能没电)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\TimeZoneInformation" >nul 2>&1&&echo √ 配置保存正常||echo × 配置保存失败
echo.&pause&goto M

:C2
cls&echo.
echo ========== 启动模式检测 ==========
reg query "HKLM\SYSTEM\CurrentControlSet\Control\FirmwareResources" >nul 2>&1&&(echo UEFI模式&reg query "HKLM\SYSTEM\CurrentControlSet\Control\SecureBoot\State" /v UEFISecureBootEnabled >nul 2>&1&&(for /f "tokens=2 delims==" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\SecureBoot\State" /v UEFISecureBootEnabled ^|findstr "0x"') do if "%%a"=="0x1" echo 安全启动：启用||echo 安全启动：禁用)||echo 安全启动：不支持)||echo BIOS模式
echo.&pause&goto M

:C3
cls&echo.
echo ========== 启动项检测 ==========
bcdedit /enum "{bootmgr}" > "%T%\b.txt" 2>&1&&(echo 启动顺序：&findstr "displayorder" "%T%\b.txt")||echo 读取失败
bcdedit /enum /v | findstr "description"&del "%T%\b.txt"
echo.&pause&goto M

:C4
cls&echo.
echo ========== UEFI修复 ==========   
if not exist "%U%" (echo 无修复文件&pause&goto M)
if not exist "%B%" (echo 无BCD模板&pause&goto M)
diskpart /s "%T%\d.txt" > "%T%\e.txt" 2>&1&echo list volume>%T%\d.txt&echo exit>>%T%\d.txt&diskpart /s "%T%\d.txt" > "%T%\e.txt" 2>&1
set "E="&for /f "tokens=2,5 delims= " %%a in ('type "%T%\e.txt" ^|findstr "FAT32" ^|findstr "EFI"') do set "E=%%a:"
if not defined E set /p "E=输入EFI盘符："
mountvol %E% /s >nul 2>&1&&echo 挂载EFI分区成功||echo 挂载失败
set "BAK=%E%\EFI\Microsoft\Boot_Backup_%date:~0,4%%date:~5,2%%date:~8,2%"
if exist "%E%\EFI\Microsoft\Boot" xcopy /e /h /y "%E%\EFI\Microsoft\Boot" "%BAK%\" >nul 2>&1&&echo 备份完成
xcopy /e /h /y "%U%\*" "%E%\" >nul 2>&1&&echo 复制修复文件成功||echo 复制失败
bcdboot C:\Windows /s %E% /f UEFI >nul 2>&1&&echo BCD重建成功||(copy /y "%B%" "%E%\EFI\Microsoft\Boot\BCD" >nul 2>&1&&echo BCD模板恢复成功||echo BCD失败)
del "%T%\d.txt" "%T%\e.txt"
echo.&echo 修复完成&pause&goto M

:C5
cls&echo.
echo ========== BIOS修复 ==========
bootsect /nt60 C: /mbr >nul 2>&1&&echo MBR修复成功||echo MBR失败
bootsect /nt60 C: >nul 2>&1&&echo 引导扇区修复成功||echo 引导扇区失败
bcdboot C:\Windows /s C: /f BIOS >nul 2>&1&&echo BCD重建成功||echo BCD失败
echo.&echo 修复完成&pause&goto M

:X
rmdir /s /q "%T%" >nul 2>&1
exit /b 0
pause