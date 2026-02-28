#!/bin/bash

echo "=== 开始一键修复 /opt 目录、应用商店和输入法 ==="

# 1. 重建 /opt 目录并修复权限
sudo mkdir -p /opt
sudo chmod 755 /opt
sudo chown root:root /opt
echo "✅ 已重建 /opt 目录并修复权限"

# 2. 修复系统依赖与软件包
sudo apt --fix-broken install -y
sudo dpkg --configure -a
echo "✅ 已修复系统依赖与损坏的软件包"

# 3. 清理并更新软件源缓存
sudo apt clean
sudo apt update -y
echo "✅ 已清理并更新软件源缓存"

# 4. 重新安装应用商店
sudo apt reinstall kylin-software-center -y
echo "✅ 已重新安装应用商店"

# 5. 安装输入法框架
sudo apt install fcitx-bin fcitx-table fcitx-config-gtk -y
echo "✅ 已安装 fcitx 输入法框架"

# 6. 下载并安装搜狗输入法
wget -O sogoupinyin.deb https://cdn2.ime.sogou.com/dl/index/1687243979/sogoupinyin_4.0.1.2800_x86_64.deb
sudo dpkg -i sogoupinyin.deb
sudo apt --fix-broken install -y
rm -f sogoupinyin.deb
echo "✅ 已安装搜狗输入法"

# 7. 重启输入法框架
fcitx -r
echo "✅ 已重启输入法框架"

echo "=== 修复完成！请注销当前用户再重新登录以生效所有配置 ==="