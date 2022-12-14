import cv2
import numpy as np

with open('count.txt') as file:
    count = int(file.read().strip())

while True:
    img = cv2.imread('Resources/p1.jpg')
    minArea = 500
    color = (255,0,255)
    plateCascade = cv2.CascadeClassifier("Resources/haarcascade_russian_plate_number.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img,'Number Plate',(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,thickness=2)
            imgPlate = img[y:y+h,x:x+w]
            cv2.imshow('Plate',imgPlate)

    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(f'Resources/Scanned/NoPlate_{count}.jpg',imgPlate)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,
                    2, (0, 0, 255), 2)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1

    with open('count.txt', 'w') as file:
        file.write(str(count))

cv2.destroyAllWindows()
