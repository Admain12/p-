#!/usr/bin/env bash
set -euo pipefail

RED=$(tput setaf 1 2>/dev/null || echo "")
GREEN=$(tput setaf 2 2>/dev/null || echo "")
YELLOW=$(tput setaf 3 2>/dev/null || echo "")
BLUE=$(tput setaf 4 2>/dev/null || echo "")
CYAN=$(tput setaf 6 2>/dev/null || echo "")
BOLD=$(tput bold 2>/dev/null || echo "")
RESET=$(tput sgr0 2>/dev/null || echo "")

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "${RED}错误: 缺少命令 $1${RESET}" >&2
    exit 1
  }
}

need_cmd nmcli
need_cmd ip

clear
echo
echo "${BOLD}${CYAN}===============================================================${RESET}"
echo "${BOLD}${CYAN}                                                               ${RESET}"
echo "${BOLD}${CYAN}          Bond 网卡绑定配置工具 v2.0                          ${RESET}"
echo "${BOLD}${CYAN}          By:虚拟化时代君 - 自动化网络配置                    ${RESET}"
echo "${BOLD}${CYAN}                                                               ${RESET}"
echo "${BOLD}${CYAN}===============================================================${RESET}"
echo

mapfile -t IFACES < <( 
  nmcli -t -f DEVICE,TYPE device status | 
  awk -F: ' 
    $2=="ethernet" || $2=="infiniband" { 
      dev=$1 
      if (dev!="lo" && dev!~/(^bond|^br|^virbr|^docker|^veth|^tun|^tap|^wg|^sit|^gre|^vlan|^team)/) print dev 
    }'
)

if (( ${#IFACES[@]} < 2 )); then
  echo "${RED}错误: 可用物理网卡少于 2 块, 无法创建 bond${RESET}"
  nmcli device status
  exit 1
fi

echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo "${BOLD}${BLUE} 可用物理网卡列表                                              ${RESET}"
echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo
for i in "${!IFACES[@]}"; do
  dev="${IFACES[$i]}"
  state=$(nmcli -t -f DEVICE,STATE device status | awk -F: -v d="$dev" '$1==d{print $2}')
  mac=$(nmcli -t -f GENERAL.HWADDR device show "$dev" 2>/dev/null | cut -d: -f2- || echo "unknown")
  ip4=$(ip -4 -o addr show "$dev" 2>/dev/null | awk '{print $4}' | head -n1 || echo "none")
  printf "  ${BOLD}${YELLOW}[%d]${RESET} ${CYAN}%-12s${RESET} 状态: ${GREEN}%-12s${RESET} IP: ${YELLOW}%-18s${RESET} MAC: ${BLUE}%s${RESET}\n" "$i" "$dev" "$state" "${ip4}" "${mac}"
done
echo

echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo "${BOLD}${BLUE} Bond 基本配置                                                ${RESET}"
echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo
read -rp "  ${BOLD}Bond 接口名称${RESET} (默认 bond0): " BOND_NAME
BOND_NAME="${BOND_NAME:-bond0}"
echo

echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo "${BOLD}${BLUE} Bond 工作模式选择                                            ${RESET}"
echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo
echo "  ${YELLOW}1)${RESET} balance-rr      (轮询模式)"
echo "  ${YELLOW}2)${RESET} active-backup   (主备模式) ${GREEN}推荐${RESET}"
echo "  ${YELLOW}3)${RESET} balance-xor     (XOR 哈希分流)"
echo "  ${YELLOW}4)${RESET} broadcast       (广播模式)"
echo "  ${YELLOW}5)${RESET} 802.3ad (LACP)  (动态链路聚合) ${GREEN}生产推荐${RESET}"
echo "  ${YELLOW}6)${RESET} balance-tlb     (发送负载均衡)"
echo "  ${YELLOW}7)${RESET} balance-alb     (发送+接收负载均衡)"
echo
read -rp "  ${BOLD}请选择模式${RESET} (默认 2): " MODE_NO
MODE_NO="${MODE_NO:-2}"

case "$MODE_NO" in
  1) BOND_MODE="balance-rr" ;;
  2) BOND_MODE="active-backup" ;;
  3) BOND_MODE="balance-xor" ;;
  4) BOND_MODE="broadcast" ;;
  5) BOND_MODE="802.3ad" ;;
  6) BOND_MODE="balance-tlb" ;;
  7) BOND_MODE="balance-alb" ;;
  *) echo "${RED}无效的模式选择${RESET}"; exit 1 ;;
