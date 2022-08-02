#!/bin/sh

APP=/app
DATA=/app/data

autossh -M 59999 -fND 127.0.0.1:18118 "${SERVER_USERNAME}"@"${SERVER_IP}"

# 配置privoxy
sed -i '$a\forward-socks5 / 127.0.0.1:18118 .' /etc/privoxy/config
sed -i '$a\forward-socks5t / 127.0.0.1:18118 .' /etc/privoxy/config
privoxy /etc/privoxy/config

mkdir -p $DATA/config $DATA/log

# 生成secret.key
if [ ! -f "$DATA/config/secret.key" ]; then
  cat /dev/urandom | head -1 | md5sum | head -c 32 >"$DATA/config/secret.key"
fi

# 根据CPU核数得到worker数（核数小于2则为2）
if [ -z "$MAX_WORKER_NUM" ]; then
  CPU_CORE_NUM=$(grep -c ^processor /proc/cpuinfo)
  export CPU_CORE_NUM
  if [ "$CPU_CORE_NUM" -lt 2 ]; then
    export MAX_WORKER_NUM=2
  else
    export MAX_WORKER_NUM=$CPU_CORE_NUM
  fi
fi



sleep 10 # TODO 延长启动时间，暂时解决启动时数据库未就绪的问题
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --noinput
python manage.py inituser --username="$ROOT_USERNAME" --password="$ROOT_PASSWORD" --action=create_super_admin
python manage.py loaddata power/fixtures/power.json


exec supervisord -c $APP/.deploy/supervisord.ini
