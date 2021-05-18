import json
import numpy as np
import datetime 
from datetime import datetime
from itertools import repeat
import pymongo
import uuid
from bson import json_util, ObjectId
import json

class Connector:
    def __init__(self,name):
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient[name]
        self.col_user = self.mydb["users"]

    def get_all_employee(self, idadmin):
        users = [doc for doc in self.col_user.find()]
        return users

    def get_ids(self, idadmin) :
        ids = [doc['name'] for doc in self.col_user.find({"idadmin" : idadmin})]
        return ids

    def add_user(self, name, features, features_mask):
        try : 
            mydict = { "name": name, "features" : features, "features_mask" : features_mask}
            return self.col_user.insert_one(mydict)
        except:
            return None
        
    def get_users(self):
        names = []
        myquery = {}
        features= np.array([]).reshape(0, 512)
        features_mask= np.array([]).reshape(0, 512)
        users = self.col_user.find(myquery)
        for user in users:
            t = np.array(user["features"]).reshape(-1, 512).shape[0]
            name = [x for x in repeat(user["name"], t)]
            names.extend(name)
            features = np.concatenate((features, np.array(user["features"]).reshape(-1, 512)))
            features_mask = np.concatenate((features, np.array(user["features_mask"]).reshape(-1, 512)))

        return names, features, features_mask
    

# X=Connector("Face")
# # X.add_attend("Hảo")
# # X.get_user()
# # # X.add_user("hao","1234")
# print(X.subtime("17:25:00",X.get_attend_name("Hảo","13-08-2020")))