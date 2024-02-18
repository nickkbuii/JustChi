import cv2
import mediapipe as mp
import time
import numpy as np
import func as f
import moves as m

mp_pose = mp.solutions.pose
print(list(mp_pose.POSE_CONNECTIONS))
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# turn on the webcam
cap = cv2.VideoCapture(0)

#initializations
key_landmark_indices = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]
moveIndex = 0
score = 0

# countdown
print(3)
time.sleep(1.5)
print(2)
time.sleep(1.5)
print(1)
time.sleep(1.5)
print("GO!!")

#capture start time
start = time.time()
t = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB, flip the image around y-axis for correct handedness output
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image and draw the pose annotation
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:

        # get current time
        t = round(time.time() - start)

        # dictionary of important vectorized landmarks
        key_points = {
            str(k): 
                np.array((results.pose_landmarks.landmark[k].x, results.pose_landmarks.landmark[k].y))
            for k in key_landmark_indices
        }

        # important angle measurements
        right_arm_angle = f.angle(key_points["11"], key_points["13"], key_points["15"])
        left_arm_angle = f.angle(key_points["12"], key_points["14"], key_points["16"])
        right_torso_angle = f.angle(key_points["23"], key_points["11"], key_points["13"])
        left_torso_angle = f.angle(key_points["24"], key_points["12"], key_points["14"])
        right_knee_angle = f.angle(key_points["23"], key_points["25"], key_points["27"])
        left_knee_angle = f.angle(key_points["24"], key_points["26"], key_points["28"])
        right_leg_angle = f.angle(key_points["11"], key_points["23"], key_points["25"])
        left_leg_angle = f.angle(key_points["12"], key_points["24"], key_points["26"])

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if t == m.key_times[moveIndex]:
            angles = [right_arm_angle, left_arm_angle, right_torso_angle, left_torso_angle, right_knee_angle, left_knee_angle, right_leg_angle, left_leg_angle]
            comparisons = [f.similarity(m.key_angles[moveIndex][i], 0.261799, angles[i]) for i in range(len(angles))]
            if all(comparisons): score+=1
            print(f'Score: {score} \n')

            # increment so we can look for next move
            moveIndex+=1


    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
