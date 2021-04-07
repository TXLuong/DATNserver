import psycopg2
from entity.monitor import Monitor 
# import Json
class MonitorService:
    connection = None
    def __init__(self):
        print("Khoi tao chua the !!!!!!!!!!!")
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
            # find user by email address
            cursor = self.connection.cursor()
            postgres_select_query = """ SELECT * FROM "monitor" WHERE email = %s"""
            print("asca")
            cursor.execute(postgres_select_query,(email,))
            self.connection.commit()
            data = cursor.fetchone()
            print(type(data))
            print(data)
            return tuple(data)
    
        except (Exception, psycopg2.Error)  as error :
            print("Failed to insert record into mobile table", error)
        finally : 
            pass
            # closeing database connection 
            # if self.connection : 
            #     cursor.close()
            #     self.connection.close()
            #     print("Database connection os close successful") 
    def checkLogin(self, email, password):
        print("troll very troll !")
        # check user and password
        data = self.findUserByEmail(email)
        
        print(type(data))
        if data is None : 
            print("true")
        return True
        # data = tuple(data)
        # print(data[1])
        # result = Monitor(tuple(data)) 
        # result = None
        # print(result.email)
        # if result and result.password == password:
        #     print("tlammmmmmmmmmmmmmmmmmmmmmmmmmmm")
        #     return True
        # else: return False

# class EmployeeService:
#     pass

# class WorkLogService:
#     pass

# ngu = MonitorService()
# ngu.checkLogin("cc","as")