from email.policy import default
import click
from flask.cli import AppGroup

from api.models import AuthUser


user_cli = AppGroup("user")


@user_cli.command("create")
@click.option("--name", prompt="用户名", help="用于登录的用户名")
@click.password_option(prompt="密码", confirmation_prompt="重复密码", help="用于登录的密码")
@click.option("--super", is_flag=True, show_default=True, default=True, prompt="是否为超级用户", help="设置用户为超级管理员")
def create_user(name, password, super):
    """创建用户"""
    user = AuthUser(username=name, password=password, is_superuser=1 if super else 0)
    user.create()
    click.echo("创建成功！")


@user_cli.command("delete")
@click.option("--name", prompt="用户名", help="用于登录的用户名")
@click.confirmation_option(prompt="确认删除该用户？", help="删除操作确认")
def delete_user(name):
    """删除用户"""
    user = AuthUser.get_by_username(name)
    if not user:
        click.echo(f"删除失败，用户名{name}不存在！")
    else:
        user.delete()
        click.echo("删除成功！")


def init_app(app):
    app.cli.add_command(user_cli)
