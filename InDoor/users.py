from Tools.custom_errors import *
from Tools.sqlite_new import SQLiteDatabaseManager
import datetime
import os

class UserActionManager:
    def __init__(self,db_path:str,table_name:str,log_dir_path:str):
        run_time = datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.log_dir_path = log_dir_path
        if not os.path.exists(self.log_dir_path):
            os.mkdir(self.log_dir_path)
        self.log_location = f"{self.log_dir_path}/{run_time}.log"
        self.db_path = db_path
        self.table_name = table_name
        self.sqlite=SQLiteDatabaseManager(self.db_path)
        self.log_file=open(self.log_location,"w",encoding="utf-8",errors="ignore")

    def __create_user(self, user_name:str, password:str,is_administrator:bool=False)->bool|tuple:
        try:
            if not password:
                raise PasswordDoesNotMatchException("Please enter password")
            else:
                pass
        except PasswordDoesNotMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        table_exist=self.sqlite.table_exists(self.table_name)
        if not table_exist:
            self.sqlite.create_table(self.table_name,{"user_name":"text unique not null","password":"text not null","id":"integer primary key not null","is_administrator":"boolean not null default false"})
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
            user_id=users_data_now[0]["id"]+1
        except IndexError:
            user_id=1
        try:
            self.sqlite.execute_sql(f"insert into {self.table_name}(user_name,password,id,is_administrator) values(?,?,?,?)",(user_name,password,user_id,is_administrator))
        except Exception as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        if is_administrator:
            return True,True
        return True,False
    def crur(self,user_name:str, password:str,is_administrator:bool=False)->bool:
        return self.__create_user(user_name,password,is_administrator)

    def __login_user(self, user_name:str|None, password:str, user_id: None | int)->bool|tuple:
        try:
            if not(user_name or user_id):
                raise UserNameDoesNotMatchException("Please enter user_name or user_id")
            else:
                pass
        except UserNameDoesNotMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        user_name_searched=self.sqlite.query(f"select user_name,password,id,is_administrator from {self.table_name} where {"user_name" if user_name else user_id}=?",((user_name,)if user_name else (user_id,)))
        try:
            if not user_name_searched:
                raise UserDoesNotExistException("Please create any user first")
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
                                print(f"Successfully logged in administrator {user_name if user_name else f"ID = {user_id}"}")
                                print(f"Successfully logged in administrator {user_name if user_name else f"ID = {user_id}"}",file=self.log_file)
                                self.log_file.close()
                                return True,True
                            else:
                                print(f"Successfully logged in normal user {user_name if user_name else f"ID = {user_id}"}")
                                print(f"Successfully logged in normal user {user_name if user_name else f"ID = {user_id}"}",file=self.log_file)
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
        return True,False
    def lour(self,user_name:str|None=None, password:str="",user_id:None|int=None) -> bool:
        return self.__login_user(user_name,password,user_id)

    def __change_user_name(self,old_user_name:str,new_user_name:str,password:str)->bool:
        try:
            if old_user_name==new_user_name:
                raise UserNameMatchException("The old user name and the new one can't be the same")
            else:
                pass
        except UserNameMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        user_name_list=self.sqlite.query(f"select user_name,id,password from {self.table_name}")
        user_does_not_exist=0
        try:
            for i in user_name_list:
                if i["user_name"]==old_user_name:
                    if i["password"]==password:
                        self.sqlite.execute_sql(f"update {self.table_name} set user_name=? where id=?",(new_user_name,i["id"]))
                        break
                    else:
                        raise PasswordDoesNotMatchException(f"Password {password} does not match")
                else:
                    user_does_not_exist+=1
            if user_does_not_exist==len(user_name_list):
                raise UserDoesNotExistException(f"User {old_user_name} does not exists")
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
        except Exception as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        return True
    def curn(self,old_user_name:str,new_user_name:str,password:str)->bool:
        return self.__change_user_name(old_user_name,new_user_name,password)

    def __change_user_password(self,user_name:str,old_password:str,new_password:str)->bool:
        try:
            if old_password==new_password:
                raise PasswordMatchException("The old password and the new one can't be the same")
            else:
                pass
        except PasswordMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        password_list=self.sqlite.query(f"select user_name,password from {self.table_name}")
        user_does_not_exist=0
        try:
            for i in password_list:
                if i["user_name"]==user_name:
                    if i["password"]==old_password:
                        self.sqlite.execute_sql(f"update {self.table_name} set password=? where user_name=?",(new_password,user_name))
                        break
                    else:
                        raise PasswordDoesNotMatchException(f"Password {old_password} does not match")
                else:
                    user_does_not_exist+=1
            if user_does_not_exist==len(password_list):
                raise UserDoesNotExistException(f"User {user_name} does not exists")
        except PasswordDoesNotMatchException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        except UserDoesNotExistException as e:
            print(e)
            print(e,file=self.log_file)
            self.log_file.close()
            return False
        return True
    def curp(self,user_name:str,old_password:str,new_password:str)->bool:
        return self.__change_user_password(user_name,old_password,new_password)