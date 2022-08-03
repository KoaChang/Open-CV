import cv2 as cv
import numpy as np

# img = cv.imread('Resources/cards.jpg')

# width,height = 250,350
#
# pts1 = np.float32([[111,219],[287,188],[154,482],[352,440]])
# pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
#
# matrix = cv.getPerspectiveTransform(pts1,pts2)
# output = cv.warpPerspective(img,matrix,(width,height))

img = cv.imread('Resources/paper.jpg')

width,height = 300,400

pts1 = np.float32([[402,466],[929,545],[93,1178],[956,1326]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])

matrix = cv.getPerspectiveTransform(pts1,pts2)
output = cv.warpPerspective(img,matrix,(width,height))

cv.imshow('Blank',img)
cv.imshow('Warp',output)

cv.waitKey(0)







