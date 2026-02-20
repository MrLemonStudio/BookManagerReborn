from Tools.custom_errors import UserExistsException
from Tools.sqlite_new import SQLiteDatabaseManager
import datetime
import os

class UserActionManager:
    def __init__(self,db_path,table_name):
        run_time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.log_dir_path = "../logs"
        if not os.path.exists(self.log_dir_path):
            os.mkdir(self.log_dir_path)
        self.log_location = f"{self.log_dir_path}/{run_time}.log"
        self.db_path = db_path
        self.table_name = table_name
        self.sqlite=SQLiteDatabaseManager(self.db_path)
        self.connection=self.sqlite.connect()
        self.cursor=self.connection.cursor()
        self.log_file=open(self.log_location,"w",encoding="utf-8",errors="ignore")

    def __create_user(self, user_name:str, password:str,is_administrator:bool=False)->bool:
        table_exist=self.sqlite.table_exists(self.table_name)
        if not table_exist:
            self.sqlite.create_table(self.table_name,{"user_name":"text unique not null","password":"text","id":"integer primary key not null","is_administrator":"boolean not null default false"})
        else:
            pass
        users_data_now=self.sqlite.query(f"select user_name,id from {self.table_name}")
        for i in users_data_now:
            try:
                if i["user_name"]==user_name:
                    raise UserExistsException(f"User {user_name} already exists")
            except UserExistsException as e:
                print(e)
                print(e,file=self.log_file)
                self.log_file.close()
                return False
        try:
            user_id=users_data_now[-1]["id"]+1
        except IndexError:
            user_id=1
        try:
            self.sqlite.execute_sql(f"insert into {self.table_name}(user_name,password,id,is_administrator) values(?,?,?,?)",(user_name,password,user_id,is_administrator))
        except Exception as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        return True
    def crur(self,user_name:str, password:str,is_administrator:bool=False)->bool:
        return self.__create_user(user_name,password,is_administrator)