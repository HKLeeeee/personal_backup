import matplotlib.pyplot as plt
import os
from math import ceil
from glob import glob
import cv2

def visualize_images(image_dir, mask_dir, num_cols=4, num_images=10, title='Visualize masks', fontsize=20, figsize=None):
    images = sorted(glob(os.path.join(image_dir,'*.png')))
    masks = sorted(glob(os.path.join(mask_dir,'*.png')))
    
    num_rows = int(ceil(float(num_images) / float(num_cols)))
    
    if figsize is not None :
        fig, ax = plt.subplots(num_rows, num_cols, figsize=figsize)
    else :
        fig, ax = plt.subplots(num_rows, num_cols)
   
    
    idx = 0
    for image, mask in zip(images[:num_images], masks[:num_images]):
        col_id = idx % num_cols
        row_id = idx // num_cols
        img = plt.imread(image)
        m = cv2.imread(mask, cv2.IMREAD_UNCHANGED)
        ax[row_id, col_id].imshow(img) 
        ax[row_id, col_id].axis('off')
        ax[row_id, col_id].imshow(m, cmap='hot', alpha=0.5)
        idx += 1
    plt.suptitle(title, fontsize=fontsize)
    fig.tight_layout()
    plt.show()    