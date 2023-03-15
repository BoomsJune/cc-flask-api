import time
from datetime import datetime, timezone


def date_to_ts(date: datetime) -> int:
    """本地时间转时间戳"""
    return int(time.mktime(date.timetuple()))


def fmt_date(date: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """格式化时间"""
    return datetime.strftime(date, fmt)


def ts_to_date(timestamp: int) -> datetime:
    """时间戳转本地时间"""
    return datetime.fromtimestamp(timestamp)


def now() -> datetime:
    """获取当前时间（带本地时区）"""
    utc_dt = datetime.now(timezone.utc)
    return utc_dt.astimezone()


def now_ts() -> int:
    """获取当前时间戳"""
    return date_to_ts(now())


def now_str(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间字符串"""
    return fmt_date(now(), fmt)
