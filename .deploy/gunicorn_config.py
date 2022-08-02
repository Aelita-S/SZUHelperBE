# !/usr/bin/env python3

import os

bind = '0.0.0.0:8000'  # 监听ip和端口号
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'  # 设置gunicorn访问日志格式，错误日志无法设置
worker_class = 'gevent'  # 使用gevent模式，默认的是sync模式
workers = int(int(os.getenv('MAX_WORKER_NUM', default=2)) / 2)
threads = 4
keep_alive = 32

max_requests = 1000000  # 请求数超过该数后自动重启worker
max_requests_jitter = 50000  # 加上随机数避免worker同时重启

# timeout = 120

if os.getenv("PROJ_ENV", "PROD") == "DEV":
    # 开发环境自动Reload
    reload = True
else:
    preload = True