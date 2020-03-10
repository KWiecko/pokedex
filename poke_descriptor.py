import argparse
import cv2
import imutils
from imutils.paths import list_images
import numpy as np
import matplotlib.pyplot as plt
import pickle

from zernike_moments import ZermikeMoments


if __name__ == '__main__':
    ap = argparse.ArgumentParser()

    ap.add_argument('--sprites', default='./sprites')
    ap.add_argument('--index', default='./index_file')

    prsd_args = vars(ap.parse_args())

    desc = ZermikeMoments(21)
    index = {}

    prcsd_imgs_pths = list_images(prsd_args['sprites'])
    # print([el for el in prcsd_imgs_pths])

    for prcsd_img_pth in prcsd_imgs_pths:

        poke_name = prcsd_img_pth.split('/')[-1].replace('.png', '')
        # print(poke_name)

        poke_img = cv2.imread(prcsd_img_pth)

        clr_fdx_poke_img = cv2.cvtColor(poke_img, cv2.COLOR_BGR2GRAY)

        brdr_fxd_poke_img = cv2.copyMakeBorder(
            clr_fdx_poke_img, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=255)
        bitwise_img = cv2.bitwise_not(brdr_fxd_poke_img)
        bitwise_img[bitwise_img > 0] = 255

        outline = np.zeros(brdr_fxd_poke_img.shape, dtype='uint8')

        init_cnts = \
            cv2.findContours(
                bitwise_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        grbbd_cnts = imutils.grab_contours(init_cnts)
        srtd_cnts = sorted(grbbd_cnts, key=cv2.contourArea, reverse=True)[0]
        cnts_img = cv2.drawContours(outline, [srtd_cnts], -1, 255, -1)

        index[poke_name] = desc.describe(cnts_img)

        # print(index[poke_name])

        # fig, ax = plt.subplots(1, 3)
        # ax[0].imshow(poke_img)
        # ax[1].imshow(brdr_fxd_poke_img, cmap='gray', interpolation='nearest')
        # ax[2].imshow(cnts_img, cmap='gray', interpolation='nearest')
        # plt.show()

    with open(prsd_args['index'], 'wb') as index_file:
        pickle.dumps(index)

    pass
