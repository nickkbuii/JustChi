# JustChi

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
![TreeHacks10](https://img.shields.io/badge/event-TreeHacks-8C1515)

A pose-tracking VR application built with Meta Quest 2 for interactive Tai Chi learning. TreeHacks 2024.

![image](https://github.com/nickkbuii/JustChi/blob/main/demo.png)

## Inspiration
The idea behind JustChi stemmed from a desire to improve the physical and mental well-being of seniors through accessible and engaging technology. Since everyone on the team has a relative who would benefit from the gentle exercise that is Tai Chi, we thought it would be a wonderful idea to prototype a futuristic VR game targeting the growing senior population. By combining the ancient practice of Tai Chi, known for its health benefits such as improved balance, flexibility, and stress reduction, with modern Virtual Reality (VR) and Computer Vision technology, JustChi aims to provide a unique and immersive experience that is both beneficial and enjoyable for its users.

## What it does
Think "Just Dance" but instead of high-intensity dance, our users are immersed in relaxing and peaceful VR environments where they can engage in the ancient Chinese art of Tai Chi. Once set up on the Meta Quest 2, our users can select from a variety of Tai Chi styles and soothing background environments. They are then sent to these environments where they can follow along with our prerecorded Tai Chi "master" through a game-like experience. Along the way, we provide supportive feedback and calculate the accuracy of their moves, using it to display their Tai Chi score in real-time. Through Just Chi, anyone can learn Tai Chi and reap a myriad of health benefits while being educated on ancient Chinese culture.

## How we built it
We used an open-source computer vision framework called MediaPipe to determine our user's pose by tracking keypoints (and their coordinates) displayed along the user's body, storing and transmitting these coordinates through a Flask server. We then ran these coordinates through our pose comparison Python algorithm, which compares the coordinates of the user's keypoints with the keypoints of our Tai Chi "master" using linear algebra techniques. Then, we used Figma, HTML, CSS, JavaScript, and a VR development framework called A-Frame to design our VR UI/UX and environment that is displayed to the user through the Meta Quest headset.

## Installation
Requirements: 
* Python (3.11.4)
* mediapipe (0.8.9.1)
* Flask-SocketIO (5.3.6)
* opencv-python (4.5.5.61)
* numpy (1.26.4)

Installation steps:
1. Clone the repository
```
$ git clone https://github.com/nickkbuii/JustChi.git
```
2. Connect host and Meta Quest 2 to a local network
4. Run the `app.py`file
```
$ python app.py
```
5. Open server address on browser in Meta Quest 2 

## Our Team
* Rally Lin (rally.lin@duke.edu)
* Daniel Yang (dy5251@princeton.edu)
* Alex Tong (alextong1010@berkeley.edu)
* Nick Bui (nicholasqbui@berkeley.edu)
