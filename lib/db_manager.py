import pymysql
from pymysql import Error, cursors
from typing import Any, List, Dict, Optional, Tuple, Union
import streamlit as st
from contextlib import contextmanager


class DatabaseManager:
    """简化版 PyMySQL 数据库操作类"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化数据库连接

        Args:
            config: 数据库配置字典，包含以下键:
                - host: 数据库主机
                - port: 数据库端口
                - user: 用户名
                - password: 密码
                - database: 数据库名
        """
        if config is None:
            # 从 Streamlit secrets 获取配置
            try:

                self.config = {
                    'host': st.secrets["db"]["host"],
                    'port': st.secrets["db"]["port"],
                    'user': st.secrets["db"]["user"],
                    'password': st.secrets["db"]["password"],
                    'database': st.secrets["db"]["database"],
                    'charset': 'utf8mb4',
                    'cursorclass': cursors.DictCursor
                }
            except KeyError as e:
                st.error(f"缺少数据库配置: {e}")
                raise
        else:
            self.config = config
            self.config.setdefault('charset', 'utf8mb4')
            self.config.setdefault('cursorclass', cursors.DictCursor)

        self.connection = None
        self._connect()

    def _connect(self) -> None:
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**self.config)
        except Error as e:
            st.error(f"数据库连接失败: {e}")
            raise

    def reconnect(self) -> None:
        """重新连接数据库"""
        self.close()
        self._connect()

    def close(self) -> None:
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()

    def is_connected(self) -> bool:
        """检查数据库连接是否有效"""
        try:
            if self.connection and self.connection.open:
                self.connection.ping(reconnect=True)
                return True
            return False
        except Error:
            return False

    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        cursor = None
        try:
            # 确保连接有效
            if not self.is_connected():
                self.reconnect()

            cursor = self.connection.cursor()
            yield cursor
            self.connection.commit()
        except Error as e:
            if self.connection:
                self.connection.rollback()
            st.error(f"数据库操作失败: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

    def execute(self, query: str, params: Optional[Tuple] = None) -> List[Dict]:
        """
        执行查询语句并返回结果

        Args:
            query: SQL查询语句
            params: 查询参数

        Returns:
            查询结果列表
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def execute_non_query(self, query: str, params: Optional[Tuple] = None) -> int:
        """
        执行非查询语句（INSERT, UPDATE, DELETE）

        Args:
            query: SQL语句
            params: 参数

        Returns:
            受影响的行数
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def insert(self, table: str, data: Dict) -> int:
        """
        插入单条数据

        Args:
            table: 表名
            data: 要插入的数据字典

        Returns:
            插入的行ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self.get_cursor() as cursor:
            cursor.execute(query, tuple(data.values()))
            return cursor.lastrowid

    def update(self, table: str, data: Dict, condition: str, params: Optional[Tuple] = None) -> int:
        """
        更新数据

        Args:
            table: 表名
            data: 要更新的数据字典
            condition: WHERE条件
            params: 条件参数

        Returns:
            受影响的行数
        """
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"

        # 合并参数
        all_params = tuple(data.values()) + (params if params else ())

        with self.get_cursor() as cursor:
            cursor.execute(query, all_params)
            return cursor.rowcount

    def delete(self, table: str, condition: str, params: Optional[Tuple] = None) -> int:
        """
        删除数据

        Args:
            table: 表名
            condition: WHERE条件
            params: 条件参数

        Returns:
            受影响的行数
        """
        query = f"DELETE FROM {table} WHERE {condition}"

        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.rowcount

    def get_one(self, table: str, condition: str = "1=1", params: Optional[Tuple] = None) -> Optional[Dict]:
        """
        获取单条数据

        Args:
            table: 表名
            condition: WHERE条件
            params: 条件参数

        Returns:
            单条数据或None
        """
        query = f"SELECT * FROM {table} WHERE {condition} LIMIT 1"

        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()

    def get_all(self, table: str, condition: str = "1=1", params: Optional[Tuple] = None) -> List[Dict]:
        """
        获取所有匹配的数据

        Args:
            table: 表名
            condition: WHERE条件
            params: 条件参数

        Returns:
            数据列表
        """
        query = f"SELECT * FROM {table} WHERE {condition}"

        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

    def count(self, table: str, condition: str = "1=1", params: Optional[Tuple] = None) -> int:
        """
        统计数量

        Args:
            table: 表名
            condition: WHERE条件
            params: 条件参数

        Returns:
            数量
        """
        query = f"SELECT COUNT(*) as count FROM {table} WHERE {condition}"

        with self.get_cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result['count'] if result else 0

    def table_exists(self, table_name: str) -> bool:
        """
        检查表是否存在

        Args:
            table_name: 表名

        Returns:
            是否存在
        """
        query = """
                SELECT COUNT(*) as count
                FROM information_schema.tables
                WHERE table_schema = %s \
                  AND table_name = %s \
                """

        with self.get_cursor() as cursor:
            cursor.execute(query, (self.config['database'], table_name))
            result = cursor.fetchone()
            return result['count'] > 0 if result else False


# 在 Streamlit 中使用的单例模式
@st.cache_resource
def get_db():
    """获取数据库管理器单例"""
    return DatabaseManager()
