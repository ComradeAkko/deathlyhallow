# cloak.py by Jiro Mizuno

import cv2
import numpy as np

def cloak():
    # learned video capture from https://stackoverflow.com/questions/604749/how-do-i-access-my-webcam-in-python
    cam = cv2.VideoCapture(0)

    # get intial 24 frames to base background on
    for i in range(24):
        ret,background = cam.read()
    # flip the background for convolution purposes
    background = np.flip(background, axis = 1)

    # while the camera is running
    while(cam.isOpened()):
        # get the current camera
        ret, img = cam.read()

        # flip the image for convolution purposes
        img = np.flip(img, axis = 1)

        # convert the image of HSV color space
        # HSV = Hue, Saturation, Value
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # blur it via gaussian kernel
        blur = cv2.GaussianBlur(hsv, (11,11), 0)

        # set the lower range of red detection
        lower0 = np.array([0,120,70])
        upper0 = np.array([10,255,255])
        lowerMask = cv2.inRange(hsv, lower0, upper0)

        # set the higher range of red detection
        lower1 = np.array([170,120,70])
        upper1 = np.array([180,255,255])
        upperMask = cv2.inRange(hsv, lower1, upper1)

        # combine the masks
        newMask = lowerMask + upperMask

        # use the open morphological transformation to find noiseless red spots
        kernel = np.ones((5,5),np.uint8)
        newMask = cv2.morphologyEx(newMask, cv2.MORPH_OPEN, kernel)
        
        # replace pixels that are red with the backgroudn
        img[np.where(newMask == 255)] = background[np.where(newMask == 255)]

        # display the images
        cv2.imshow('Display', img)

        # end if commanded 
        k = cv2.waitKey(10)
        if k == 27:
            break

if __name__ == '__main__':
    cloak()

        

