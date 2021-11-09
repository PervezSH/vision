import cv2
import numpy as np
import utilities

#param
scale = 2
widthP = 210*scale
hieghtP = 297*scale

pathImage = "1.jpg"
img = cv2.imread(pathImage)

def measureDim(img):
# Preprocessing
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgThreshold = cv2.Canny(imgBlur, 50, 85)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
    imgErode = cv2.erode(imgDial, kernel, iterations=1)
# Find all contours
    imgContour = img.copy()
    imgBigContour = img.copy()
    imgWarp = img.copy()
    contours, hierarchy = cv2.findContours(imgErode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour, contours, -1, (255, 125, 0), 2)
# Find biggest contour
    imgBigContour, finalContours = utilities.getContour(imgBigContour, contours, min_area=5000, filter=4, draw=True)
    if len(finalContours) != 0:
        biggestContours = finalContours[0][2]
        imgWarp =  utilities.warpImg(img, biggestContours, widthP, hieghtP)
        imgGreyWI = cv2.cvtColor(imgWarp, cv2.COLOR_BGR2GRAY)
        imgBlurWI = cv2.GaussianBlur(imgGreyWI, (5, 5), 1)
        imgThresholdWI = cv2.Canny(imgBlurWI, 50, 50)
        kernel = np.ones((5, 5))
        imgDialWI = cv2.dilate(imgThresholdWI, kernel, iterations=2)
        imgErodeWI = cv2.erode(imgDialWI, kernel, iterations=1)
    # Find all contours
        imgContourWI = imgWarp.copy()
        imgBigContourWI = imgWarp.copy()
        imgMeasured = imgWarp.copy()
        contours2, hierarchy2 = cv2.findContours(imgErodeWI, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(imgContourWI, contours2, -1, (255, 125, 0), 2)
        imgBigContour2, finalContours2 = utilities.getContour(imgBigContourWI, contours2, min_area=5000, filter=4, draw=False)
        if len(finalContours2) != 0:
            for obj in finalContours2:
                #cv2.polylines(imgBigContour2, [obj[2]], True, (255, 125, 0), 2)
                nPoints = utilities.reorder(obj[2])
                width = round((utilities.findDistance(nPoints[0][0]//scale, nPoints[1][0]//scale)/10), 1) - 0.1
                height = round((utilities.findDistance(nPoints[0][0]//scale, nPoints[2][0]//scale)/10), 1) - 0.1
                cv2.arrowedLine(imgBigContour2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255 ,125 ,0), 2, 8, 0, 0.05)
                cv2.arrowedLine(imgBigContour2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 125, 0), 2, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgBigContour2, '{}cm'.format(width), (x+w//2, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, .5,
                            (255, 125, 0), 1)
                cv2.putText(imgBigContour2, '{}cm'.format(height), (x-w//4, y+h//2), cv2.FONT_HERSHEY_COMPLEX_SMALL, .5,
                            (255, 125, 0), 1)
                imgMeasured = imgBigContour2
        return imgMeasured