import cv2
import mediapipe as mp
import time
import math
from pynput.mouse import Button, Controller

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils
mouse = Controller()

pTime = 0
cTime = 0
last_x = 0
last_y = 0
current_x = 0
current_y = 0
smooth_val = 3
fire_dis = 30
x_pos_adjust = -600
y_pos_adjust = -600
x_rate_adjust = 2.5
y_rate_adjust = 2.5

while True:
    ret, img = cap.read()
    imgHight, imgWidth, _ = img.shape
    if ret:
        img_flip = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img_flip, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        if results.multi_hand_landmarks:
            for one_hand in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img_flip, one_hand, mp_hands.HAND_CONNECTIONS)
                one_hand_LM = one_hand.landmark
                for p_id, p_lm in enumerate(one_hand_LM):
                    xPos = int(p_lm.x * imgWidth)
                    yPos = int(p_lm.y * imgHight)
                    zPos = 0 - p_lm.z
                    cv2.putText(img_flip, str(p_id), (xPos, yPos), cv2.FONT_HERSHEY_SIMPLEX, 10 * zPos, (0, 0, 255), 2)

                # fingure action: 4,8,12 are needed
                pos_set = []
                finger_set = [4, 8, 12]  # 4 and 8 for twist, 12 for movement
                for finger_id in finger_set:
                    f_xPos = int(one_hand_LM[finger_id].x * imgWidth)
                    f_yPos = int(one_hand_LM[finger_id].y * imgHight)
                    pos_set.append((f_xPos, f_yPos))

                direct_distance = math.sqrt((pos_set[0][0] - pos_set[1][0]) ** 2 + (pos_set[0][1] - pos_set[1][1]) ** 2)

                if direct_distance < fire_dis:  # if Twist figuers
                    print("True")
                    mouse.press(Button.left)
                else:
                    print("False")
                    mouse.release(Button.left)

                # else:
                cursorLoc_x = pos_set[2][0] * x_rate_adjust + x_pos_adjust
                cursorLoc_y = pos_set[2][1] * y_rate_adjust + y_pos_adjust

                # make cursor move smoothly
                current_x = last_x + (cursorLoc_x - last_x) / smooth_val
                current_y = last_y + (cursorLoc_y - last_y) / smooth_val

                # set cursor location
                mouse.position = (current_x, current_y)

                last_x = current_x
                last_y = current_y

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img_flip, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('img', img_flip)

    if cv2.waitKey(1) == ord('q'):
        break
