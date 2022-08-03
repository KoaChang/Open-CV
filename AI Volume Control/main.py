import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript

################################
wCam, hCam = 640, 480
################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7,maxHands=1)

volBar = 400
volPer = 0
area = 0
colorVol = (255,0,0)

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    allHands, img = detector.findHands(img,draw=True)

    if len(allHands) != 0:
        lmList = allHands[0]['lmList']
        bbox = allHands[0]['bbox']
        area = (bbox[2]) * (bbox[3]) // 100

        if 250 < area < 1000:
            x1, y1 = lmList[4][:2]
            x2, y2 = lmList[8][:2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            distance,lineInfo,img = detector.findDistance((x1,y1),(x2,y2),img,draw=True)

            # Hand range 50 - 300
            # Volume Range 0-10

            volBar = np.interp(distance, [50, 250], [400, 150])
            volPer = np.interp(distance, [50, 250], [0, 100])

            smoothness = 5
            volPer = smoothness * round(volPer / smoothness)

            fingers = detector.fingersUp(allHands[0])

            # If pinky is down set volume
            if fingers[4] == 1:
                osascript.osascript("set volume output volume {}".format(volPer))
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cVol = osascript.osascript('output volume of (get volume settings)')[1]
    cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, colorVol, 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
