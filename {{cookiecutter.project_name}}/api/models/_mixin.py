from api.extensions.db import db
from flask_sqlalchemy import Pagination


class CRUDMixin(db.Model):
    """基础数据模型 含增删改查"""

    __abstract__ = True

    MAX_PAGE_SIZE = 100  # 最大页大小

    def create(self):
        """创建"""
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        """更新"""
        db.session.commit()
        return self

    def delete(self):
        """删除"""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def base_query(cls):
        """基础查询条件"""
        return cls.query

    @classmethod
    def get_all(cls):
        """获取所有数据"""
        return cls.base_query().all()

    @classmethod
    def get_by_page(cls, current=1, page_size=20, query=None, order_by: list = None, **kwargs) -> Pagination:
        """分页获取数据

        Args:
            current (int, optional): 当前页. Defaults to 1.
            page_size (int, optional): 页面大小. Defaults to 20.
            query (_type_, optional): 查询条件. Defaults to None.
            order_by (list, optional): 排序 传入字符串列表
                                       默认升序，使用'-'表示降序 如['-id']表示按id降序.
                                       Defaults to None.

        Returns:
            Pagination: sqlalchemy分页对象
        """
        query = query if query is not None else cls.base_query()

        if order_by is not None:
            _orders = [getattr(cls, b[1:]).desc() if b.startswith("-") else getattr(cls, b).asc() for b in order_by]
            query = query.order_by(*_orders)

        return query.paginate(page=current, per_page=page_size, error_out=False, max_per_page=cls.MAX_PAGE_SIZE)


class LogMixin(db.Model):
    """标记需要操作记录的model

    继承LogMixin的模型类最好补充以下信息：
    1. 重写__repr__()
    """

    __abstract__ = True
