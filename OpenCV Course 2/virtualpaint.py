import cv2
import numpy as np

# blue pen - [81,50,0,122,255,255]
# red pen - [0,235,68,10,255,255]
# purple sharpie - [126,43,0,159,255,255]
# green pen - [69,33,0,92,255,255]
# yellow highlighter - [22,93,0,45,255,255]

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

myColors = [[81,50,0,122,255,255],[0,235,68,10,255,255],[126,43,0,159,255,255],[69,33,0,92,255,255],[22,93,0,45,255,255]]
myColorValues = [[255,0,0],[0,0,255],[255,0,255],[0,255,0],[0,255,255]]  #BGR
myPoints = []  # [x,y,index of color]

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []

    for i,color in enumerate(myColors):
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = getContours(mask)

        if x!=0 and y!= 0:
            newPoints.append([x,y,i])

    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return (x+w//2,y)  #returns the coordinate of the top middle of the cap of the pen

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    img = cv2.flip(img,1)
    imgResult = cv2.flip(imgResult,1)
    newPoints = findColor(img,myColors,myColorValues)
    if len(newPoints) != 0:
        for p in newPoints:
            myPoints.append(p)

    if len(myPoints) != 0:
        drawOnCanvas(myPoints,myColorValues)

    cv2.imshow("Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break