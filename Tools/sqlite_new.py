
#By Deepseek
#I deleted a few examples of this

import sqlite3
from typing import List, Union, Dict, Any
from pathlib import Path
import logging
from contextlib import closing


class SQLiteDatabaseManager:
    """可重用的SQLite数据库管理器"""

    def __init__(self, db_path: Union[str, Path], enable_foreign_keys: bool = True):
        """
        初始化数据库管理器

        Args:
            db_path: 数据库文件路径
            enable_foreign_keys: 是否启用外键约束（SQLite默认关闭）
        """
        self.db_path = Path(db_path)
        self.enable_foreign_keys = enable_foreign_keys
        self.connection = None
        self._setup_logging()

    def _setup_logging(self):
        """设置日志"""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def connect(self) -> sqlite3.Connection:
        """建立数据库连接并返回连接对象"""
        try:
            # 确保父目录存在
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

            # 使用uri模式以支持额外的连接参数
            db_uri = f"file:{self.db_path}?mode=rwc"

            # 连接数据库
            conn = sqlite3.connect(db_uri, uri=True)
            conn.row_factory = sqlite3.Row  # 启用行工厂以字典形式返回结果

            # 启用外键约束（SQLite默认关闭）
            if self.enable_foreign_keys:
                conn.execute("PRAGMA foreign_keys = ON")

            # 优化性能设置
            conn.execute("PRAGMA journal_mode = WAL")  # 使用WAL模式提高并发性能
            conn.execute("PRAGMA synchronous = NORMAL")  # 在安全性和性能间平衡
            conn.execute("PRAGMA cache_size = -2000")  # 设置缓存大小为2MB

            self.connection = conn
            self.logger.info(f"成功连接到数据库: {self.db_path}")
            return conn

        except sqlite3.Error as e:
            self.logger.error(f"数据库连接失败: {e}")
            raise

    def execute_sql(self, sql: str, parameters: tuple = None,
                    commit: bool = True) -> sqlite3.Cursor:
        """
        执行SQL语句

        Args:
            sql: SQL语句
            parameters: 参数元组
            commit: 是否自动提交

        Returns:
            sqlite3.Cursor对象
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            if parameters:
                cursor.execute(sql, parameters)
            else:
                cursor.execute(sql)

            if commit:
                self.connection.commit()

            return cursor

        except sqlite3.Error as e:
            self.logger.error(f"SQL执行失败: {e}\nSQL: {sql}")
            if self.connection:
                self.connection.rollback()
            raise

    def execute_many(self, sql: str, parameters_list: List[tuple]) -> None:
        """
        批量执行SQL语句

        Args:
            sql: SQL语句
            parameters_list: 参数列表
        """
        if self.connection is None:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql, parameters_list)
            self.connection.commit()

        except sqlite3.Error as e:
            self.logger.error(f"批量SQL执行失败: {e}")
            self.connection.rollback()
            raise

    def create_table(self, table_name: str, columns: Dict[str, str],
                     constraints: List[str] = None, if_not_exists: bool = True) -> None:
        """
        创建表

        Args:
            table_name: 表名
            columns: 列定义字典 {列名: 数据类型和约束}
            constraints: 表级约束列表
            if_not_exists: 如果表不存在则创建
        """
        if_not_exists_clause = "IF NOT EXISTS " if if_not_exists else ""

        # 构建列定义
        columns_sql = ", ".join([f"{col_name} {col_def}"
                                 for col_name, col_def in columns.items()])

        # 添加表级约束
        if constraints:
            columns_sql += ", " + ", ".join(constraints)

        sql = f"CREATE TABLE {if_not_exists_clause}{table_name} ({columns_sql})"

        self.execute_sql(sql)
        self.logger.info(f"表 '{table_name}' 创建成功")

    def create_index(self, index_name: str, table_name: str,
                     columns: List[str], unique: bool = False) -> None:
        """
        创建索引

        Args:
            index_name: 索引名
            table_name: 表名
            columns: 列名列表
            unique: 是否创建唯一索引
        """
        unique_clause = "UNIQUE " if unique else ""
        columns_str = ", ".join(columns)

        sql = f"CREATE {unique_clause}INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns_str})"
        self.execute_sql(sql)
        self.logger.info(f"索引 '{index_name}' 创建成功")

    def query(self, sql: str, parameters: tuple = None) -> List[Dict[str, Any]]:
        """
        查询数据

        Args:
            sql: SQL查询语句
            parameters: 参数元组

        Returns:
            字典列表形式的结果
        """
        cursor = self.execute_sql(sql, parameters, commit=False)
        rows = cursor.fetchall()

        # 转换为字典列表
        return [dict(row) for row in rows]

    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        sql = """
              SELECT name \
              FROM sqlite_master
              WHERE type = 'table' \
                AND name = ? \
              """
        result = self.query(sql, (table_name,))
        return len(result) > 0

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """获取表结构信息"""
        return self.query(f"PRAGMA table_info({table_name})")

    def close(self) -> None:
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("数据库连接已关闭")

    def __enter__(self):
        """上下文管理器入口"""
        if self.connection is None:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()

    def backup_database(self, backup_path: Union[str, Path]) -> None:
        """
        备份数据库

        Args:
            backup_path: 备份文件路径
        """
        backup_path = Path(backup_path)
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with closing(sqlite3.connect(backup_path)) as backup_conn:
                self.connection.backup(backup_conn)
            self.logger.info(f"数据库备份成功: {backup_path}")

        except sqlite3.Error as e:
            self.logger.error(f"数据库备份失败: {e}")
            raise


