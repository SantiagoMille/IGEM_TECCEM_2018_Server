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
    hola = request.get_json()['data']
    time.strftime("%c")
    ref = db.reference('color/'+time.strftime("%b-%d-%Y-%H:%M:%S"))
    ref.set({
    	'data':hola
    	})
    return "true"

if __name__ == "__name__":
	app.run()