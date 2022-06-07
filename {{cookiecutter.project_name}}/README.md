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

> - 默认加载`.flaskenv`的环境变量，后加载`.env`的环境变量
>
> - 请在`.env`中修改配置，请勿提交`.env`


```bash
cp .flaskenv .env
vim .env
```

3. 数据库更新
   > 若导入已有数据的数据库， 请先`truncate alembic_version`

```bash
flask db migrate
flask db upgrade
```

4. 运行

```bash
# 启动API
flask run
```

## Deploy

> 命令已集成到`deploy.sh`中，若不需要更新环境，可只执行`docker-compose up -d --build`

```bash
# 1. build base image
docker build -t {{cookiecutter.project_name}}:base -f Dockerfile.base .

# 2. deploy
docker-compose up -d --build
```
