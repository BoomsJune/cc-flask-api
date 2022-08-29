#!/usr/bin/bash

tips(){
    if [ $1 -ne 0 ]; then
        echo -e "ERROR:" $3
        exit 1
    else
        echo -e "SUCCESS:" $2
    fi
}

info(){
    echo -e "INFO:" $1
}

error(){
    echo -e "ERROR:" $1
    exit 1
}

info "校验环境变量"
for var in "ENV_PATH" "LOG_PATH"
do
    if [ -z ${!var} ];then
        error "缺少环境变量: $var"
    else
        echo "$var = ${!var}"
    fi
done

info "进入python虚拟环境"
python_path="${ENV_PATH}/${SPUG_APP_NAME}"
if [ ! -d ${python_path} ]; then
    info "初始化项目依赖的Python虚拟环境: ${python_path}"
    python3 -m venv ${python_path}
else
    info "python虚拟目录${python_path}已存在，跳过..."
fi
source ${python_path}/bin/activate

info "安装python依赖"
pip install --upgrade pip
pip install -r requirements.txt
tips $? "python依赖安装成功" "python依赖安装失败"

info "更新supervisor配置"
. ./deploy/supervisor/supervisor.ini.sh
init_supervisord "/etc/supervisord.d/${SPUG_APP_NAME}.ini"
supervisorctl update

info "更新环境变量配置"
/bin/cp -f ${ENV_PATH}/${SPUG_APP_NAME}.env .env

info "开始启动服务"
for server_name in "${SPUG_APP_NAME}" "${SPUG_APP_NAME}_celery_worker" "${SPUG_APP_NAME}_celery_beat"
do
    supervisorctl restart ${server_name}
    supervisorctl status ${server_name} | grep RUNNING
    tips $? "节点 ${server_name} 启动成功" "节点 ${server_name} 启动失败"
done


