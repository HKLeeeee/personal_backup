import os
import shutil
import xml.etree.ElementTree as ET
import zipfile
from glob import glob
from tqdm.auto import tqdm
import sys
import json

## glob 한글 파싱 안됨..!!! 왜안됨?! ##

 # TODO fix here ####################################################################################
root = '/storage/교통문제 해결을 위한 CCTV 교통 영상(시내도로)'
section = '교통안전(Bbox)'
training = root + f'/Training/{section}'
validation = root + f'/Validation/{section}'

training_dest_root = root + '/Training/labels'

train_folder_list = glob(training + '/*/*/*.json')
valid_folder_list = glob(validation + '/*/*/*.json')

category = {
    # 시내도로 라벨 목록 
    1 : 'car', # 승용차
    2 : 'small-bus', # 소형버스
    3 : 'big-bus', # 대형버스
    4 : 'truck', # 트럭
    5 : 'trailer', # 대형 트레일러
    6 : 'motorcycle', # 오토바이, 자전거
    7 : 'pedestrian', # 보행자
    8 : 'unknown' # 분류없음
}
#####################################################################################################

def kitti_format():
    kitti = {
        'label' : '', # label
        'truncated' : 0,
        'occluded' : 0,
        'alpha' : 0,
        'xtl' : 0,
        'ytl' : 0,
        'xbr' : 0,
        'ybr' : 0,
        'dimensions_h' : 0,
        'dimensions_w' : 0,
        'dimensions_l' : 0,
        'location_x' : 0,
        'location_y' : 0,
        'location_z' : 0,
        'rotation_y' : 0
    }
    return kitti


def unzip(file_path, dest='.') :
    if not os.path.isdir(dest):
        os.makedirs(dest)
    
    with zipfile.ZipFile(file_path, 'r') as zip_ref :
        zip_ref.extractall(dest)
    
    return dest

            
def xml2kitty(xml, label_folder, dest):
    if not os.path.isdir(dest):
        os.makedirs(dest)
        
    xml_path = os.path.join(label_folder, xml)
    tree = ET.parse(xml_path)
    all_image_tag = tree.findall('image')
    
    #print(f'### {xml_path.split("/")[-1]} : {len(all_image_tag)} ###')
    
    for image in all_image_tag:
        image_name = image.attrib['name'].replace('png', 'txt')
        box_tag_all = image.findall('box')
        
        kitti_dict_list = []
        for box in box_tag_all:
            attrib = box.attrib
            kitti = kitti_format()
            
            for key in ['label', 'occluded', 'xtl', 'ytl', 'xbr', 'ybr']:
                   
                kitti[key] = attrib[key]
            
            kitti_dict_list.append(kitti)
        
        kitti_dest = os.path.join(dest, xml.replace('.xml',''))
        if not os.path.isdir(kitti_dest):
            os.makedirs(kitti_dest)
            
        write_kiiti(kitti_dest, image_name, kitti_dict_list)    
        
        
def write_kiiti(dest, file_name, kitti_dict_list):
    with open(os.path.join(dest, file_name), 'w' ) as file:
        for kitti_dict in kitti_dict_list :
            line = ' '.join(list(map(str, kitti_dict.values()))) + '\n'
            file.write(line)
          
def aihub2kiiti(json_path, dest) :
    if not os.path.isdir(dest):
        os.makedirs(dest)
    '''
    sample json_path :
    '{root}/Training/교통안전(Bbox)/충대서문네거리/SC5863301/충대서문네거리_SC5863301.json'
    dest :
    '{root}/Training/labels/충대서문네거리/SC5863301/'
    '''
    
    image_info_dict = {'id' : 'file_name'}
    with open(json_path, 'r') as f :
        print('[load]', json_path.split('/')[-1])
        json_obj = json.load(f)

        '''
        save info dict
        {'id': 'file_name',
        311473: 'SC5863301/20200909_020001_R_10050.jpg'}
        '''
        for image_info in json_obj['images']:
            image_info_dict[image_info['id']] = image_info['file_name']

        annotations = json_obj['annotations']
        print(json_path.split('/')[-1], ' 파일 하나에 있는 이미지 수', len(annotations))
        
    for annot in annotations:
        kitti_dict_list = []
        
        bbox = annot['bbox']
        obj_id = annot['category_id']
        img_id = annot['image_id']
                # print(image_info_dict[img_id])
        for o, b in zip(obj_id, bbox):
            kitti = kitti_format()
            
            kitti['label'] = category[o]
            kitti['xtl'] = b[0]
            kitti['ytl'] = b[1]
            kitti['xbr'] = b[2]
            kitti['ybr'] = b[3]
            
            # kitti dict 저장
            kitti_dict_list.append(kitti)
        
            
        file_name = image_info_dict[img_id].split('/')[-1].replace('jpg', 'txt')
        # txt 파일 저장 위치 지정
        write_kiiti(dest, file_name, kitti_dict_list)
        
        
def run_loop(zip_file_list):
    # 고속도로 
    for folder in tqdm(zip_file_list) :
        if '[원천]' in folder:
            continue
        
        print('[unzip]', folder)
        label_folder = unzip(folder, folder.replace('.zip',''))
        print('[save to]', label_folder)

        xmls = os.listdir(label_folder)
        
        for xml in xmls:
            xml2kitty(xml, label_folder, dest=label_folder.replace('바운딩박스', 'labels'))
            
        shutil.rmtree(label_folder)
        
        
'''
[시내도로 run]

for json_path in train_folder_list:
    path_list = json_path.split('/')[:-1]
    dest = '/'.join(path_list).replace('교통안전(Bbox)', 'labels')
    
    aihub2kiiti(json_path, dest)
    
'''