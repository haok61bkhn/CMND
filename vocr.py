import matplotlib.pyplot as plt
from PIL import Image
import cv2
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import glob
import time

class VOCR():
    def __init__(self):
        config = Cfg.load_config_from_name('vgg_transformer')
        config['weights'] = './model/transformerocr.pth'
        # config['weights'] = 'https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA'
        # config['device'] = ''
        config['device']='cuda:0'
        config['predictor']['beamsearch']=False
        self.detector = Predictor(config)

    def recognize(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        return self.detector.predict(img)

if __name__ == "__main__":

    X=OCR()
    for path in glob.glob("images/*"):
        img=cv2.imread(path)
       
        cv2.imshow("image",img)
        t1=time.time()
        print(X.recognize(img))
        print("time",time.time()-t1)
        cv2.waitKey(0)


