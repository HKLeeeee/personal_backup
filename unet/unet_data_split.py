# images, masks로 구성된 파일
# image(train, valid, test), mask(train, valid,test)로 datasplit
# test set에는 마스크가 필요없는데 이걸로 train valid test 나누면 test set도 마스크를 가짐

import subprocess
from glob import glob
import os, shutil
import argparse
import nibabel as nib
import cv2
from tqdm import tqdm
import random

def split(config):
    train_img = os.path.join(config.image, 'train')
    valid_img = os.path.join(config.image, 'valid')
    test_img = os.path.join(config.image, 'test')
    
    train_label = os.path.join(config.label, 'train')
    valid_label = os.path.join(config.label, 'valid')
    test_label = os.path.join(config.label, 'test')
    
    for folder in [train_img, valid_img, test_img, train_label, valid_label, test_label]:
        if not os.path.isdir(folder):
            os.makedirs(folder)
    
    data_list = list(map(lambda x : x.split('/')[-1], glob(config.image+'/*.png')))
    
    random.shuffle(data_list)
    length = len(data_list)
    train_set = data_list[:round(length*config.train)]
    valid_set = data_list[round(length*config.train):round(length*config.train)+round(length*config.valid)]
    test_set = data_list[round(length*config.train)+round(length*config.valid):]
    
    for data in train_set :
        # mv image
        shutil.move(os.path.join(config.image, data),
                    os.path.join(train_img, data))
        # mv label
        shutil.move(os.path.join(config.label, data),
                    os.path.join(train_label, data))
        
    for data in valid_set :
        # mv image
        shutil.move(os.path.join(config.image, data),
                    os.path.join(valid_img, data))
        # mv label
        shutil.move(os.path.join(config.label, data),
                    os.path.join(valid_label, data))
        
    for data in test_set :
        # mv image
        shutil.move(os.path.join(config.image, data),
                    os.path.join(test_img, data))
        # mv label
        shutil.move(os.path.join(config.label, data),
                    os.path.join(test_label, data))
        
    
def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, default='./images', help='image')
    parser.add_argument('--masks', type=str, default='./masks', help='masks')
    parser.add_argument('--train', type=float, default=0.8, help='train set ratio')
    parser.add_argument('--valid', type=float, default=0.1, help='valid set ratio')
    parser.add_argument('--test', type=float, default=0.1, help='test set ratio')

    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == '__main__' :
    opt = parse_opt()
    split(opt)
