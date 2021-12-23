import cv2
import time
import numpy as np
import Hand_Tracking_Module as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
pTime = 0
cTime =0

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
detector = hm.handDetector(detectionCon=0.75)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volpercent = 0
area = 0
colorVol = (255, 0, 0)


while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmList,bbox = detector.findPosition(img)
    if len(lmList) != 0:
        widB = bbox[2]-bbox[0]
        hB = bbox[3]-bbox[1]
        area = (widB*hB)//100
        # print(area)
        if 350<area<1500:
            # print("yes")
            length,img,lineInfo=detector.findDis(4,8,img)
            # print(length)

            volBar = np.interp(length, [30, 150], [400, 150])
            volpercent = np.interp(length, [30, 150], [0, 100])
            # print(vol)
            smoothnes = 5
            volpercent = smoothnes*round(volpercent/smoothnes)
            fingers = detector.fingerUp()
            print(fingers)
            if fingers[4] == 0:
                volume.SetMasterVolumeLevelScalar(volpercent / 100, None)
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 10, (255, 0, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

        # print(bbox)
        # print(lmList[4],lmList[8])

        # print(length)



        # if length < 30:

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)

    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,150,0),cv2.FILLED)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, f'Vol Set: {int(cVol)}', (400, 50), cv2.FONT_HERSHEY_COMPLEX,1, colorVol, 3)
    cv2.putText(img, f'{str(int(volpercent))}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 231, 167), 3)

    cv2.imshow("video",img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
