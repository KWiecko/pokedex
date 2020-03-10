import argparse
import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
# from pyimageserach import imutils
import imutils
from skimage import exposure


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--query', default='./gb_imgs/gameboy-query.jpg')

    args = vars(ap.parse_args())

    # gb_img = cv2.imread(args['query'])

    image = cv2.imread(args["query"])
    ratio = image.shape[0] / 300.0
    orig = image.copy()
    image = imutils.resize(image, height=300)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    plt.imshow(edged, cmap='gray', interpolation='nearest')
    plt.show()
    plt.clf()

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            print('Contour found!')
            break

    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
    cv2.imshow("Game Boy Screen", image)
    cv2.waitKey(0)
