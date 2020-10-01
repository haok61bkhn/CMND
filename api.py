from flask import Flask, Response,jsonify,request,render_template,url_for,flash,redirect
import base64
import pickle
import json
import numpy as np
import cv2
import time
import uuid
import shutil
# import urllibre
import os
from io import BytesIO
from main import CMND
#from vnaddress import VNAddressStandardizer
import time
#address = VNAddressStandardizer(raw_address = "Tân Đức Hàm Tần Bình Thuận".lower(), comma_handle = False,detail=True)

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
detetor=CMND()
# declare var 


def save_image(image):
    session_id = str(uuid.uuid1())
    dirpath = os.path.join('static/data', session_id)
    os.makedirs(dirpath)
    inpath = os.path.join(dirpath, 'input.jpg')
    cv2.imwrite(inpath, image)
    return inpath

@app.route("/", methods=['GET','POST']) # webapi
def upload_file():
    if request.method == "GET":
      return render_template("index.html")
    if request.method == 'POST': 
        image=request.form["image"]
        if(1):
        #try:
            #________________________process________________________________________
            image=image.split(",")[1]
            image=base64.b64decode(image)
            image= np.frombuffer(image, dtype=np.uint8)
            image = cv2.imdecode(image, flags=1)
            path = save_image(image) # save original image

            #test result is image
            #res_img = image.copy()
            #b64_res_img = convert_tob64(res_img)
            #restext="abc"
            t1=time.time()
            img_aligned,restext=detetor.predict(image)
            print("time detect ",time.time()-t1)
            #b64_res_img=convert_tob64(img_aligned)
            b64_res_img=save_image(img_aligned) 
            result=restext
            #print(VNAddressStandardizer(raw_address = result['ad2'], comma_handle = False,detail=True).execute())
            t1=time.time()
            ad1=result['ad2']
            ad2=result['ad1']
            #ad1=VNAddressStandardizer(raw_address = result['ad2'], comma_handle = False,detail=True).execute()['result']
            #ad2=VNAddressStandardizer(raw_address = result['ad1'], comma_handle = False,detail=True).execute()['result']
            print("time post process ",time.time()-t1)
            return render_template("index.html",orimg=path,resimg=b64_res_img,result=restext,id=result['id'],name=result['date'].upper(),date=result['name'].upper(),ad1=ad1,ad2=ad2)  
        
        #except:
         # print("No image selected")
         # return render_template("index.html")
       
            

def convert_tob64(frame):
     _, im_arr = cv2.imencode('.png', frame)  # im_arr: image in Numpy one-dim array format.
     im_bytes = im_arr.tobytes()
     im_b64 = base64.b64encode(im_bytes)    
     return "data:image/png;base64,"+str(im_b64)[2:-1]

@app.route("/api",methods=['GET','POST'])
def process():
    r = request.json
    #print(r)
    output={}
    data=r['image']
    img=base64.b64decode(data)
    img= np.frombuffer(img, dtype=np.uint8)
    img = cv2.imdecode(img, flags=1)
    #print(img.shape)
    img_aligned,restext=detetor.predict(img)
    return restext

@app.route("/api1",methods=['GET','POST'])
def process2():
   try:
    r = request.json
    #print(r)
    name=r['name']
    img=cv2.imread(name)
    output={}
    img_aligned,restext=detetor.predict(img)
    return restext
   except:
    return {}
if __name__ == "__main__":
    #predict = Process()
    app.run(host="0.0.0.0",port=8668,debug=True,threaded=True)


