import cv2
import numpy as np

classesFile = 'coco.names'
classesName = []

#Param
whT = 320
confidenceThresh = 0.5
nmsThreshold = 0.3

def initializeNetwork(tiny=True):
    with open(classesFile, 'rt') as f:
        global classesName
        classesName = f.read().strip('\n').split('\n')

    if tiny:
        modelConfiguration = 'yolov3-tiny.cfg'
        modelWeights = 'yolov3-tiny.weights'
    else:
        modelConfiguration = 'yolov3.cfg'
        modelWeights = 'yolov3.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net

def detectObject(net, img):
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    findObjects(outputs, img)
    return img

def findObjects(outputs, img):
    hT, wT, cT = img.shape
    bbox = []                   #x, y, w, h
    classIds = []
    confidences = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]          #Removing First Five Columns
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confidenceThresh:
                w, h = int(detection[2]*wT), int(detection[3]*hT)
                x, y = int(detection[0]*wT - w/2), int(detection[1]*hT - h/2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confidences.append(float(confidence))
    #Eliminating the overlapping boxes
    indices = cv2.dnn.NMSBoxes(bbox, confidences, confidenceThresh, nmsThreshold)
    #Overlayying the Bounding Box Over Image
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 125, 0), 2)
        cv2.putText(img, f'{classesName[classIds[i]].upper()}',
                    (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 125, 0), 2)

#{int(confidences[i]*100)}%