import time

import cv2
import os
import sys
import random

import numpy as np
import argparse
import random as rng

from PIL import Image


def main():
    path = "output/IRVC01/"

    try:
        if not os.path.exists(path):
            os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
        sys.exit()
    else:
        print("Successfully created the directory %s " % path)

    image = cv2.imread("images/02.jpg")

    cv2.imshow("image", image)
    cv2.waitKey(0)

    #  Draw BoundingBox
    tl = 25, 15
    br = 350, 100
    cv2.rectangle(image, tl, br, (0, 0, 255), 3)

    cv2.imshow("image", image)
    cv2.waitKey(0)

    count = 0

    #  Position Loop
    for x in range(0, image.shape[1], 10):
        for y in range(0, image.shape[0], 10):
            #  Zoom loop
            for z in np.arange(0.2, 3.0, 0.05):

                if z < 1.0:
                    createZoomedOutImage(image, z, x, y, tl, br)
                elif z == 1.0:
                    continue
                elif z > 1.0:
                    createZoomedInImage(image, z, x, y, tl, br)


    print("IMAGES CREATED : " + str(count))

def createZoomedInImage(image, zoom, imgPosx, imgPosy, boundBoxTL=None, boundBoxBR=None):
    # ALL IMAGES SHOULD BE THIS SIZE
    height = image.shape[0]
    width = image.shape[1]

    #  Resize image to zoom amount
    resizedImage = cv2.resize(image, (int(zoom*width), int(zoom*height)), interpolation=cv2.INTER_LINEAR)

    #  check to see if the bounding box is still in view
    resizedImageW = resizedImage[1]
    resizedImageH = resizedImage[0]
    newBBTLx = int(boundBoxTL[0]*zoom)
    newBBTLy = int(boundBoxTL[1]*zoom)

    newBBBRx = int(boundBoxBR[0]*zoom)
    newBBBRy = int(boundBoxBR[1]*zoom)

    ntl = newBBTLx, newBBTLy
    nbr = newBBBRx, newBBBRy

    #TEST
    # cv2.rectangle(resizedImage, ntl, nbr, (255, 0, 0), 2)
    # cv2.imshow("resizedbb", resizedImage)
    # cv2.waitKey(0)

    #  crop image to original height & width
    startPosX = imgPosx
    endPosX = width + imgPosx

    # if endPosX > resizedImage.shape[1]:
    #     endPosX =

    startPosY = imgPosy
    endPosY = height + imgPosy

    croppedImage = resizedImage[startPosY:endPosY, startPosX:endPosX]

    # cv2.imshow("resizedbb", croppedImage)
    # cv2.waitKey(0)

    #  check if all points of the bb are in the image
    croppedH = croppedImage.shape[0]
    croppedW = croppedImage.shape[1]

    boxVisible = True
    #  Verify that the sides are in the image
    if nbr[0]-startPosX > croppedW:
        # print("Bottom right CORNER Y : NOT IN")
        # cv2.imshow("resizedbb", croppedImage)
        # cv2.waitKey(0)
        boxVisible = False
    if ntl[0]-startPosX < 0:
        # print("top left CORNER Y : NOT IN")
        # cv2.imshow("resizedbb", croppedImage)
        # cv2.waitKey(0)
        boxVisible = False

    #  Verify that the top and bottom are in the image
    if ntl[1]-startPosY < 0:
        # print("TOP LEFT CORNER Y : NOT IN")
        # cv2.imshow("resizedbb", croppedImage)
        # cv2.waitKey(0)
        boxVisible = False

    if ntl[1]-startPosY > croppedH:
        # print("bottom LEFT CORNER Y : NOT IN")
        # cv2.imshow("resizedbb", croppedImage)
        # cv2.waitKey(0)
        boxVisible = False



    # cv2.imshow("cropped", croppedImage)
    # cv2.waitKey(0)

    #save & return
    if boxVisible:
        cv2.imwrite("output/IRVC01/" + "IRVC01_x" + str(zoom) + "_" + str(imgPosx) + "_" + str(imgPosy)+".png", croppedImage)


def createZoomedOutImage(image, zoom, posx, posy, tl=None, br=None):
    # ALL IMAGES SHOULD BE THIS SIZE
    height = image.shape[0]
    width = image.shape[1]

    x_offset = int((width - image.shape[1]) / 2) + posx
    y_offset = int((height - image.shape[0]) / 2) + posy

    #  Resize the image (Zoom out / shrink image )
    img = cv2.resize(image, (int(zoom*width), int(zoom*height)), interpolation=cv2.INTER_LINEAR)

    # Create black blank image
    blank_image = np.zeros((height, width, 3), np.uint8)


    blank_image[:] = (255, 255, 255)
    # cv2.imshow("Blank image", blank_image)
    # cv2.waitKey(0)

    # print(y_offset, x_offset)
    # print(y_offset+img.shape[0], x_offset+img.shape[1])


    try:
        blank_image[y_offset:y_offset+img.shape[0], x_offset:x_offset+img.shape[1]] = img
        cv2.imwrite("output/IRVC01/" + "IRVC01_x" + str(zoom) + "_" + str(posx) + "_" + str(posy) + ".png", blank_image)
    except Exception as e:
        # print(e)
        f = ":("
    # cv2.imshow("Blank image", blank_image)
    # cv2.waitKey(0)

def test():
    image = cv2.imread("images/02.jpg")
    tl = 25, 15
    br = 350, 100
    cv2.rectangle(image, tl, br, (0, 0, 255), 3)
    createZoomedInImage(image, 1.15, 10, 0, tl, br)

if __name__ == "__main__":
    main()
    # test()