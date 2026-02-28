@echo off
chcp 65001 > nul 

set cd D:\Program Files(86)\VMware
set cd C:\windows\System32\Microsoft\Protect
copy C:\test.txt d:\#复制 an 
type c:\boot.ini

#!/bin/bash
# 应用自动部署脚本
# 功能：拉取Git代码、编译打包、启停服务、版本回滚
# 作者：DevOps Engineer
# 日期：2026-01-04
# 适用场景：Java Spring Boot应用，基于Systemd管理服务

# -------------------------- 配置参数 --------------------------
APP_NAME="user-service"          # 应用名称
GIT_REPO="https://gitlab.example.com/dev/user-service.git"  # Git仓库地址
GIT_BRANCH="release-1.0"         # 部署分支/标签
APP_DIR="/opt/apps/${APP_NAME}"   # 应用部署目录
JAR_NAME="${APP_NAME}.jar"       # 应用Jar包名称
LOG_DIR="/var/log/${APP_NAME}"    # 应用日志目录
BACKUP_DIR="${APP_DIR}/backup"    # 版本备份目录
JAVA_OPTS="-Xms512m -Xmx1024m"    # Java运行参数
SERVICE_NAME="${APP_NAME}.service" # Systemd服务名

# -------------------------- 函数定义 --------------------------
# 日志记录函数
log() {
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[${timestamp}] [${1}] ${2}" >> "${LOG_DIR}/deploy.log"
    echo "[${timestamp}] [${1}] ${2}"
}

# 检查命令执行结果
check_result() {
    if [ $? -ne 0 ]; then
        log "ERROR" "${1} 执行失败，脚本退出"
        exit 1
    else
        log "INFO" "${1} 执行成功"
    fi
}

# 备份当前版本
backup_current_version() {
    log "INFO" "开始备份当前版本"
    mkdir -p "${BACKUP_DIR}"
    if [ -f "${APP_DIR}/${JAR_NAME}" ]; then
        local backup_file="${BACKUP_DIR}/${JAR_NAME}.$(date +%Y%m%d%H%M%S)"
        cp "${APP_DIR}/${JAR_NAME}" "${backup_file}"
        check_result "版本备份"
    else
        log "WARN" "当前无已部署版本，跳过备份"
    fi
}

# 拉取Git代码并编译打包
pull_and_build() {
    log "INFO" "开始拉取Git代码（分支：${GIT_BRANCH}）"
    if [ ! -d "${APP_DIR}/src" ]; then
        git clone "${GIT_REPO}" "${APP_DIR}/src"
        check_result "Git仓库克隆"
    fi
    cd "${APP_DIR}/src" || exit 1
    git checkout "${GIT_BRANCH}"
    check_result "切换至分支${GIT_BRANCH}"
    git pull origin "${GIT_BRANCH}"
    check_result "拉取最新代码"
    
    log "INFO" "开始编译打包"
    ./mvnw clean package -DskipTests
    check_result "Maven打包"
    cp "target/${JAR_NAME}" "${APP_DIR}/"
    check_result "复制Jar包至部署目录"
}

# 停止应用服务
stop_service() {
    log "INFO" "开始停止${APP_NAME}服务"
    systemctl stop "${SERVICE_NAME}"
    check_result "服务停止"
    # 等待进程退出
    sleep 5
    if pgrep -f "${JAR_NAME}" > /dev/null; then
        log "WARN" "服务进程未正常退出，强制杀死"
        pkill -f "${JAR_NAME}"
    fi
}

# 启动应用服务
start_service() {
    log "INFO" "开始启动${APP_NAME}服务"
    systemctl start "${SERVICE_NAME}"
    check_result "服务启动"
    # 检查服务状态
    sleep 10
    if systemctl is-active --quiet "${SERVICE_NAME}"; then
        log "INFO" "${APP_NAME}服务启动成功，状态正常"
    else
        log "ERROR" "${APP_NAME}服务启动失败，查看日志获取详情"
        exit 1
    fi
}

# 版本回滚（回滚至最近一次备份）
rollback_version() {
    log "INFO" "开始执行版本回滚"
    local latest_backup=$(ls -lt "${BACKUP_DIR}/${JAR_NAME}."* 2>/dev/null | head -n 1 | awk '{print $9}')
    if [ -z "${latest_backup}" ]; then
        log "ERROR" "无备份版本可回滚，脚本退出"
        exit 1
    fi
    stop_service
    cp "${latest_backup}" "${APP_DIR}/${JAR_NAME}"
    check_result "恢复备份版本（${latest_backup}）"
    start_service
}

# -------------------------- 主逻辑 --------------------------
# 初始化日志目录
mkdir -p "${LOG_DIR}"

# 解析命令行参数
case "$1" in
    deploy)
        backup_current_version
        pull_and_build
        stop_service
        start_service
        log "INFO" "${APP_NAME}部署完成"
        ;;
    rollback)
        rollback_version
        log "INFO" "${APP_NAME}版本回滚完成"
        ;;
    stop)
        stop_service
        log "INFO" "${APP_NAME}服务停止完成"
        ;;
    start)
        start_service
        ;;
    restart)
        stop_service
        start_service
        log "INFO" "${APP_NAME}服务重启完成"
        ;;
    *)
        echo "用法：$0 {deploy|rollback|start|stop|restart}"
        echo "  deploy  - 部署应用（拉取代码、打包、启停服务）"
        echo "  rollback - 回滚至最近一次备份版本"
        echo "  start/stop/restart - 启停/重启服务"
        exit 1
        ;;
esac
set a[0]=10
set b[1]=6
cls set
%~dp0
set %var% a=b\a
set %var% b=a*b
::显示应算出来的值
echo “a"  Rem Adding an element at end of an array
set [2] = ?
