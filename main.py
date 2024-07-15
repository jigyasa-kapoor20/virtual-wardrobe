import os

import cvzone
import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
cap.set(3, 3000)
cap.set(4, 4000)

detector = PoseDetector()

shirtFolderPath = "Resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
print(listShirts)
fixedRatio = [180/150, 340/190, 340/190, 320/190, 360/190]
shirtRatioHeightWidth = [250/300, 350 / 343, 350 / 343, 300 / 343, 350 / 343]
imageNumber = 0
imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)
counterRight = 0
counterLeft = 0
selectionSpeed = 10

while True:
    success, img = cap.read()
    img = detector.findPose(img)
    # img = cv2.flip(img,1)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
    if lmList:
        #center = bboxInfo["center"]

        lm11 = (lmList[11][0:2])
        lm12 = (lmList[12][0:2])

        imgShirt = cv2.imread(os.path.join(shirtFolderPath, listShirts[imageNumber]), cv2.IMREAD_UNCHANGED)
        widthOfShirt = int((lm11[0]-lm12[0])*fixedRatio[imageNumber])
        print(widthOfShirt)

        imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt * shirtRatioHeightWidth[imageNumber])))

        currentScale = (lm11[0]-lm12[0])/190
        offset = [[int(30*currentScale), int(50*currentScale)],  [int(90 * currentScale), int(60 * currentScale)],
                  [int(90 * currentScale), int(60 * currentScale)], [int(70*currentScale), int(60*currentScale)],
                  [int(90 * currentScale), int(60 * currentScale)]]

        try:
            img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[imageNumber][0], lm12[1] - offset[imageNumber][1]))
        except:
            pass

        img = cvzone.overlayPNG(img, imgButtonRight, (1074, 293))
        img = cvzone.overlayPNG(img, imgButtonLeft, (72, 293))

        if lmList[16][0] < 300:
            counterRight += 1
            cv2.ellipse(img, (139, 360), (66, 66), 0, 0,
                        counterRight * selectionSpeed, (0, 255, 0), 20)

            if counterRight * selectionSpeed > 360:
                counterRight = 0
                imageNumber += 1

        elif lmList[15][0] > 900:
            counterLeft += 1
            cv2.ellipse(img, (1138, 360), (66, 66), 0, 0,
                        counterLeft * selectionSpeed, (0, 255, 0), 20)

            if counterLeft * selectionSpeed > 360:
                counterLeft = 0

                if imageNumber > 0:
                    imageNumber -= 1

        else:
            counterRight = 0
            counterLeft = 0

    cv2.imshow("Image", img)
    cv2.waitKey(1)