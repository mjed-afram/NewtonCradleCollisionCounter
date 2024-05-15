import cv2 as cv
import numpy as np


class ImagePreprocessor():
    def __init__(self):
        pass

    @staticmethod
    def binarizeImage(frame):
        # removing noise using median filter
        median_filter = cv.medianBlur(frame, 5)
        # convert to grayscale
        gray_frame = cv.cvtColor(median_filter, cv.COLOR_BGR2GRAY)
        # Adaptiv thresholding is helpfull when the illumination and the background change(illumination and background are static in this project). It dynamically adjusts the threshold value based on the local region's characteristics.
        adaptive_thresh = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 15, 5)  # 25, 1
        # closing operation to fill the holes in the image
        kernel = cv.getStructuringElement(cv.MORPH_CROSS, (7, 7)) # (cv.MORPH_ELLIPSE, (3, 3))
        closing = cv.morphologyEx(adaptive_thresh, cv.MORPH_CLOSE, kernel)
        print(closing.shape)

        return closing
    
