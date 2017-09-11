#!/usr/bin/env python
import numpy as np
import cv2
# import os
# import argparse
# import yaml
# from glob import glob
###################################################################################################
## user input video name
def extant_file(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

if __name__ == "__main__":
    import argparse, sys, os
    from argparse import ArgumentParser

    parser = ArgumentParser(description="ikjMatrix multiplication")
    parser.add_argument("-i", "--input",
        dest="filename", required=True, type=extant_file,
        help="input file with two matrices", metavar="FILE")
    args = parser.parse_args()

    Name = args.filename
print(Name)
# #################################################################################################
# ##video processing backup
# #
cap = cv2.VideoCapture(Name)
K_undistort2 = np.array([[1822.7410517557776, 0.0, 1380.9286407307004], [0.0, 1823.2135457248423, 1107.4325084607897], [0.0, 0.0, 1.0]])
K_undistort1 = np.array([[1822.7410517557776, 0.0, 1380.9286407307004], [0.0, 1823.2135457248423, 1107.4325084607897], [0.0, 0.0, 1.0]])
K_array = np.array([[-0.3995256101289808, 0.1860076410786205, -0.01028873144026083, -0.003397377103708964, -0.0476809580344696]])
Name_1 = Name.split('.')
print(Name)
print(Name_1)
Name_2 = Name_1[0] + '_und.mkv'
fourcc = cv2.VideoWriter_fourcc(*'H264')
out = cv2.VideoWriter(Name_2,fourcc,12,  (1000,750))

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
