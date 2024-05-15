import cv2 as cv
import numpy as np


class Tracker():
    def __init__(self):
        pass


    def extractCoordinates(frame):
        # Get the height and width of the frame
        height, width = frame.shape[:2]

        # Define the dimensions and position of the Region of Interest (ROI). This is the area where the tracking will be done.
        roi_width = 100
        roi_height = 600
        roi_x = (width - roi_width) // 2
        roi_y = (height - roi_height) // 2

        # Calculate the ROI coordinates and extract the ROI frame from the original frame
        roi = (roi_x, roi_y, roi_x + roi_width, roi_y + roi_height)
        roi_frame = frame[roi[1]:roi[3], roi[0]:roi[2]]

        # Find contours within the ROI frame
        contours, _ = cv.findContours(roi_frame, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        # Filter contours by area size
        max_area = 2200
        min_area = 400
        filtered_cnt = [contour for contour in contours if min_area < cv.contourArea(contour) < max_area]


        # Create a blank color frame with the same dimensions as the original frame
        color_frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Create a copy of the ROI frame to draw contours and bounding boxes on
        color_roi_frame = roi_frame.copy()
        color_roi_frame = cv.cvtColor(color_roi_frame, cv.COLOR_GRAY2BGR)


        box_positions = []
        for c in filtered_cnt:
            # Calculate the bounding box for each contour
            (x, y, w, h) = cv.boundingRect(c)
            # Draw the contour and bounding box
            cv.drawContours(color_roi_frame, [c], -1, (255, 0, 0), 2)
            cv.rectangle(color_roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the centroid of the contour (Just for visualization purpose)
            M = cv.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # Draw a circle at the centroid (Just for visualization purpose)
            cv.circle(color_roi_frame, (cX, cY), 3, (0, 0, 255), -1)
            
            # Append the position of the bounding box's center to the list
            box_positions.append((roi[0] + x + w // 2, roi[1] + y + h // 2))
            
        # Overlay the processed ROI frame onto the blank color frame
        color_frame[roi[1]:roi[3], roi[0]:roi[2]] = color_roi_frame

        # Return the color frame with drawn contours and bounding boxes, and the list of box positions
        return color_frame , box_positions
    

    def track(frame, coordinates):
        
        if len(coordinates) != 5:
            pass

        y_diff = abs(coordinates[-1][1] - coordinates[0][1])
        x_diff = coordinates[-1][0] - coordinates[0][0]

        last_x_coor = coordinates[-1][0]


        min = 0
        max = 50

        while True:
            
            if len(coordinates) >= 5 and x_diff == 0:

                return frame
            
            elif (min < ((abs(x_diff) * 100) / last_x_coor) < max) & ((y_diff / max) < abs(y_diff / x_diff) <= (y_diff / 1)) and len(coordinates) >=5:

                return frame


            return frame