
from Detect_cmnd.model_center import CENTER_MODEL
import glob
import cv2
import os
from Detect_fields.detect import Detector_fields
from ocr import OCR
import time
class CMND(object):
    def __init__(self):
        self.Detect_cmnd=CENTER_MODEL(weight_path="Detect_cmnd/weights/model_cmnd_best.pth")
        self.Detect_fields=Detector_fields()
        self.ocr=OCR()
        self.fields=['id','name','date','ad1','ad2']

    def predict(self,img):
        restext={}
        t1=time.time()
        font = cv2.FONT_HERSHEY_SIMPLEX 
        img_aligned= self.Detect_cmnd.detect(img)
        print("centernet ",time.time()-t1)
        t1=time.time()
        if(img_aligned is not None):
            img_aligned=cv2.resize(img_aligned,(800,650))
            res,resimg=self.Detect_fields.detect(img_aligned,0.3)
            print("yolo ",time.time()-t1)
            t1=time.time()
            for x in self.fields:
                restext[x]=self.ocr.predict(resimg[x],res[x],x)
                if(restext[x] is None ): restext[x]=""
            print("ocr ",time.time()-t1)
            #     if(cl=="id"):
            #         text=(self.id.recognize(im))
            #     # if(cl=="name"):
            #     else:
            #         text=self.str.recognize(im)
            #     img_aligned=cv2.putText(img_aligned,text,(box[0],box[1]),font,1,(255,0,0),1,cv2.LINE_AA)
                #for box in res[x]:
                 #print("a")  
                 #img_aligned=cv2.rectangle(img_aligned,(box[0],box[1]),(box[2],box[3]),(255,0,0),2,1)
        else : 
                img_aligned = cv2.resize(img,(750,600))
                res,resimg=self.Detect_fields.detect(img_aligned,0.3)
                for x in self.fields:
                 restext[x]=self.ocr.predict(resimg[x],res[x],x)
                 #for box in res[x]:  
                  #img_aligned=cv2.rectangle(img_aligned,(box[0],box[1]),(box[2],box[3]),(255,0,0),2,1)
        restext['name']=restext['name'].upper()
        return img_aligned,restext


if __name__=="__main__":
    X=CMND()
    img=cv2.imread("image/331.jpg")
    cv2.imshow("image",X.prepare(img))
    cv2.waitKey(0)
