import time
import threading
import cv2
import mediapipe as mp
import time

keyframes = []
capture = True
if capture:
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils
    time.sleep(2)

    cap = cv2.VideoCapture(0)  # Use the webcam
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
            pos_loc = []
            for landmark in results.pose_landmarks.landmark:
                pos_loc.append([landmark.x, landmark.y, landmark.visibility])
            keyframes.append(pos_loc)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
            break
        time.sleep(1/20)

    cap.release()
cv2.destroyAllWindows()

