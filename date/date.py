import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import time
import cv2
import torch
from torch.autograd import Variable
import lib.utils.utils as utils
import lib.models.crnn as crnn
import lib.config.alphabets as alphabets
import yaml
from easydict import EasyDict as edict
import argparse
import glob
from configdate import get_config

class DATE(object):
    def __init__(self):
        self.config=get_config()
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.model = crnn.get_crnn(self.config).to(self.device)
        checkpoint = torch.load(self.config.checkpoint)
        if 'state_dict' in checkpoint.keys():
            self.model.load_state_dict(checkpoint['state_dict'])
        else:
            self.model.load_state_dict(checkpoint)
        self.model.eval()
    
    def recognize(self,img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        converter = utils.strLabelConverter(self.config.DATASET.ALPHABETS)
        h, w = img.shape
        # fisrt step: resize the height and width of image to (32, x)
        img = cv2.resize(img, (0, 0), fx=self.config.MODEL.IMAGE_SIZE.H / h, fy=self.config.MODEL.IMAGE_SIZE.H / h, interpolation=cv2.INTER_CUBIC)

        # second step: keep the ratio of image's text same with training
        h, w = img.shape
        inp_h = self.config.MODEL.IMAGE_SIZE.H
        inp_w = self.config.MODEL.IMAGE_SIZE.W
        w_cur = int(img.shape[1] / (self.config.MODEL.IMAGE_SIZE.OW / self.config.MODEL.IMAGE_SIZE.W))
        img = cv2.resize(img, (0,0), fx=inp_w / w, fy=inp_h / h, interpolation=cv2.INTER_CUBIC)
        img = np.reshape(img, (inp_h, inp_w, 1))

        # normalize
        img = img.astype(np.float32)
        img = (img / 255. - self.config.DATASET.MEAN) / self.config.DATASET.STD
        img = img.transpose([2, 0, 1])
        img = torch.from_numpy(img)

        img = img.to(self.device)
        img = img.view(1, *img.size())
        preds = self.model(img)

        _, preds = preds.max(2)
        preds = preds.transpose(1, 0).contiguous().view(-1)
    
        preds_size = Variable(torch.IntTensor([preds.size(0)]))
        sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
        # print('results: {0}'.format(sim_pred))
        return sim_pred                                             
if __name__=="__main__":
    X=ID()
    img=cv2.imread("id/15.jpg")
    cv2.imshow("image", img)
    print(X.recognize(img))
    cv2.waitKey(0)
