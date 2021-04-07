import os.path
import cv2
from service import MonitorService
import os
from flask import Flask, request, render_template, send_from_directory, jsonify, make_response
import jwt
import datetime
from flask_cors import CORS
import base64
from service import MonitorService 
app = Flask(__name__)
CORS(app, resources=r'/login')
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
    # auth = request.get_json()
    # return "logined"
    headers = request.headers.get("Authorization")
    transform = base64.b64decode(headers)
    res = transform.decode("UTF-8")
    print("res ---------------- ", res)
    arr = res.split(":")
    auth = {"email" : arr[0], "password" : arr[1]}

    if auth and service.checkLogin(auth['email'], auth['password']) :
        # verify who user is 
        token = jwt.encode({'user': auth['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
        print("token ------------------------- ", token)
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm = "Login required "'})
if __name__ == "__main__" :
    app.run()