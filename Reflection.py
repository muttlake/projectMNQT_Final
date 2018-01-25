"""
Project MNQT
Reflection class
"""

import numpy as np
import cv2

class Reflection:

    #Horizontal Reflection
    def reflectOnAxisX(self, image):

        row, col = image.shape
        new_image = np.zeros((row, col))

        for x in range(int(row-1/2)):
            for y in range(col):
                topPix = image[x, y]
                bottomPix = image[row - x -1, y]
                new_image[x, y] = bottomPix
                new_image[row - x -1, y] = topPix

        return new_image

    #Vertical Reflection
    def reflectOnAxisY(self, image):
        row, col = image.shape
        new_image = np.zeros((row, col))

        for x in range(row):
            for y in range(int(col-1/2)):
                leftPix = image[x, y]
                rightPix = image[x, col - y - 1]
                new_image[x, y] = rightPix
                new_image[x, col - y - 1] = leftPix

        return new_image
