
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tool.utils import *
from tool.darknet2pytorch import Darknet
from config import get_config
import cv2
import glob


class Detector_fields:
    def __init__(self):
        opt=get_config()
        self.model=Darknet(opt.cfg)
        self.model.load_weights(opt.weights)
        self.model.to(opt.device)
        self.class_names=load_class_names(opt.names)
        self.size=(self.model.width,self.model.height)
        self.num_classes=6
        print(self.class_names)
    
    def detect(self,img,thresh=0.6):
        res={}
        resimg={}
        for x in self.class_names:
            resimg[x]=[]
            res[x]=[]
        im0=img.copy()
        size=(img.shape[0],img.shape[1])
        img = cv2.resize(img, self.size)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        boxes=[]
        
        type_obj=[]
        score=[]
        boxes = do_detect(self.model, img, thresh, self.num_classes, thresh, 1)
        res_box=[]
        ims=[]
        classes=[]
        for box in boxes:
          #if(int(box[6])==2  or int(box[6])==3  or int(box[6])==5  or int(box[6])==7  ): # 2 3 5 7  is vehicle 
            if(self.class_names[int(box[6])]=="date"):
                margin =0
            if(self.class_names[int(box[6])]=="id"):
                margin = 3
                #print("id")
            else:
                margin=0
            x1 = max(int((box[0] - box[2] / 2.0) * size[1])-margin,0)
            y1 = max(int((box[1] - box[3] / 2.0) * size[0])-margin-1,0)
            x2 = min(int((box[0] + box[2] / 2.0) * size[1]+margin),im0.shape[1])
            y2 = min(int((box[1] + box[3] / 2.0) * size[0]+margin),im0.shape[0])
            imm=im0[y1:y2,x1:x2]

            # if(imm.shape[0]>20 and imm.shape[1]>20):
            # res_box.append([x1,y1,x2,y2])
            # ims.append(imm)
            # classes.append(self.class_names[int(box[6])])
            res[self.class_names[int(box[6])]].append([x1,y1,x2,y2])
            resimg[self.class_names[int(box[6])]].append(imm)
        return res,resimg

    
if __name__ == "__main__":
    X=Detector()
    d=0
    d1=0
    for path in tqdm.tqdm(glob.glob("image/*")):
     try:
        img=cv2.imread(path)
 
        boxes,ims,classes=X.detect(img,0.3)
     
        for box in boxes:
            img=cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,255,0),1,1)
        for im,cl in zip(ims,classes):
            cv2.imwrite("output/"+cl+"/"+str(d)+".jpg",im)
            d+=1
        cv2.imwrite("output/image/"+str(d1)+".jpg",img)
        d1+=1
     except Exception as e:
         print(e)

