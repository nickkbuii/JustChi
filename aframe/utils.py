import numpy as np

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle(p1, mid, p2):
    p1 = np.array(p1)
    mid = np.array(mid)
    p2 = np.array(p2)
    v1_u = unit_vector(p1 - mid)
    v2_u = unit_vector(p2 - mid)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def compare_angles(reference, frame):
    differences = [abs(reference[key] - frame[key]) for key in reference]
    return sum(differences) / len(differences)

def objective_function(keypoints1, keypoints2, scale, translation):
    transformed_keypoints1 = (keypoints1 * scale) + translation
    ssd = np.sum((transformed_keypoints1 - keypoints2)**2)
    return ssd

def gradient_descent(keypoints1, keypoints2, learning_rate=0.001, iterations=1000):
    scale = 1.0
    translation = np.zeros(2)
    
    for i in range(iterations):
        scale_grad = 2 * np.sum((keypoints1 * scale + translation - keypoints2) * keypoints1)
        translation_grad = 2 * np.sum(keypoints1 * scale + translation - keypoints2, axis=0)
        scale -= learning_rate * scale_grad
        translation -= learning_rate * translation_grad
        if i == iterations-1:
            cost = objective_function(keypoints1, keypoints2, scale, translation)
            print(f"Iteration {i}: SSD = {cost}")
    
    return scale, translation

def apply_transformation(keypoints, scale, translation):
    return (keypoints * scale) + translation

def calculate_similarity(transformed_keypoints, keypoints):
    distances = np.sqrt(np.sum((transformed_keypoints - keypoints)**2, axis=1))
    similarity_score = np.mean(distances)
    return similarity_score

def filter_keypoints_by_visibility(keyframe1, keyframe2):
    print(keyframe1[:, 2])
    print(np.where(keyframe1[:, 2] > 0.5))
    visible_indices = np.where((keyframe1[:, 2] > 0.5) & (keyframe2[:, 2] > 0.5))[0]
    print(visible_indices)
    filtered_keyframe1 = keyframe1[visible_indices, :2]
    filtered_keyframe2 = keyframe2[visible_indices, :2]
    return filtered_keyframe1, filtered_keyframe2


if __name__ == "__main__":
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

        max_frames = 3
        count = 0
        cap = cv2.VideoCapture(0)  # Use the webcam
        while cap.isOpened():
            count += 1
            if count > max_frames:
                break
            success, image = cap.read()
            if not success:
                continue
            
            # Convert the BGR image to RGB, flip the image around y-axis for correct handedness output
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # Process the image and draw the pose annotation
            results = pose.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            visible = False
            if results.pose_landmarks:
                pos_loc = []
                for landmark in results.pose_landmarks.landmark:
                    if landmark.visibility > 0.5:
                        visible = True
                    pos_loc.append([landmark.x, landmark.y, landmark.visibility])
                    # pos_loc.append({"x": landmark.x, "y": -landmark.y, "z": landmark.z, "visibility": landmark.visibility})
                keyframes.append(pos_loc)
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            print(visible)

            cv2.imshow('MediaPipe Pose', image)
            if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
                break
            time.sleep(1)
        cap.release()

    # Example keypoints (these should be replaced with actual data)
    keypoints = np.array(keyframes)

    for i in range(len(keypoints)-1):
        keypoints1 = keypoints[i]
        keypoints2 = keypoints[i+1]
        keypoints1, keypoints2 = filter_keypoints_by_visibility(keypoints1, keypoints2)
        if len(keypoints1) < 10:
            print("Not enough keypoints for comparison")
            continue

        # Normalize keypoints to have zero mean
        keypoints1_centered = keypoints1 - np.mean(keypoints1, axis=0)
        keypoints2_centered = keypoints2 - np.mean(keypoints2, axis=0)

        # Run gradient descent
        scale, translation = gradient_descent(keypoints1_centered, keypoints2_centered)

        # Apply the optimal scale and translation to keypoints1
        transformed_keypoints1 = apply_transformation(keypoints1_centered, scale, translation)

        # Calculate similarity score
        similarity_score = calculate_similarity(transformed_keypoints1, keypoints2_centered)

        # Calculate similarity score
        print(f"Optimal scale: {scale}")
        print(f"Optimal translation: {translation}")
        print(f"Valid keypoints: {len(keypoints1)}")
        print(f"Similarity score (average Euclidean distance): {similarity_score}")
