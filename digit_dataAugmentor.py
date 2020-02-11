import cv2
import os
import glob
import numpy as np
import random

def my_mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\") # 去除尾部 \ 符号
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        return True
    else:
        return False

#not fill
def randomShifting_nofill(inputImg, probability=1.0, shiftScale=0.2, fillFlg = True):
    imgSrc = inputImg.copy()
    dsize = (imgSrc.shape[1], imgSrc.shape[0])
    # print(imgSrc.shape)

    imgW = imgSrc.shape[1]
    Left_scale = (int)(imgW*shiftScale)
    Right_scale = (int)(-1*imgW*shiftScale)
    Right_Left_scale = random.randint(Right_scale, Left_scale)
    # print(Right_Left_scale)
    shiftSacle = abs(Right_Left_scale)
    if Right_Left_scale > 0:
        imgSrc = imgSrc[:imgSrc.shape[0], shiftSacle:imgSrc.shape[1]]
    else:
        imgSrc = imgSrc[:imgSrc.shape[0], 0:imgSrc.shape[1]-shiftSacle]
    
    # print(imgSrc.shape)

    imgH = imgSrc.shape[0]
    Up_scale = (int)(imgH*shiftScale)
    Down_scale = (int)(-1*imgH*shiftScale)
    Up_Down_scale = random.randint(Down_scale,Up_scale)
    # print(Up_Down_scale)
    shiftSacle = abs(Up_Down_scale)
    if Right_Left_scale > 0:
        imgSrc = imgSrc[shiftSacle:imgSrc.shape[0], :imgSrc.shape[1]]
    else:
        imgSrc = imgSrc[:imgSrc.shape[0]-shiftSacle, 0:imgSrc.shape[1]]
    
    if fillFlg:
        imgSrc = cv2.resize(imgSrc, dsize)

    # print(imgSrc.shape)
    return imgSrc

def dataAugmentor(src_path, dst_path):

    # 创建目标保存文件夹
    my_mkdir(dst_path)
    dbtype_list = os.listdir(src_path)
    print(dbtype_list)

    # 读取数据集源文件
    imgCnt = 0
    for folder in dbtype_list:
        dstfilepath = os.path.join(dst_path, folder)
        my_mkdir(dstfilepath) 

        data_path = os.path.join(src_path, folder)
        filenames = os.listdir(data_path)
        no_of_images = len(filenames)
        imgCnt += no_of_images
        print(data_path, no_of_images)
        for filename in filenames:
            imgPath = os.path.join(data_path, filename)
            # print("imgPath:{}".format(imgPath) )
            imgSrc = cv2.imread(imgPath)
            
            if imgSrc is None:
                continue
            else:
                imgSrc = cv2.cvtColor(imgSrc, cv2.COLOR_BGR2RGB)
                savePath = imgPath.replace(src_path, dst_path)
                #print("savePath:{}".format(savePath) )
                cv2.imwrite(savePath, imgSrc)
                agImg = randomShifting_nofill(imgSrc)
                savePath = savePath.replace(filename, "ag_" + filename)
                cv2.imwrite(savePath, agImg)
                #print("savePath:{}".format(savePath))
                break
        print("totalSize=",imgCnt*2)

src_path = "/mnt/AlgoTempData0/zhouxiangping/class/ReID_CodeClass/data/train_v0/"
dst_path = "/mnt/AlgoTempData0/zhouxiangping/class/ReID_CodeClass/data/train/"

if __name__ == "__main__":
    dataAugmentor(src_path, dst_path)