esac
echo

echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo "${BOLD}${BLUE} IPv4 配置方式                                                ${RESET}"
echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo
echo "  ${YELLOW}1)${RESET} DHCP (自动获取) ${GREEN}默认${RESET}"
echo "  ${YELLOW}2)${RESET} 静态 IP (手动指定)"
echo
read -rp "  ${BOLD}请选择配置方式${RESET} (默认 1): " IP_MODE
IP_MODE="${IP_MODE:-1}"

ADDR_CIDR=""
GATEWAY=""
DNS_SERVERS=""

if [[ "$IP_MODE" == "2" ]]; then
  IP_METHOD="manual"
  echo
  read -rp "  IPv4 地址 (如 192.168.1.100): " IPADDR
  read -rp "  子网前缀 (如 24): " PREFIX
  ADDR_CIDR="${IPADDR}/${PREFIX}"

  read -rp "  配置默认网关? (y/N): " GW_YN
  if [[ "$GW_YN" =~ ^[Yy]$ ]]; then
    read -rp "    网关地址: " GATEWAY
  fi

  read -rp "  配置 DNS? (y/N): " DNS_YN
  if [[ "$DNS_YN" =~ ^[Yy]$ ]]; then
    read -rp "    DNS 服务器 (多个用逗号分隔): " DNS_SERVERS
  fi
else
  IP_METHOD="auto"
fi
echo

echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo "${BOLD}${BLUE} 选择网卡 (至少 2 块)                                         ${RESET}"
echo "${BOLD}${BLUE}---------------------------------------------------------------${RESET}"
echo
read -rp "  ${BOLD}输入网卡序号${RESET} (用空格分隔, 如: 0 1): " -a IDX

