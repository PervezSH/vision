import cv2
import numpy as np
import utilities

#param
scale = 2
widthP = 210*scale
hieghtP = 297*scale

pathImage = "1.jpg"
img = cv2.imread(pathImage)

def warpPers(img):
#Preprocessing
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey, (5, 5), 1)
    imgThreshold = cv2.Canny(imgBlur, 50, 85)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)
    imgErode = cv2.erode(imgDial, kernel, iterations=1)
#Find all contours
    imgContour = img.copy()
    imgBigContour = img.copy()
    imgWarp = img.copy()
    contours, hierarchy = cv2.findContours(imgErode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgContour, contours, -1, (255, 125, 0), 2)
#Find biggest contour
    imgBigContour, finalContours = utilities.getContour(imgBigContour, contours, min_area=5000, filter=4, draw=True)
    if len(finalContours) != 0:
        biggestContours = finalContours[0][2]
        imgWarp =  utilities.warpImg(img, biggestContours, widthP, hieghtP, 0)
        return imgBigContour, imgWarp
    else:
        return imgWarp, imgWarp