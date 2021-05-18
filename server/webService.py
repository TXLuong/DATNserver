import os.path
import cv2
from service import MonitorService
import os
from flask import Flask, request, render_template, send_from_directory, jsonify, make_response, Response
import jwt
import datetime
from flask_cors import CORS
import base64
from service import MonitorService 
import json
app = Flask(__name__)
CORS(app, resources=r'/login')
CORS(app, resources=r'/monitor/current')
CORS(app, resources=r'/logout')
CORS(app, resources=r'/turnIn')
# CORS(app, resources=r'/getCurent')
app.config['SECRET_KEY'] ='thisisthesecretkey'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

service = MonitorService()

service.checkLogin("acds","acscscd")

@app.route("/monitor/create", methods=["POST"])
def create_monitor():
    data = request.get_json()
    print("----------------",type(data))
    monitor = data 
    service.create_monitor(monitor)
    return data

@app.route("/monitors", methods=["GET"])
def getlist():
    data = service.get_monitors()
    print(type(data))
    return jsonify(data)

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    execution_path = target
    print(execution_path)
    image = Predict(os.path.join(execution_path, filename))
    print(image.shape)
    print('predicted')
    out_image = cv2.imwrite(os.path.join(execution_path,  "flask"+filename), image)
    print('wrote out the image')
    print('flask'+filename)
    return render_template("Flask_FacialRecognition_WebService.html", image_name="flask"+filename)


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)


@app.route('/login', methods = ['POST'])
def login():
    # de username va password trong header
    headers = request.headers.get("Authorization")
    transform = base64.b64decode(headers)
    res = transform.decode("UTF-8")
    arr = res.split(":")
    auth = {"email" : arr[0], "password" : arr[1]}
    check, userInfo = service.checkLogin(auth['email'], auth['password'])
    if auth and check :
        # verify who user is 
        token = jwt.encode({'user': auth['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60*12)}, app.config['SECRET_KEY'])
        return jsonify({"token": token.decode('UTF-8'),"userInfo" : userInfo})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required "'})


@app.route("/workLog/create", methods=["POST"])
def workLog():
    data = request.json
    # data = jsonify(data)
    print("recieved data ", data['time'])
    print(type(data))
    service.addWorkLog(data)
    return data

@app.route("/create/employee", methods=["POST"])
def createEmployee():
    # create employee at Posgres
    res = request.json
    
    # create employee at mongoDb
@app.route("/monitor/current", methods=["GET"])
def getCurrent():
    return {"username" : "luong","password" : "luong", "firstname" : "luong","email" : "lu@gmail.com"}

@app.route("/logout", methods=["POST"])
def logout():
    # set refresh token to null
    return "ok"

@app.route("/turnIn", methods=["POST"])
def turnIn():
    token = request.headers.get("X-Auth-Token") 
    auth = jwt.decode(token,app.config['SECRET_KEY'])
    imageBase64 = request.json
    print(auth)
    print(type(auth))
    service.check_and_add_work_log(auth, imageBase64)
    return "ok"
    # service.turnIn()
if __name__ == "__main__" :
    app.run()