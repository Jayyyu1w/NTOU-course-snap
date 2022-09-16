import os
import cv2
import pytesseract
import scipy.ndimage as ndi
import numpy as np
import skimage.restoration as re
from PIL import Image
from skimage import filters
from matplotlib import pyplot as plt

os.chdir(os.path.dirname(__file__))

def noise_reduce(img,thr,pixlim):
    chpoi=[]
    row,col=img.size
    pixdata=img.load()
    for y in range(0,col):
        for x in range(0,row):
            if x==0 or x==row-1 or y==0 or y==col-1 or pixdata[x,y] > thr:
                pixdata[x,y]=255
                continue
            count=0
            if pixdata[x,y-1] > thr:
                count=count+1
            if pixdata[x,y+1] > thr:
                count=count+1
            if pixdata[x - 1, y] > thr:
                count = count + 1
            if pixdata[x + 1, y] > thr:
                count = count + 1
            if pixdata[x - 1, y - 1] > thr:
                count = count + 1
            if pixdata[x - 1, y + 1] > thr:
                count = count + 1
            if pixdata[x + 1, y - 1] > thr:
                count = count + 1
            if pixdata[x + 1, y + 1] > thr:
                count = count + 1
            if count > pixlim:
                chpoi.append((x,y))
    for i in chpoi:
        pixdata[i[0],i[1]]=255
    return img

def noise_pixel(img,eps):
    row,col=img.size
    pixdata=img.load()
    for y in range(1,col-1):
        for x in range(1,row-1):
            cnt=0
            if np.abs(pixdata[x,y]-pixdata[x+1,y])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x-1,y])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x,y+1])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x,y-1])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x-1,y-1])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x-1,y+1])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x+1,y-1])<=eps:
                cnt=cnt+1
            if np.abs(pixdata[x,y]-pixdata[x+1,y+1])<=eps:
                cnt=cnt+1
            if cnt == 0:
                pixdata[x,y]=255
    return img


if __name__=="__main__":
    #for i in range(0,20):
        img=Image.open(f'pic{16}.jpg').convert('L')
        denoimg=img
        denoimg=noise_reduce(denoimg,185,6)
        denoimg1=noise_reduce(denoimg,140,6)
        denoimg2=noise_pixel(denoimg1,45)
        denoimg2=denoimg1
        denoimg2=np.array(denoimg2)
        r, denobin=cv2.threshold(denoimg2,195,255,cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        plt.imshow(denobin,cmap='gray')
        plt.show()
        strlist=list(pytesseract.image_to_string(denobin))
        for i in range(len(strlist)):
            if strlist[i] == 'O' or strlist[i] == 'o':
                strlist[i]='D'
            if strlist[i].islower():
                strlist[i].upper()
        str="".join(strlist)
        str=str.replace(" ","")
        print(str)