if (( ${#IDX[@]} < 2 )); then
  echo "${RED}错误: 至少需要选择 2 块网卡${RESET}"
  exit 1
fi

SLAVES=()
for id in "${IDX[@]}"; do
  if ! [[ "$id" =~ ^[0-9]+$ ]] || (( id >= ${#IFACES[@]} )); then
    echo "${RED}错误: 无效序号 $id${RESET}"
    exit 1
  fi
  SLAVES+=("${IFACES[$id]}")
done

echo
echo "${BOLD}${GREEN}===============================================================${RESET}"
echo "${BOLD}${GREEN} 配置预览                                                     ${RESET}"
echo "${BOLD}${GREEN}===============================================================${RESET}"
printf "  ${BOLD}Bond 接口名${RESET} : ${YELLOW}%s${RESET}\n" "$BOND_NAME"
printf "  ${BOLD}工作模式${RESET}     : ${YELLOW}%s${RESET}\n" "$BOND_MODE"
printf "  ${BOLD}IPv4 配置${RESET}  : ${YELLOW}%s${RESET}\n" "$( [ "$IP_METHOD" = "auto" ] && echo "DHCP (自动获取)" || echo "静态 IP: $ADDR_CIDR" )"
if [ "$IP_METHOD" = "manual" ]; then
  [[ -n "$GATEWAY" ]] && printf "  ${BOLD}默认网关${RESET}     : ${YELLOW}%s${RESET}\n" "$GATEWAY"
  [[ -n "$DNS_SERVERS" ]] && printf "  ${BOLD}DNS 服务器${RESET} : ${YELLOW}%s${RESET}\n" "$DNS_SERVERS"
fi
printf "  ${BOLD}Slave 网卡${RESET} : ${YELLOW}%s${RESET}\n" "${SLAVES[*]}"
echo "${BOLD}${GREEN}===============================================================${RESET}"
echo

# 确认配置
echo "${BOLD}${YELLOW}注意: 配置将立即生效, 当前网卡连接会中断并重新配置${RESET}"
echo
read -rp "${BOLD}是否继续?${RESET} (y/N): " CONFIRM
if ! [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
  echo "${BOLD}${BLUE}配置已取消${RESET}"
  exit 0
fi

echo
echo "${BOLD}${CYAN}开始配置 bond 网卡...${RESET}"

# 1. 停止所有选中的网卡
echo "  ${BOLD}步骤 1: 停用选中的物理网卡${RESET}"
for slave in "${SLAVES[@]}"; do
  echo "    - 停用网卡 $slave"
  nmcli device disconnect "$slave" 2>/dev/null || true
  nmcli connection down "$slave" 2>/dev/null || true
  nmcli connection delete "$slave" 2>/dev/null || true
  sleep 1

done

# 2. 创建 bond 接口
echo "  ${BOLD}步骤 2: 创建 bond 接口${RESET}"

echo "    - 创建 bond 连接 $BOND_NAME"

# 构建 nmcli 命令
NMCLI_CMD="nmcli connection add type bond ifname $BOND_NAME con-name $BOND_NAME bond.mode $BOND_MODE bond.miimon 100"

# 添加 IP 配置
if [ "$IP_METHOD" = "manual" ]; then
  NMCLI_CMD+=" ip4 $ADDR_CIDR"
  if [[ -n "$GATEWAY" ]]; then
    NMCLI_CMD+=" gw4 $GATEWAY"
  fi
  if [[ -n "$DNS_SERVERS" ]]; then
    NMCLI_CMD+=" ipv4.dns '$DNS_SERVERS'"
  fi
else
  NMCLI_CMD+=" ip4 auto"
fi

# 执行命令
$NMCLI_CMD

# 3. 添加从网卡
echo "  ${BOLD}步骤 3: 将物理网卡添加到 bond${RESET}"
for slave in "${SLAVES[@]}"; do
  echo "    - 添加网卡 $slave 到 bond"
  nmcli connection add type bond-slave ifname "$slave" con-name "bond-slave-$slave" master "$BOND_NAME"
  sleep 1

done

# 4. 启动 bond 接口
echo "  ${BOLD}步骤 4: 启动 bond 接口${RESET}"
echo "    - 启用 bond 接口 $BOND_NAME"
nmcli connection up "$BOND_NAME"

# 5. 启动从网卡
echo "  ${BOLD}步骤 5: 启用所有从网卡${RESET}"
for slave in "${SLAVES[@]}"; do
  echo "    - 启用网卡 $slave"
  nmcli connection up "bond-slave-$slave"
  sleep 1

done

# 6. 验证配置
echo "  ${BOLD}步骤 6: 验证配置${RESET}"
echo "    - 显示 bond 状态"
cat /proc/net/bonding/$BOND_NAME

echo

# 显示完成信息
echo "${BOLD}${GREEN}===============================================================${RESET}"
echo "${BOLD}${GREEN} Bond 网卡配置完成!                                          ${RESET}"
echo "${BOLD}${GREEN}===============================================================${RESET}"
printf "  ${BOLD}Bond 接口名${RESET} : ${YELLOW}%s${RESET}\n" "$BOND_NAME"
printf "  ${BOLD}IP 地址${RESET}       : ${YELLOW}%s${RESET}\n" "$(ip -4 -o addr show "$BOND_NAME" 2>/dev/null | awk '{print $4}' | head -n1 || echo "无")"
printf "  ${BOLD}状态${RESET}         : ${GREEN}已激活${RESET}\n"
echo "${BOLD}${GREEN}===============================================================${RESET}"
echo
