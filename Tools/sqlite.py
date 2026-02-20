import sqlite3
import datetime
import os
import Tools.custom_errors
class RootService:
    def __init__(self,file_location):
        self.run_time=datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.log_dir_path="../../logs"
        if not os.path.exists(self.log_dir_path):
            os.mkdir(self.log_dir_path)
        self.log_location=f"{self.log_dir_path}/{self.run_time}.log"
        self.log_file=open(self.log_location,"w",errors="ignore")
        self.file_location=file_location

class ReadTableService(RootService):
    def __read_table(self,table_name:str,sql_cmd:str) ->list|bool:
        try:
            try:
                float(self.file_location)
            except ValueError:
                pass
            else:
                raise ValueError("ERR!ERR!ERR!Value!")
            if not os.path.exists(self.file_location):
                raise FileNotFoundError("ERR!ERR!ERR!F.N.F.!")
            self.connection = sqlite3.connect(self.file_location)
        except FileNotFoundError as e:
            print(f"======\nLOGLOG\n======\n{self.run_time}")
            print("ERROR!")
            print(f"CANNOT FIND TABLE FILE NAMED {self.file_location}!\n{e}")
            print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"CANNOT FIND TABLE FILE NAMED {self.file_location}!\n{e}", file=self.log_file)
            self.log_file.close()
            return False
        except ValueError as e:
            print(f"======\nLOGLOG\n======\n{self.run_time}")
            print("ERROR!")
            print(f"FILE LOCATION MUST BE A STRING! NOT {self.file_location}!\n{e}")
            print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"FILE LOCATION MUST BE A STRING! NOT {self.file_location}!\n{e}", file=self.log_file)
            self.log_file.close()
            return False
        self.sql_cmd=f"select {sql_cmd} from {table_name}"
        self.cursor=self.connection.cursor()
        self.cursor.execute(self.sql_cmd)
        self.result=self.cursor.fetchall()
        print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
        print("OK!",file=self.log_file)
        print(f"RESULT IS {self.result}",file=self.log_file)
        self.log_file.close()
        return self.result
    def reta(self,table_name,sql_cmd="*"):
         return self.__read_table(table_name,sql_cmd)

class CreateTableService(RootService):
    def __create_table(self,table_name:str,column_names:dict)->bool:
        try:
            try:
                float(self.file_location)
            except ValueError:
                pass
            else:
                raise ValueError("ERR!ERR!ERR!Value!")
            if os.path.exists(self.file_location):
                raise FileExistsError("ERR!ERR!ERR!F.E.!")
            else:
                pass
        except FileExistsError as e:
            print(f"======\nLOGLOG\n======\n{self.run_time}")
            print("ERROR!")
            print(f"FOUND TABLE FILE NAMED {self.file_location}!\n{e}")
            print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"FOUND TABLE FILE NAMED {self.file_location}!\n{e}", file=self.log_file)
            self.log_file.close()
            return False
        except ValueError as e:
            print(f"======\nLOGLOG\n======\n{self.run_time}")
            print("ERROR!")
            print(f"FILE LOCATION MUST BE A STRING! NOT {self.file_location}!\n{e}")
            print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"FILE LOCATION MUST BE A STRING! NOT {self.file_location}!\n{e}", file=self.log_file)
            self.log_file.close()
            return False
        except Exception as e:
            print(f"======\nLOGLOG\n======\n{self.run_time}")
            print(f"ERROR!{e}")
            print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
            print(f"ERROR!{e}", file=self.log_file)
            self.log_file.close()
            return False
        self.connection = sqlite3.connect(self.file_location)
        cursor = self.connection.cursor()
        list_configs = []
        data_kinds=[]
        for i in column_names.values():
            not_null=False
            primary_key=False
            auto_increment=False
            unique=False
            if i[0] :
                not_null=True
            if i[1]:
                primary_key = True
            if i[2]:
                auto_increment = True
            if i[3]:
                unique = True
            data_kind=i[4]
            list_config=[not_null,primary_key,auto_increment,unique]
            list_configs.append(list_config)
            data_kinds.append(data_kind)
        if not len(list_configs)==len(column_names.values()):
            try:
                raise Tools.custom_errors.RUSureThatThisIsPossible("What did you do to my program!?")
            except Tools.custom_errors.RUSureThatThisIsPossible as e:
                print(e)
                print(e,file=self.log_file)
                return  False
        else:
            keys_of_dict=[]
            values_of_dict_inner=[]
            values_of_dict_outer=[]
            creation_code_outer=''
            creation_code_inner=''
            for i in column_names.keys():
                keys_of_dict.append(i)
            for b in list_configs:
                for c in b:
                    if c:
                        if c==b[0]:
                            values_of_dict_inner.append("NOT NULL")
                        if c==b[1]:
                            values_of_dict_inner.append("PRIMARY KEY")
                        if c==b[2]:
                            values_of_dict_outer.append("AUTOINCREMENT")
                        if c==b[3]:
                            values_of_dict_outer.append("UNIQUE")
                values_of_dict_outer.append(values_of_dict_inner)
            values_of_dict=""
            for d in values_of_dict_outer:
                for f in d:
                    values_of_dict+=f+" "
            for g in keys_of_dict:
                for h in data_kinds:
                    creation_code_inner+=f'"{g}" {h} {values_of_dict}'
                    creation_code_outer+=creation_code_inner+","
            if creation_code_outer[-1]==',':
                creation_code_outer=creation_code_outer[:-1]
            self.sql_cmd=f"create table {table_name} ({creation_code_outer})"
            try:
                cursor.execute(self.sql_cmd)
            except sqlite3.OperationalError as e:
                print(f"======\nLOGLOG\n======\n{self.run_time}")
                print("ERROR!")
                print(e)
                print(f"======\nLOGLOG\n======\n{self.run_time}",file=self.log_file)
                print("ERROR!", file=self.log_file)
                print(e,file=self.log_file)
                return False
            except Exception as e:
                print(f"======\nLOGLOG\n======\n{self.run_time}")
                print(f"ERROR!")
                print(e)
                print(f"======\nLOGLOG\n======\n{self.run_time}", file=self.log_file)
                print("ERROR!", file=self.log_file)
                print(e,file=self.log_file)
                return False
            else:
                self.connection.commit()
                return True
    def ceta(self,table_name:str,column_names:dict)->bool:
         return self.__create_table(table_name,column_names)