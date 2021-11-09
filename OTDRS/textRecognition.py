import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#reading image
img = cv2.imread('images/1.jpg')
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

#Detecting Words
def boundingBoxes(img):
    hImg = img.shape[0]
    wImg = img.shape[1]
    boxes = pytesseract.image_to_data(img)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            if len(b)==12:
                x,y,w,h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,0), 1)
                cv2.putText(img, b[11], (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
    return img

cv2.waitKey(0)