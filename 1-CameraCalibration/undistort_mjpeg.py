#!/usr/bin/env python
import numpy as np
import cv2
import os
import argparse
# import yaml
# from glob import glob
# # cap = cv2.VideoCapture('C:/Users/Iris/Desktop/Nearmiss_summer2017/NearMiss_submit/0-Video&PointCloud Collection/Raw_Video/2017_8_8/1_1.mkv')


#################################################################################################
##video processing backup
#
cap = cv2.VideoCapture('C:/Users/Iris/Desktop/Nearmiss_summer2017/NearMiss_submit/0-Video&PointCloud Collection/ffmpeg-20170520-64ea4d1-win64-static/bin/output_clip1.mkv')
K_undistort2 = np.array([[1822.7410517557776, 0.0, 1380.9286407307004], [0.0, 1823.2135457248423, 1107.4325084607897], [0.0, 0.0, 1.0]])
K_undistort1 = np.array([[1822.7410517557776, 0.0, 1380.9286407307004], [0.0, 1823.2135457248423, 1107.4325084607897], [0.0, 0.0, 1.0]])
K_array = np.array([[-0.3995256101289808, 0.1860076410786205, -0.01028873144026083, -0.003397377103708964, -0.0476809580344696]])

fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter('C:/Users/Iris/Desktop/Nearmiss_summer2017/NearMiss_submit/0-Video&PointCloud Collection/ffmpeg-20170520-64ea4d1-win64-static/bin/ouput_clip1_und.mkv',fourcc,12,  (1000,750))

while(cap.isOpened()):
    ret, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_und = cv2.undistort(frame, K_undistort1, K_array,
                            newCameraMatrix=K_undistort2)
    img_und_resize = cv2.resize(img_und,(1000, 750))
    frame_resize = cv2.resize(frame, (1000, 750))


    cv2.imshow('un-distort frame',img_und_resize)
    cv2.imshow('old frame',frame_resize)
    out.write(img_und_resize)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
