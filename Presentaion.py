import cv2
import os
from cvzone.HandTrackingModule import HandDetector
import numpy as np


def presentationWindow(loc, w=1280, h=720):
    cwd = "temp-data"+f'\\{loc}'

    pathImages = sorted(os.listdir(cwd), key=len)

    width = w
    height = h

    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    cv2.namedWindow("Presentation", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("Presentation", w,h)
    # variables

    imgNumber = 0
    hs = int(120*0.8)
    ws = int(213*0.8)
    buttonCounter = 0
    buttonDelay = 20
    gestureThreshold = 300
    annotations = [[]]
    annotationNumber = 0
    annotationStart = False

    detector = HandDetector(detectionCon=0.6, maxHands=1)
    buttonPressed = False
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        FullPathImage = os.path.join(cwd, pathImages[imgNumber])

        imgCurrent = cv2.imread(FullPathImage,cv2.IMREAD_UNCHANGED)
        imgCurrent = cv2.resize(imgCurrent, (1280,720),interpolation = cv2.INTER_AREA)

       
        hands, img = detector.findHands(img)
        # draw line
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 225, 0), 10)

        if hands and buttonPressed is False:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            cx , cy = hand['center']
            lmList = hand['lmList']
            # Constrain values for ease of drawing
            indexFinger = lmList[8][0], lmList[8][1]

            xVal = int(np.interp(lmList[8][0], [width//2, w], [0, width]))
            yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
            indexFinger = xVal, yVal

            if cy <= gestureThreshold:
                # gesture 1 Left
                if fingers == [1, 0, 0, 0, 0]:
                    annotationStart = False
                    print('left')
                    if imgNumber > 0:
                        buttonPressed = True
                        annotations = [[]]
                        annotationNumber = 0
                        imgNumber -= 1

                # gesture 2 Right
                if fingers == [0, 0, 0, 0, 1]:
                    annotationStart = False
                    print('Right')
                    if imgNumber < len(pathImages)-1:
                        annotations = [[]]
                        annotationNumber = 0
                        buttonPressed = True
                        imgNumber += 1

            # gesture 3 Point
            if fingers == [0, 1, 0, 0, 0]:
                cv2.circle(imgCurrent,indexFinger,12,(0,0,225),cv2.FILLED)
                annotationStart = False

            # gesture 4 Draw lines
            if fingers == [0, 1, 1, 0, 0]:
                if annotationStart is False:
                    annotationStart = True
                    annotationNumber += 1
                    annotations.append([])
                cv2.circle(imgCurrent, indexFinger, 5, (0, 0, 225), cv2.FILLED)
                annotations[annotationNumber].append(indexFinger)
            else:
                annotationStart = False

            # gesture 5 Erase The Drawing
            if fingers == [0, 1, 1, 1, 0]:
                if annotations:
                    if annotationNumber >= 0:
                        annotations.pop(-1)
                        annotationNumber -= 1
                        buttonPressed = True
        else:
            annotationStart = False
        # button press event
        if buttonPressed:
            buttonCounter += 1
            if buttonCounter > buttonDelay:
                buttonCounter = 0
                buttonPressed = False

        for i in range(len(annotations)):
            for j in range(len(annotations[i])):
                if j != 0:
                    cv2.line(imgCurrent, annotations[i][j-1], annotations[i][j], (0, 0, 200), 12)

        # Adding webcam image in slides

        imgSmall = cv2.resize(img, (ws, hs))
        h, w, c = imgCurrent.shape
        imgCurrent[0:hs, w-ws:w] = imgSmall

        cv2.imshow('img',img)
        cv2.imshow("Presentation",imgCurrent)

        key = cv2.waitKey(1)
        if key == (ord('q') or ord('Q')):
            cv2.destroyAllWindows()
            break
    cap.release()


if __name__ == "__main__":
    presentationWindow()

