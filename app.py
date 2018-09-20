from flask import Flask, redirect, url_for, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time


cred = credentials.Certificate('./igem-texem-firebase-adminsdk-0yf5a-da8a519359.json')
#default_app = firebase_admin.initialize_app(cred)
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://igem-texem.firebaseio.com"
})

app = Flask(__name__)
 
@app.route('/')
def index():
	return "Hello World!"

@app.route('/sendData',methods=['POST'])
def sendData():
    
    data = request.get_json()['data']
    token = request.get_json()['token']
    time.strftime("%c")
    ref = db.reference(token+'/color/'+time.strftime("%Y/%b/%d/%H:%M:%S"))
    ref.set({
    	'data':data
    	})
    return "true"

@app.route('/token',methods=['POST'])
def token():
    token = request.get_json()['token']
    if len(token)<=5:
        x=str(time.time())
    else:
        x='true'
        
    return x

if __name__ == "__name__":
	app.run()