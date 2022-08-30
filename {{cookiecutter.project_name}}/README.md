## {{cookiecutter.project_title}}

{{cookiecutter.project_description}}

## Develop

1. 安装

```bash
python3 -m venv venv
source venv venv

pip install -r requirements.txt

# 安装 git hooks 到.git目录用于提交前格式校验（black/flake8）
pre-commit install
```

2. 修改配置

> 默认加载`.flaskenv`的环境变量，若存在`.env`，则先加载`.env`的环境变量
>
> 本地配置请在`.env`中修改配置，请勿提交`.env`

```bash
cp .flaskenv .env
vim .env
```

3. 数据库更新（可选）
> 本地版本对齐：`flask db stamp head`
> 
> 若导入已有数据的数据库， 请先`truncate alembic_version`

```bash
flask db migrate
flask db upgrade
```

4. 运行

```bash
# 启动API
flask run

# 启动celery
celery -A runcelery.celery worker -l INFO
celery -A runcelery.celery beat -l INFO
```

## Deploy

> 生产环境使用`gunicorn`实现WSGI，相关配置在`gunicorn.config.py`

### Docker
```bash
# 含环境更新使用deploy.sh
sh deploy/docker/deploy.sh

# 仅更新代码使用restart.sh
sh deploy/docker/restart.sh

# 停止部署并删除容器
sh deploy/docker/stop.sh
```

### supervisor
```bash
sh deploy/supervisor/deploy.sh
```
