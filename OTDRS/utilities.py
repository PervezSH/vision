import cv2
import numpy as np

def getContour(img, contours, min_area = 1000, filter=0, draw=False):
    finalContours = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > min_area:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])
    finalContours = sorted(finalContours, key=lambda x:x[1], reverse=True)
    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (255,100,0), 3)
    return img, finalContours

def reorder(points):
    reorderedPoints = np.zeros_like(points)
    points = points.reshape((4,2))
    add = points.sum(1)
    reorderedPoints[0] = points[np.argmin(add)]
    reorderedPoints[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    reorderedPoints[1] = points[np.argmin(diff)]
    reorderedPoints[2] = points[np.argmax(diff)]
    return  reorderedPoints

def warpImg(img, points, w, h, pad=20):
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWarp = cv2.warpPerspective(img, matrix, (w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]
    return  imgWarp


def nothing(x):
    pass

def initializeTrackbars(initialTrackbarVals1=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 80, 255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 125, 255, nothing)

def valTrackers():
    Thresholds1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Thresholds2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    src = Thresholds1, Thresholds2
    return src

def findDistance(pts1, pts2):
    return ((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5