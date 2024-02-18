from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
import threading
import cv2
import mediapipe as mp
import time
import json
import numpy as np
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

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

FPS = 20
VAL_300 = 0.2
VAL_100 = 0.45
VAL_50 = 0.7

def judgement_value(val):
    if 0 <= val <= VAL_300:
        return 1, "Excellent!"
    elif VAL_300 < val <= VAL_100:
        return 1/3, "Great!"
    elif VAL_100 < val <= VAL_50:
        return 1/6, "OK!"
    else:
        return 0, "Miss :("

with open('./static/json/demo_data.json', 'r') as file:
    reference_data = json.load(file)

isTracking = False
start_time = 0
reference_index = 0
score_buffer = []
judgements = []
score = -1

def emit_pose_data():
    global isTracking, reference_index, start_time, score_buffer, judgements, score
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(0)  # Use the webcam
    frame_count = 0
    with app.app_context():
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                continue

            # Convert the BGR image to RGB, flip the image around y-axis for correct handedness output
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # Process the image and draw the pose annotation
            results = pose.process(image)
            if results.pose_landmarks:
                pos_loc = []
                track_loc = []
                for landmark in results.pose_landmarks.landmark:
                    pos_loc.append({"x": landmark.x, "y": -landmark.y, "z": landmark.z, "visibility": landmark.visibility})
                    track_loc.append({"x": landmark.x, "y": landmark.y, "z": landmark.z, "visibility": landmark.visibility})
                if frame_count % 10 == 0: #every x frames, update score
                    if score != -1:
                        print(f"Score: {score}")
                    buf_size = min(len(score_buffer), 10)
                    score = -1 if len(score_buffer) == 0 else sum(score_buffer[-buf_size:])/buf_size
                judgement_val, judgement_text = judgement_value(score)
                judgements.append(judgement_val)
                socketio.emit('update_model', {'pose': pos_loc, 'score': str(round(score, 3)), 
                                               'final': 'false', 'judgement': judgement_text})

            if isTracking:
                if not track_loc:
                    time.sleep(1/FPS)
                    continue
                
                current_time = time.time() - start_time
                # print(current_time, start_time)
                while reference_index < len(reference_data) and current_time > float(reference_data[reference_index]['time']):
                    reference_index = reference_index + 1
                if reference_index >= len(reference_data):
                    print("Reached end of video file.")
                    isTracking = False
                    score_buffer = []
                    final_score = sum(judgements)/len(judgements) * 1_000_000
                    socketio.emit('update_model', {'pose': pos_loc, 'score': '{:,.0f}'.format(round(final_score)), 'final': 'true'})
                    time.sleep(1/FPS)
                    continue
                reference_frame = reference_data[reference_index]

                frame_angles = {}
                for angle_name, indices in angle_key.items():
                    p1, p2, p3 = [(track_loc[i]['x'], track_loc[i]['y']) for i in indices]
                    frame_angle = angle(p1, p2, p3)
                    frame_angles[angle_name] = frame_angle

                score_buffer.append(compare_angles(reference_frame['angles'], frame_angles))
                frame_count += 1

            time.sleep(1/FPS)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/video-started', methods=['POST'])
def video_started():
    global isTracking, start_time, reference_index, score_buffer, judgements
    data = request.json
    print("Video Tracking Started")
    isTracking = True
    start_time = time.time()
    reference_index = 0
    score_buffer = []
    judgements = []
    return jsonify({"message": "Received"}), 200

@socketio.on('connect')
def test_connect():
    print('Client connected')
    threading.Thread(target=emit_pose_data).start()  # Start emitting pose data

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', ssl_context='adhoc')
    # socketio.run(app, debug=True)
