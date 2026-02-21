from Tools.custom_errors import *
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

    def __login_user(self, user_name:str|None, password:str, user_id: None | int)->bool:
        user_name_searched=self.sqlite.query(f"select user_name,password,id,is_administrator from {self.table_name} where user_name=?",(user_name,))
        try:
            if not user_name_searched:
                raise UserDoesNotExistException(f"Please create any user first")
            else:
                pass
        except UserDoesNotExistException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        user_does_not_exist=0
        try:
            for i in user_name_searched:
                    if i["user_name"]==user_name or i["id"]==user_id:
                        if i["password"]==password:
                            if i["is_administrator"]:
                                print(f"Successfully logged in administrator {user_name}")
                                print(f"Successfully logged in administrator {user_name}",file=self.log_file)
                                self.log_file.close()
                            else:
                                print(f"Successfully logged in normal user {user_name}")
                                print(f"Successfully logged in normal user {user_name}",file=self.log_file)
                                self.log_file.close()
                        else:
                            raise PasswordDoesNotMatchException(f"Password {password} does not match")
                    else:
                        user_does_not_exist+=1
            if user_does_not_exist==len(user_name_searched):
                raise UserDoesNotExistException(f"User {user_name} does not exists")
        except UserDoesNotExistException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        except PasswordDoesNotMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        return True
    def lour(self,user_name:str|None, password:str,user_id:None|int) -> bool:
        return self.__login_user(user_name,password,user_id)