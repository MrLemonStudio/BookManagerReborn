import sqlite3
import datetime
import os
class RootService:
    def __init__(self,file_location):
        self.run_time=datetime.datetime.today().strftime("%Y%m%d%H%M%S")
        self.log_location=f"../logs/{self.run_time}.log"
        self.log_file=open(self.log_location,"w",errors="ignore")
        self.file_location=file_location

class ReadTableService(RootService):
    def __read_table(self,table_name,sql_cmd="select * from ") ->list|bool:
        try:
            self.connection = sqlite3.connect(self.file_location)
        except FileNotFoundError as e:
            print(f"""======
        LOGLOG
        ======
        {self.run_time}""", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"CANNOT FIND TABLE FILE NAMED {self.file_location}!\n{e}", file=self.log_file)
            return False
        except ValueError as e:
            print(f"""======
                    LOGLOG
                    ======
                    {self.run_time}""", file=self.log_file)
            print("ERROR!", file=self.log_file)
            print(f"FILE LOCATION MUST BE A STRING! {self.file_location}!\n{e}", file=self.log_file)
            return False
        self.sql_cmd=f"{sql_cmd}{table_name}"
        self.cursor=self.connection.cursor()
        self.cursor.execute(self.sql_cmd)
        self.result=self.cursor.fetchall()
        print(f"""======
LOGLOG
======
{self.run_time}""", file=self.log_file)
        print("OK!",file=self.log_file)
        print(f"RESULT IS {self.result}",file=self.log_file)
        return self.result
