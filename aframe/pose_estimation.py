import cv2
import mediapipe as mp
import time
import numpy as np
import func as f

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture('./static/videos/test_calibration_daniel.mov')

#wave_right_groundtruth = [[np.array(0.4984560012817383, 0.632222056388855), (0.5905365347862244, 0.5802738666534424), (0.5201432704925537, 0.45120376348495483)], [(0.4996926188468933, 0.6325620412826538), (0.5940327048301697, 0.5802227854728699), (0.5201398134231567, 0.45112505555152893)], [(0.5003193616867065, 0.6331760883331299), (0.5956369042396545, 0.5801278948783875), (0.5201377272605896, 0.4508187472820282)], [(0.5011351108551025, 0.6332123279571533), (0.5967764854431152, 0.5800918340682983), (0.5202192068099976, 0.4502629339694977)], [(0.5020753145217896, 0.633340060710907), (0.597701907157898, 0.5786975026130676), (0.5221527218818665, 0.44749706983566284)], [(0.5034521818161011, 0.6334124803543091), (0.59757000207901, 0.5735445022583008), (0.5558008551597595, 0.4150393307209015)], [(0.5043197870254517, 0.6334137320518494), (0.5986346006393433, 0.5718089938163757), (0.6136442422866821, 0.4066723585128784)], [(0.5069657564163208, 0.6334171891212463), (0.6035170555114746, 0.5680589079856873), (0.6378751993179321, 0.4053720533847809)], [(0.5091813802719116, 0.6335227489471436), (0.6046320796012878, 0.567492663860321), (0.6790192127227783, 0.4206017255783081)], [(0.5110758543014526, 0.6333065629005432), (0.6090155243873596, 0.5678298473358154), (0.7085548639297485, 0.4618991017341614)], [(0.5117934942245483, 0.6330768465995789), (0.6110885143280029, 0.5680658221244812), (0.7121527791023254, 0.49009302258491516)], [(0.5124119520187378, 0.6330315470695496), (0.6141761541366577, 0.5679834485054016), (0.7167785167694092, 0.4970117509365082)], [(0.5124485492706299, 0.6329757571220398), (0.6160982847213745, 0.5680955648422241), (0.7164346575737, 0.49978122115135193)]]
wave_right_groundtruth = [1.5851508902826286, 1.557449572028618, 1.550176560846745, 1.544990731717327, 1.5674748567248586, 1.8796735599179626, 2.240048392361308, 2.3740028152673798, 2.6447414699695906, 2.914397568819228, 3.0641525962573612, 3.105196455630055, 3.103119389652787]
iter = 0
while cap.isOpened() and iter < 13:
    success, image = cap.read()
    if not success:
        continue

    # Convert the BGR image to RGB, flip the image around y-axis for correct handedness output
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Process the image and draw the pose annotation
    results = pose.process(image)
    #print(type(results))
    #vec1 = results.pose_landmarks.landmark[13].x 
    #vec2 = 
    #print(results.pose_landmarks.landmark[13].x)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
        points = [np.array((results.pose_landmarks.landmark[i].x, results.pose_landmarks.landmark[i].y)) for i in range(11, 16, 2)]
        angle = f.angle(points[0],points[1],points[2])
        if wave_right_groundtruth[iter] - 0.261799 <= angle <= wave_right_groundtruth[iter] + 0.261799:
            print('good')
        else:
            print('you suck')
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        iter += 1
        time.sleep(0.25)

    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

cap.release()
