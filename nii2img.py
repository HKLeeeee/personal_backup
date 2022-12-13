# nii(mri, 의료영상) -> 이미지파일로 바꾸는 파일
# for segmentation

# pip3 install med2image

## Ubuntu
# sudo apt-get update
# sudo apt-get install -y python3-tk

import subprocess
from glob import glob
import os
import argparse
import nibabel as nib
import cv2
from tqdm import tqdm

def convert(config):
    files = glob(config.source + ('/*nii*'))
    print(f'#############total : {len(files)}#################')
    if not os.path.isdir(config.dest):
        os.mkdir(config.dest)
        
    for src in tqdm(files) :
        if config.prefix == '':
            prefix = src.split('/')[-1].split('.')[0]
        else :
            prefix = config.prefix

        if not config.mask:
            command = ['med2image', '-i', src, '-d', config.dest, 
                    '--outputFileStem', prefix, '--outputFileType', config.file_type]
            if config.only_middle:
                command.append('--sliceToConvert')
                command.append('m')
            
            subprocess.run(command)
        else :
            mask_img = nib.load(src).get_fdata()
            for i in range(mask_img.shape[2]):
                slice = mask_img[:,:,i]
                save_dir = os.path.join(config.dest, f'{prefix}-slice{str(i).zfill(3)}.png')
                cv2.imwrite(save_dir, slice)
                
def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='./dataset/task/imagesTr', help='nii files sources')
    parser.add_argument('--dest', type=str, default='./dataset/images', help='directory to save converted images')
    parser.add_argument('--prefix', default='', help='prefix of converted images')
    parser.add_argument('--file_type', type=str, default='png', help='output file type jpg/png')
    parser.add_argument('--only_middle', action='store_true', help='convert only middle slice')
    parser.add_argument('--mask', action='store_true', help='mask image')
    return parser.parse_known_args()[0] if known else parser.parse_args()


if __name__ == '__main__' :
    opt = parse_opt()
    convert(opt)