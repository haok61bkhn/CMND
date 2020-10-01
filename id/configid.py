from easydict import EasyDict as edict
import torch
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
import lib.config.alphabets as alphabets
def get_config():
    cur_dir=os.path.dirname(os.path.realpath(__file__))
    cfg_file=os.path.join(cur_dir,"lib/config/OWN_config.yaml")
    with open(cfg_file, 'r') as f:
        conf = yaml.load(f)
    conf = edict(conf)
    conf.cur_dir=cur_dir
    conf.checkpoint=os.path.join(conf.cur_dir,"model","id.pth")
    conf.DATASET.ALPHABETS = alphabets.alphabet
    conf.MODEL.NUM_CLASSES = len(conf.DATASET.ALPHABETS)
    return conf