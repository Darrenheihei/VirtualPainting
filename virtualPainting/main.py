# Reminder: please keep the pen straight when drawing to get a better effect
import cv2
import numpy as np
import copy
from collections import namedtuple

# webcam and display window setting
cap = cv2.VideoCapture(1)
cap.set(3, 800)
cap.set(4, 700)
cap.set(10, 150)

# stores the min and max of H, S, and V for each color
# the order is h_min, h_max, s_min, s_max, v_min, v_max
allowedColorsRange = {"orange": [0, 10, 135, 255, 172, 239],
                      "green": [51, 161, 121, 255, 77, 196],
                      "pink": [115, 179, 146, 255, 95, 194]}
# stores the actual color to display when it is being detected (in BGR, not RGB)
allowedColorVal = {"orange": (0, 128, 255),
                   "green": (51, 102, 0),
                   "pink": (200, 0, 200)}
Point = namedtuple("Point", ['x', 'y', 'color'])
createdPoints = [] # each element is in the format of (x, y, color)


def findColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in allowedColorsRange:
        # create a mask for each color to extract that color
        # lower = np.array([h_min, s_min, v_min])
        # upper = np.array([h_max, s_max, v_max])
        lower = np.array(allowedColorsRange[color][::2])
        upper = np.array(allowedColorsRange[color][1::2])
        mask = cv2.inRange(imgHSV, lower, upper)
        # after detecting the color, we need to find where is the object on our image
        # to do that, we need to detect the contours and approximate the bouding box around it
        x, y = getContours(mask)
        # (x, y) is the coordinate of the tip of the pen, then we can draw a circle on this position
        if not (x == 0 and y == 0):
            createdPoints.append(Point(x, y, color))

        # cv2.imshow("Mask: " + color, mask)
    # return mask

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # all the contours will be stored in the 'countours' variable
    x, y, width, height = 0, 0, 0, 0
    for cnt in contours:
        # for each contour, find the area
        x, y, width, height = 0, 0, 0, 0
        area = cv2.contourArea(cnt)
        if area > 500: # this is to avoid we detected some noise as contour
            # find perimeter, help approximating the corners of the edges
            perimeter = cv2.arcLength(cnt, True) # the True means the shape is closed
            # approximate the corners we have for each shape
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True) # the True means the shape is closed
            # draw a bounding box around the object
            x, y, width, height = cv2.boundingRect(approx)
            # cv2.rectangle(imgResult, (x, y), (x + width, y + height), (0, 255, 0), 1)

    return x + width//2, y

def empty(x):
    pass

# create trackers
# trackBars = createTrackBars([["Hue min", 0, 179],
#                              ["Hue max", 0, 179],
#                              ["Sat min", 0, 255],
#                              ["Sat max", 0, 255],
#                              ["Val min", 0, 255],
#                              ["Val max", 0, 255]]) # this is a dict

# cv2.namedWindow("TrackBars", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("TrackBars", 640, 100)
# cv2.createTrackbar("Hue min", "TrackBars", 0, 179, empty)
# cv2.createTrackbar("Hue max", "TrackBars", 179, 179, empty)
# cv2.createTrackbar("Sat min", "TrackBars", 0, 255, empty)
# cv2.createTrackbar("Sat max", "TrackBars", 255, 255, empty)
# cv2.createTrackbar("Val min", "TrackBars", 0, 255, empty)
# cv2.createTrackbar("Val max", "TrackBars", 255, 255, empty)
while True:
    # get images from webcam
    success, img = cap.read()
    imgResult = copy.deepcopy(img)

    # h_min = cv2.getTrackbarPos("Hue min", "TrackBars")
    # h_max = cv2.getTrackbarPos("Hue max", "TrackBars")
    # s_min = cv2.getTrackbarPos("Sat min", "TrackBars")
    # s_max = cv2.getTrackbarPos("Sat max", "TrackBars")
    # v_min = cv2.getTrackbarPos("Val min", "TrackBars")
    # v_max = cv2.getTrackbarPos("Val max", "TrackBars")
    mask = findColor(img)

    # draw the points
    for i in createdPoints:
        cv2.circle(imgResult, (i.x, i.y), 15, allowedColorVal[i.color], cv2.FILLED)

    # cv2.imshow("Video", cv2.bitwise_and(img, img, mask=mask))
    cv2.imshow("Video", imgResult)
    button = cv2.waitKey(1) & 0xFF
    if button == ord('q'):
        break
    elif button == ord('c'): # clear all created points
        createdPoints = []

    # TrackBar.displayTrackBar()
# orange: [0, 10, 158, 255, 142, 223]
# green: [61, 171, 121, 255, 77, 196]
# pink: [165, 179, 144, 255, 97, 192]