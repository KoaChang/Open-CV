import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ''

keyboard = Controller()

# bold filled keys
def drawAll(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h),
                          20, rt=0)
        cv2.rectangle(img, (x,y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    return img

# transparent keys
# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         w,h = button.size
#         cvzone.cornerRect(imgNew, (x, y, w, h),
#                           20, rt=0)
#         cv2.rectangle(imgNew, (x,y), (x + w, y + h),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.8
#     mask = imgNew.astype(bool)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out

class Button():
    def __init__(self,pos,text,size=(85,85)):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []

for i in range(len(keys)):
    for j,key in enumerate(keys[i]):
        buttonList.append(Button([j*100+50,100*i+50],key))

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    allHands, img = detector.findHands(img)
    img = drawAll(img,buttonList)

    if len(allHands) != 0:
        lmList, bboxInfo = allHands[0]['lmList'], allHands[0]['bbox']
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l = detector.findDistance(lmList[8][:2],lmList[12][:2],img)[0]

                if l < 40:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.05)

    cv2.imshow('Image',img)
    cv2.waitKey(1)
