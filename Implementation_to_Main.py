import cv2
import pickle as pk
import cvzone as cvz
import numpy as np

frame = cv2.VideoCapture('Parked-stabilized.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pk.load(f)

width, height = 107, 50

def checkParkingSpace(imgPro):

    spaceCounter =  0
    for pos in posList:
        x,y = pos


        imgCrop = imgPro[y:y+ height, x:x+width]
        # cv2.imshow(str(x*y),imgCrop)

        count = cv2.countNonZero(imgCrop)
        cvz.putTextRect(img,str(count),(x,y+height-3),scale=1,thickness=2, offset=0)


        if count < 980:
            color = (0,255,0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0,0,255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvz.putTextRect(img, f'Empty Space: {spaceCounter}/{len(posList)}', (100,50), scale=3, thickness=5, offset=20,colorR=(0,0,0))






while True:

    if frame.get(cv2.CAP_PROP_POS_FRAMES) == frame.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = frame.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV,25,16)

    imgMedian = cv2.medianBlur(imgThreshold,5)

    kernel = np.ones((3,3),np.uint8)
    imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)

    checkParkingSpace(imgDilate)




  # cv2.imshow("imgMedian",imgMedian)
    cv2.imshow("image",img)
    # cv2.imshow("imageGray",imgGray)
    key = cv2.waitKey(10)

    if key == 27:
        break