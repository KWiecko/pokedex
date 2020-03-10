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

    gb_img = cv2.imread(args['query'])

    ratio = gb_img.shape[0] / 300.0

    # print(ratio)
    # input('ratio sanity check')

    gb_orig = gb_img.copy()
    rszd_img = imutils.resize(gb_img, height=300)

    gray_img = cv2.cvtColor(rszd_img, cv2.COLOR_BGR2GRAY)

    gray_bil_filter = cv2.bilateralFilter(gray_img, 11, 17, 17)
    edged = cv2.Canny(gray_bil_filter, 30, 200)

    plt.imshow(edged, cmap='gray', interpolation='nearest')
    plt.show()
    plt.clf()

    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)

    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c_idx, c in enumerate(cnts):
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        if len(approx) == 4:
            des_cont = approx
            break

    extrctd_contours = \
        cv2.drawContours(rszd_img, [des_cont], -1, (0, 255, 0), 3)
    print('extrctd_contours')
    print(des_cont)

    plt.imshow(extrctd_contours)  # , cmap='gray', interpolation='nearest')
    plt.show()
    plt.clf()

    pts = des_cont.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    sums = pts.sum(axis=1)

    rect[0] = pts[np.argmin(sums)]
    rect[2] = pts[np.argmin(sums)]

    diff = np.diff(pts, axis=1)
    # print(diff)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    print('pts')
    print(pts)

    print('rect')
    print(rect)

    res_rect = rect * ratio
    print(res_rect)

    tl, tr, br, bl = rect
