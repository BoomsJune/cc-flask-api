import os

from flask import current_app
from werkzeug.utils import secure_filename

from api.util import md5_file
from api.exception import APIException


class FileService:
    @classmethod
    def join(cls, dir: str, *args) -> str:
        """获取目录绝对路径

        Args:
            dir (str): 子目录路径，不需要以'/'开头

        Returns:
            str: 绝对路径
        """
        return os.path.join(current_app.config["UPLOAD_PATH"], dir, *args)

    @classmethod
    def relpath(cls, path: str) -> str:
        """获取相对路径

        Args:
            path (str): 路径

        Returns:
            str: 相对路径
        """
        return os.path.relpath(path, current_app.config["UPLOAD_PATH"])

    @classmethod
    def allowed_file(cls, filename: str, extensions: list) -> bool:
        """文件扩展名校验

        Args:
            filename (str): 文件名
            extensions (list): 允许的扩展名

        Returns:
            bool: 是否允许
        """
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in extensions
        )

    @classmethod
    def upload(cls, file, subdir: str, new_name: str = None) -> str:
        """上传文件

        Args:
            file (BinaryIO): 文件
            subdir (str): 子目录，不需要以'/'开头
            new_name (str): 指定文件名，如果没有指定则默认内容md5

        Returns:
            str: 存储相对路径
        """

        # create dir
        # subdir = os.path.join(subdir, now_str('%Y%m'))
        filepath = cls.join(subdir)
        if not cls.exists(filepath):
            os.makedirs(filepath)

        # change name
        filename_arr = file.filename.rsplit(".", 1)
        if not new_name:
            new_name = md5_file(file)
        new_filename = secure_filename(new_name + "." + filename_arr[1])

        # save
        file.save(os.path.join(filepath, new_filename))

        return os.path.join(subdir, new_filename)

    @classmethod
    def remove(cls, filepath: str):
        """删除文件

        Args:
            filepath (str): 文件位置
        """
        if not os.path.exists(filepath):
            raise APIException("文件不存在")
        os.remove(filepath)

    @classmethod
    def exists(cls, path: str) -> bool:
        """判断文件是否存在

        Args:
            path (str): 文件位置

        Returns:
            bool: 是否存在
        """
        return os.path.exists(path)
