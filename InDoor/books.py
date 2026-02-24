from Tools.custom_errors import *
from pathlib import Path
from Tools.sqlite_new import SQLiteDatabaseManager
import datetime
import os

class BooksManager:
    def __init__(self,db_path:str,table_name:str,log_dir_path:str|Path):
        run_time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.log_dir_path = log_dir_path
        if not os.path.exists(self.log_dir_path):
            os.mkdir(self.log_dir_path)
        self.log_location = f"{self.log_dir_path}/{run_time}.log"
        self.db_path = db_path
        self.table_name = table_name
        self.sqlite=SQLiteDatabaseManager(self.db_path)
        self.log_file=open(self.log_location,"w",encoding="utf-8",errors="ignore")

    def __new_book(self,book_name:str,book_id:int|float|str,book_price:int|float|None=None,author:str|None=None,picture:bytes|None=None)->bool:
        try:
            if (not book_name) or (not book_id):
                raise NameMatchesException("Book name or book id is required")
            else:
                pass
        except NameMatchesException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        table_exist = self.sqlite.table_exists(self.table_name)
        if not table_exist:
            self.sqlite.create_table(self.table_name, {"book_name": "text not null",
                                                       "book_id": "text primary key not null",
                                                       "book_price": "real",
                                                       "author": "text",
                                                       "picture": "blob"})
        else:
            pass
        books_data_now = self.sqlite.query(f"select book_id from {self.table_name}")
        try:
            for i in books_data_now:
                if book_id == i["book_id"]:
                    raise ExistsException(f"Book {book_name} already exists")
        except ExistsException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        try:
            self.sqlite.execute_sql(f"insert into {self.table_name} (book_name,book_id,book_price,author,picture) values (?,?,?,?,?)",
                                    (book_name,book_id,book_price,author,picture))
        except Exception as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        return True
    def nebk(self,book_name:str,book_id:int|float|str,book_price:int|float|None=None,author:str|None=None,picture:bytes|None=None)->bool:
        return self.__new_book(book_name,book_id,book_price,author,picture)