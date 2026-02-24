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

    def __new_book(self,book_name:str,book_id:int|float|str,book_price:int|float|None=None,author:str|None=None,picture:str|Path|None=None)->bool:

        return True