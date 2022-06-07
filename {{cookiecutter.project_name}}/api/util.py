import hashlib
import time
import datetime
import subprocess
import uuid
import random

from flask import current_app


def get_uuid() -> str:
    """生成UUID"""
    return uuid.uuid1().hex


def hash_key() -> str:
    """随机字符串"""
    hash = random.getrandbits(128)
    return "%032x" % hash


def md5(data: str) -> str:
    """md5数据"""
    return hashlib.md5(data.encode("utf8")).hexdigest()


def md5_file(file) -> str:
    """md5文件"""
    hash = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash.update(chunk)
    file.seek(0)
    return hash.hexdigest()


def sign_by_md5(data: dict, secret: str) -> str:
    """md5签名"""
    sort_data = sorted(data.items(), key=lambda m: m[0])
    data_str = "&".join(["%s=%s" % _d for _d in sort_data]) + secret
    return md5(data_str)


def date2ts(date: datetime.datetime) -> int:
    """本地时间转时间戳"""
    return int(time.mktime(date.timetuple()))


def date2str(date: datetime.datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间"""
    return datetime.datetime.strftime(date, fmt)


def ts2date(timestamp: int) -> datetime.datetime:
    """时间戳转本地时间"""
    return datetime.datetime.fromtimestamp(timestamp)


def now() -> datetime.datetime:
    """获取当前时间"""
    return datetime.datetime.now()


def now_ts() -> int:
    """获取当前时间戳"""
    return date2ts(now())


def now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间字符串"""
    return date2str(now(), fmt)


def command_execute(command: str) -> subprocess.CompletedProcess:
    """执行命令行"""
    p = subprocess.run(command.split(" "), capture_output=True, text=True)
    # current_app.logger.info(f"{command}: {p.stdout}")
    if p.stderr:
        current_app.logger.error(f"{command}: {p.stderr}")
    return p
