import cv2 as cv
import numpy as np


class FramePreprocessor():
    def __init__(self):
        pass


    @staticmethod
    def HSVsegment(frame):

        blurr = cv.medianBlur(frame, 3)
        hsv = cv.cvtColor(blurr, cv.COLOR_BGR2HSV)
        lower_bound = np.array([10, 55, 120])     # 34 can be up to 100
        upper_bound = np.array([180, 255, 255])
        mask = cv.inRange(hsv, lower_bound, upper_bound)
        result = cv.bitwise_and(frame, frame, mask=mask)

        return result

    @staticmethod
    def binarizeImage(frame):
        # removing noise using median filter
        median_filter = cv.medianBlur(frame, 5)
        # convert to grayscale
        gray_frame = cv.cvtColor(median_filter, cv.COLOR_BGR2GRAY)
        # Adaptiv thresholding is helpfull when the illumination and the background change(illumination and background are static in this project). It dynamically adjusts the threshold value based on the local region's characteristics.
        adaptive_thresh = cv.adaptiveThreshold(gray_frame, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 15, 9)  # 15, 5
        # closing operation to fill the holes in the image
        kernel = cv.getStructuringElement(cv.MORPH_CROSS, (7, 7)) # (cv.MORPH_ELLIPSE, (3, 3))
        closing = cv.morphologyEx(adaptive_thresh, cv.MORPH_CLOSE, kernel)
        print(closing.shape)

        return closing
    
    @staticmethod
    def fillGaps(frame):

        floodfill = frame.copy()
        h, w = floodfill.shape[:2]
        mask = np.zeros((h+2, w+2), np.uint8)
        cv.floodFill(floodfill, mask, (0, 0), 255)
        floodfill_inv = cv.bitwise_not(floodfill)
        filled_gaps = frame | floodfill_inv

        return filled_gaps
    
    