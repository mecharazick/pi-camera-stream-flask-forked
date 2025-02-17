#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from flask_cors import CORS
# from camera import VideoCamera
from motor import Motor
import threading
import time
import os

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
CORS(app)

def sendCommandToMotor(command):
    mot = Motor()
    mot.issueCommand(command)
    return


@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

@app.route('/command', methods=['POST'])
def command():
    if request.method == 'POST':
        command = request.get_json()['command']
        threading.Thread(target=sendCommandToMotor, args=[command])
    return '<h1>Comando Enviado</h1>'

def gen(camera):
    lastFrameSentTime = time.time()
    #get camera frame
    while True:
        if(time.time() < lastFrameSentTime + 2.0):
            continue
        frame = camera.get_frame()
        lastFrameSentTime = time.time()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)