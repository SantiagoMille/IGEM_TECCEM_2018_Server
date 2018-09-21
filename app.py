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
	return "Hello IGEM!"

@app.route('/sendData',methods=['POST'])
def sendData():
    try:
        data = request.get_json()['data']
        token = request.get_json()['token']
        print("token1: ",token)
        print("data1:",data)
        time.strftime("%c")
        print("token2: ",token)
        ref = db.reference(token+'/color/'+time.strftime("%Y/%b/%d/%H:%M:%S"))
        ref.set({
        	'data':data
        	})
        return "true"
    except ValueError:
        return "false"

@app.route('/token',methods=['POST'])
def token():
    token = request.get_json()['token']
    print(token)
    if len(token)<=5:
        x=str(time.time())
    else:
        x=token
        
    return x

if __name__ == "__name__":
	app.run()