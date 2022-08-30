#!/usr/bin/bash

init_supervisord(){

> $1
cat>>$1<<EOF

[program:${SPUG_APP_NAME}]
directory=${SPUG_DST_DIR}
command=${python_path}/bin/gunicorn run:app
stdout_logfile=${LOG_PATH}/${SPUG_APP_NAME}/sup_api.log
stderr_logfile=${LOG_PATH}/${SPUG_APP_NAME}/sup_api_error.log
autostart=true
autorestart=true

[program:${SPUG_APP_NAME}_celery_worker]
directory=${SPUG_DST_DIR}
command=${python_path}/bin/celery -A runcelery.celery worker -l INFO
stdout_logfile=${LOG_PATH}/${SPUG_APP_NAME}/sup_celery_worker.log
redirect_stderr=true
autostart=true
autorestart=true

[program:${SPUG_APP_NAME}_celery_beat]
directory=${SPUG_DST_DIR}
command=${python_path}/bin/celery -A runcelery.celery beat -l INFO
stdout_logfile=${LOG_PATH}/${SPUG_APP_NAME}/sup_celery_beat.log
redirect_stderr=true
autostart=true
autorestart=true

EOF
}