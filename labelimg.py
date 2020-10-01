import matplotlib.pyplot as plt
from PIL import Image
import cv2
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import glob
import time
import os 
import tqdm
class OCR():
    def __init__(self):
        config = Cfg.load_config_from_name('vgg_transformer')
        config['weights'] = './model/transformerocr.pth'
        # config['weights'] = 'https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA'
        # config['device'] = ''
        config['device']='cuda'
        config['predictor']['beamsearch']=False
        self.detector = Predictor(config)

    def recognize(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return self.detector.predict(img)

if __name__ == "__main__":

    X=OCR()
    dataroot="output"
    # print(os.listdir(dataroot))
    ldir= os.listdir(dataroot)
    for lb in ldir:
        print("begin ",lb)
        lims=glob.glob(os.path.join(dataroot,lb,"*.jpg"))

        for f in tqdm.tqdm(lims):
             try:
                img=cv2.imread(f)
                txt=open(f[:-3]+"txt","w+")
                txt.writelines(X.recognize(img))
                txt.close()
             except:
                print(f)



