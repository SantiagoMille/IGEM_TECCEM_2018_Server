from flask import Flask, redirect, url_for, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
import re
import cv2 as cv
import numpy as np
import time
import json

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
        float(token)
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
        float(token)

        if len(token)<=5:
            x=str(time.time())
        else:
            x=token
        return x
            
    except ValueError:
        return str(time.time())

@app.route('/short',methods=['POST'])
def short():
    try:
        img_request = request.files['file'].read()
        npimg = np.fromstring(img_request, np.uint8)
        img_rgb = cv.imdecode(npimg, cv.IMREAD_UNCHANGED)

        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        template =  cv.imread('cell4.png',0)
        w, h = template.shape[::-1]

        template2 =  cv.imread('cell3.png',0)
        w2, h2 = template2.shape[::-1]

        template3 =  cv.imread('cell2.png',0)
        w3, h3 = template3.shape[::-1]

        template4 =  cv.imread('cell.png',0)
        w4, h4 = template4.shape[::-1]

        template4 =  cv.imread('cell.png',0)
        w4, h4 = template4.shape[::-1]

        template5 =  cv.imread('cell5.png',0)
        w5, h5 = template5.shape[::-1]

        ###############################################################################

        res = cv.matchTemplate(img_gray,template5,cv.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            #cv.rectangle(img2   , pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        img_gray2 = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        #cv.imwrite('res'+'1'+'.png',img_rgb)

        ###############################################################################

        res = cv.matchTemplate(img_gray2,template2,cv.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            #cv.rectangle(img2   , pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        img_gray3 = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        #cv.imwrite('res'+'2'+'.png',img_rgb)

        ###############################################################################

        res = cv.matchTemplate(img_gray3,template3,cv.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            #cv.rectangle(img2   , pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        img_gray4 = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        #cv.imwrite('res'+'3'+'.png',img_rgb)

        ###############################################################################

        res = cv.matchTemplate(img_gray4,template4,cv.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            #cv.rectangle(img2   , pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        img_gray5 = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        #cv.imwrite('res'+'4'+'.png',img_rgb)
        ###############################################################################

        res = cv.matchTemplate(img_gray5,template,cv.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where( res >= threshold)

        for pt in zip(*loc[::-1]):
            #cv.rectangle(img2   , pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        #cv.imwrite('res'+'5'+'.png',img_rgb)

    except Exception as e: 
        print(e)
    
    return img_rgb

@app.route('/large',methods=['POST'])
def large():
    cells=0
    try:
        img_request = request.files['file'].read()
        npimg = np.fromstring(img_request, np.uint8)
        img = cv.imdecode(npimg, cv.IMREAD_UNCHANGED)

        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        blur = cv.GaussianBlur(gray,(7,7),0)
        ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY)
        ret,th_bin_ostu = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        titles = ['BINARY+OTSU']
        images = [th_bin_ostu]
        
        for i in range(len(images)):
            if True:
                
                kernel = np.ones((4,4), np.uint8) 
                kernel2 = np.ones((2,2), np.uint8) 
                   
                img_dilation = cv.erode(images[i], kernel, iterations=1) 
                #img_dilation = cv.dilate(img_erosion, kernel2, iterations=1) 
                
                original,puntos,_ = cv.findContours(img_dilation, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                print(titles[i],":",len(puntos))
                cells = len(puntos)
                for c in puntos:
                    rect = cv.boundingRect(c)
                    #if rect[2] < 100 or rect[3] < 100: continue
                    x,y,w,h = rect
                    cv.rectangle(img_dilation,(x,y),(x+w,y+h),(255,255,0),2)
                    cv.putText(img_dilation,'Detected',(x+w+10,y+h),0,0.3,(255,255,0))

    except Exception as e: 
        print(e)
    
    data = {}
    data['cells'] = cells
    json_data = json.dumps(data)
    return json_data

if __name__ == "__name__":
	app.run()