from logging import exception
import psycopg2
from entity.monitor import Monitor 
from datetime import date, datetime
# import Json
class MonitorService:
    connection = None
    def __init__(self):
        print("Khoi tao ")
        self.connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="postgres")
    def get_monitors():
        pass
    def create_monitor(self, monitor):
        cursor = self.connection.cursor()
        try: 
            print("what's on the earth .... ")
            postgres_insert_query = """ INSERT INTO "monitor" ("username", "password") VALUES (%s,%s)"""
            record_to_insert = (monitor['username'], monitor['password'])
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
        except (Exception, psycopg2.Error)  as error :
            print("Failed to insert record into mobile table", error)
        finally : 
            # closeing database connection 
            print("sacsdcsac", cursor)
            if  self.connection : 
                cursor.close()
                self.connection.close()
                print("Database connection os close successful") 
    def get_monitors(self):
        try: 
            cursor = self.connection.cursor()
            print("what's on the earth .... ")
            postgres_insert_query = """ SELECT * FROM "monitor" """
            cursor.execute(postgres_insert_query)
            self.connection.commit()
            data = cursor.fetchall()
            print(data, "get list monitors successfully")
            return data
        except (Exception, psycopg2.Error)  as error :
            print("Failed to insert record into mobile table", error)
        finally : 
            # closeing database connection 
            if self.connection : 
                cursor.close()
                self.connection.close()
                print("Database connection os close successful") 
    def findUserByEmail(self, email):
        try:
            # find user by email address in monitor table 
            cursor = self.connection.cursor()
            postgres_select_query_monitor = """ SELECT * FROM "monitor" WHERE email = %s"""
            print("asca")
            cursor.execute(postgres_select_query_monitor,(email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None and len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))
                return data[0]
            
            # find user by email address in employee table
            print("find user by email address in employee table") 
            postgres_select_query_employee = """ SELECT * FROM "employee" WHERE email = %s """
            cursor.execute(postgres_select_query_employee, (email,))
            self.connection.commit()
            data = cursor.fetchall()
            if data != None or len(data) > 0 : 
                print("User nhan duoc khi truy van voi email la : ", data)
                print(type(data))
                return data[0]
            print("done find user by email address in employee table")
            return "error"


            # find user by email address in table employee
        except (Exception, psycopg2.Error)  as error :
            print("Failed to query table", error)
        finally : 
            pass
            # closeing database connection 
            # if self.connection : 
            #     cursor.close()
            #     self.connection.close()
            #     print("Database connection os close successful") 
    def checkLogin(self, email, password, ):
        data = self.findUserByEmail(email)
        print("Loai cua data tra ve la : ", type(data)) 
        if data != None and len(data) > 0:
            roleid = str(data[-1])
            print(data[2] + "--------------" + password[1:])
            return data[2] == password[1:], roleid
        return None, None
    def addWorkLog(self, data):
        try:
            sqlQuery = """INSERT INTO "worklog"("time", "employeeid", "monitorid", "userimage") VALUES(%s, %s, %s, %s)"""
            cursor = self.connection.cursor()
            print("flag1")
            print(data)
            cursor.execute(sqlQuery, tuple(data.values()))
            print("flag2")
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into work log table", error)
        finally : 
            print("close success")
            self.connection.close()
    def check_spoof(self, imageBase64):
        # check base on machine learning model 
        # 1. Is this fake or real ?
        # 2. Who is this ?
        isFake = False
        isWho = None 
        return isFake, isWho
    def check_and_add_work_log(self, auth, imageBase64):
        email = auth['user']
        isFake, who = self.check_spoof(imageBase64)
        # neu la fake face 
        # if worklog for to day does't not exist, create 1 more record 
        isFake = False
        who = "tran xuan luong"
        if isFake:
            return "face is fake"
        elif who is None:
            return "image doesn't match any person in the system"

        success = 1
        if isFake: success = 0
        print("run to here")
        try:
            queryGetId = """ select id from employee where email = %s """
            cursor = self.connection.cursor()
            cursor.execute(queryGetId, (email,))
            self.connection.commit()
            idUser = cursor.fetchall()
            print("after get user id ")
            # create new worklog
            insertLogQuery = """insert into worklog(employeeid, userimage, daywork, logtime, success) values (%s, %s, %s, %s, %s ) """
            print("oh shit")
            values = (idUser[0],imageBase64, date.today(),datetime.now(), success,)
            print(values)
            cursor.execute(insertLogQuery, values)
            self.connection.commit()
            print(idUser)
        except (Exception, psycopg2.Error) as error :
            print("Failed to insert record into work log table", error)
        finally : 
            print("close success")
            self.connection.close()
    def addFace(data):
        pass
        # if worklog for today exist, just add 5 minutes to time column
        # select workLog for today of user with email auth['user]

