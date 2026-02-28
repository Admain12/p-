@echo off
chcp 65001 >nul
echo 正在优化系统服务（谨慎运行，建议先备份服务状态）
:: 禁用远程注册表服务（降低安全风险）
sc config RemoteRegistry start= disabled
:: 禁用Windows Search（提升机械硬盘性能）
sc config WSearch start= disabled
:: 禁用Superfetch（SSD用户建议关闭）
sc config SysMain start= disabled
echo 服务优化完成，部分优化需重启生效！	
pause
