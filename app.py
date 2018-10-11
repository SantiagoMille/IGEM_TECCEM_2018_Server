from flask import Flask, redirect, url_for, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import re

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
        numbers= re.findall(r"[-+]?\d*\.\d+|\d+", data)
        print(numbers)
        token = request.get_json()['token']
        time.strftime("%c")
        url = 'data/'+token+'/'+time.strftime("%Y/%b/%d/%H:%M:%S")
        url = url.replace(".", "")
        ref = db.reference(url)
        ref.set({
        	'R':numbers[2],
            'G':numbers[3],
            'B':numbers[4],
            'T':numbers[0],
            'C':numbers[1]
        	})
        return "true"
    except ValueError:
        print(":(((")
        return "false"

@app.route('/token',methods=['POST'])
def token():
    token='';
    token = request.get_json()['token']
    
    try:
        int(token)

        if len(token)<=5:
            x=str(time.time())
        else:
            x=token
        return x
            
    except ValueError:
        return "false"

    

if __name__ == "__name__":
	app.run()