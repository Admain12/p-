@echo off
chcp 65001 >nul
echo 正在修复EXE文件关联...
assoc .exe=exefile
ftype exefile="%%1" %%*

echo 正在修复BAT文件关联...
assoc .bat=batfile
ftype batfile="%%1" %%*

echo 正在修复CMD文件关联...
assoc .cmd=cmdfile
ftype cmdfile="%%1" %%*

echo 正在修复COM文件关联...
assoc .com=comfile
ftype comfile="%%1" %%*

echo 正在修复REG文件关联...
assoc .reg=regfile
ftype regfile=regedit.exe "%%1"

echo 正在修复MSI文件关联...
assoc .msi=WindowsInstallerPackage
ftype WindowsInstallerPackage=msiexec.exe /i "%%1" %%*

echo 所有核心文件关联修复完成！
pause