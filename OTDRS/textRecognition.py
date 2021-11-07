import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#reading image
img = cv2.imread('download.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)              #converting BGR to RGB

#reading video
def realTimeTextRecognition():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    while True:                                             #reading video frame by frame
        isTrue, frame = capture.read()
        if not isTrue:
            print("Not able to read frame:(\n----Displaying result from default image----")
            break
        cv2.imshow("WebCam Feed", frame)                     #displaying frame

        if cv2.waitKey(10) & 0xff == 32:
            img = frame
            capture.release()
            cv2.destroyWindow("WebCam Feed")
            break

def getText(img):
    return pytesseract.image_to_string(img)

cv2.waitKey(0)