from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading
import cv2
import mediapipe as mp
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

def emit_pose_data():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)  # Use the webcam
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
                for landmark in results.pose_landmarks.landmark:
                    pos_loc.append({"x": landmark.x, "y": -landmark.y, "z": landmark.z, "visibility": landmark.visibility})
                socketio.emit('update_model', {'pose': pos_loc})

            time.sleep(1/30)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    print('Client connected')
    threading.Thread(target=emit_pose_data).start()  # Start emitting pose data

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', ssl_context='adhoc')
    # socketio.run(app, debug=True, host='0.0.0.0', ssl_context=('server.crt', 'server.key'))
