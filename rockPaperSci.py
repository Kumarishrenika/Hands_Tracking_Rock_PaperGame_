import cvzone
import numpy as np
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import random

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]    #[ 1st zero for AI and last zero for Player]

while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img,(0,0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
 

#  find Hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time()- intialTime
            cv2.putText(imgBG, str(int(timer)), (605,435),cv2.FONT_HERSHEY_PLAIN,6, (255,0,255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0,0,0,0,0]:
                        playerMove = 1    # Rock
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2    # Paper
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3   # Scissor

                    randomNumber = random.randint(1,3)    

                    imgAI = cv2.imread(f"Resources/{randomNumber}.png",cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

                    # player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                          (playerMove == 2 and randomNumber == 1) or \
                          (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI  Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                          (playerMove == 1 and randomNumber == 2) or \
                          (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1



    imgBG[234:654,795:1195] = imgScaled
    
    if stateResult: 
         imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

    cv2.putText(imgBG, str((scores[0])), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str((scores[1])), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Scaled", imgScaled)
    if cv2.waitKey(1) == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False

    if cv2.waitKey(1) == ord('q'):
        break
    

