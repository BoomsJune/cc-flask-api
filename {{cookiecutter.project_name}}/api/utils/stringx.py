import hashlib
import uuid
import random
import string


def get_uuid() -> str:
    """生成UUID"""
    return uuid.uuid1().hex


def hash_key(size: int = 16) -> str:
    """随机字符串"""
    letters = string.ascii_letters + string.digits
    letterSize = len(letters)
    if size > letterSize:
        size = letterSize
    return "".join(random.sample(letters, size))


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
