import cv2
import numpy as np
from wand.image import Image


aruco = cv2.aruco
# print dir(aruco)

# dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
# dictionary = aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

# marker = aruco.drawMarker(dictionary, 0, 36)
# cv2.imshow('0_100', marker)
# cv2.imwrite('0_100.png', marker)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

markerLength = 3.6   # Here, our measurement unit is centimetre.
markerSeparation = 1   # Here, our measurement unit is centimetre.
board = aruco.GridBoard_create(7, 10, markerLength, markerSeparation, dictionary)
# cv2.imshow('board', board)
# cv2.imwrite('board.png', board)

arucoParams = aruco.DetectorParameters_create()

# with Image(filename="test.pdf") as img:
#      img.save(filename="test.png")


# img = cv2.imread('../../images/image.png')
img = cv2.imread('test.png')
img = cv2.resize(img, None, fx=0.5, fy=0.5)
# cv2.imshow('board', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary)
print "corners",  corners
print "ids" , ids

for i, corner in enumerate( corners ):
    points = corner[0].astype(np.int32)
    cv2.polylines(img, [points], True, (0,255,255))
    print type(points[0])
    cv2.putText(img, str(ids[i][0]), tuple(points[0]), cv2.FONT_HERSHEY_PLAIN, 1,(0,0,0), 1)

cv2.imshow('drawDetectedMarkers', img)
cv2.imwrite('drawDetectedMarkers.png', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
