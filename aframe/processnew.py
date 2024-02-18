import cv2
import mediapipe as mp
import numpy as np
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture('taichi.mp4')

frame_rate = 30.0
frame_counter = 0

frames_data = []

angle_key = {
    "right_arm_angle": (11, 13, 15),
    "left_arm_angle": (12, 14, 16),
    "right_torso_angle": (23, 11, 13),
    "left_torso_angle": (24, 12, 14),
    "right_knee_angle": (23, 25, 27),
    "left_knee_angle": (24, 26, 28),
    "right_leg_angle": (11, 23, 25),
    "left_leg_angle": (12, 24, 26)
}

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break  # Exit loop if video ends or there's an error
    
    # Calculate the timestamp based on the frame counter
    timestamp = frame_counter / frame_rate
    
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        def unit_vector(vector):
            return vector / np.linalg.norm(vector)

        def angle(p1, mid, p2):
            p1 = np.array(p1)
            mid = np.array(mid)
            p2 = np.array(p2)
            v1_u = unit_vector(p1 - mid)
            v2_u = unit_vector(p2 - mid)
            return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

        landmarks = [{'x': landmark.x, 'y': landmark.y, 'z': landmark.z, 'visibility': landmark.visibility} 
                     for landmark in results.pose_landmarks.landmark]

        frame_angles = {}
        for angle_name, indices in angle_key.items():
            p1, p2, p3 = [(landmarks[i]['x'], landmarks[i]['y']) for i in indices]
            frame_angle = angle(p1, p2, p3)
            frame_angles[angle_name] = frame_angle
                
        frames_data.append({'time': timestamp, 'landmarks': landmarks, 'angles': frame_angles})
    
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break
    
    # Increment frame counter
    frame_counter += 1

cap.release()
cv2.destroyAllWindows()

# Write data to JSON file
with open('landmarks_data.json', 'w') as f:
    json.dump(frames_data, f, indent=4)