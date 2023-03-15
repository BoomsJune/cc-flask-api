import subprocess


def execute(command: str) -> subprocess.CompletedProcess:
    """执行命令行"""
    p = subprocess.run(command.split(" "), capture_output=True, text=True)
    return p
