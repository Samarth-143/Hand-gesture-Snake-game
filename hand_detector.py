import cv2
import math
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

class HandDetector:
    def __init__(self):
        # Download the hand_landmarker.task model if not present
        import os
        import urllib.request
        self.model_path = 'hand_landmarker.task'
        if not os.path.exists(self.model_path):
            print('Downloading hand_landmarker.task model...')
            url = 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task'
            urllib.request.urlretrieve(url, self.model_path)

        base_options = mp_python.BaseOptions(model_asset_path=self.model_path)
        options = mp_vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5)
        self.detector = mp_vision.HandLandmarker.create_from_options(options)
        self.results = None
        self.last_landmarks = None

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        from mediapipe.tasks.python.vision.core.image import Image as MPImage
        mp_image = MPImage(image_format=1, data=img_rgb)
        self.results = self.detector.detect(mp_image)
        self.last_landmarks = None
        if self.results.hand_landmarks:
            self.last_landmarks = self.results.hand_landmarks[0]
            if draw:
                for lm in self.last_landmarks:
                    cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)
        return img

    def find_position(self, img):
        landmark_list = []
        if self.last_landmarks:
            h, w, c = img.shape
            for id, lm in enumerate(self.last_landmarks):
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark_list.append([id, cx, cy])
        return landmark_list

    def get_hand_direction(self, img):
        landmark_list = self.find_position(img)
        if len(landmark_list) == 0:
            return None
        wrist = landmark_list[0]  # id 0
        thumb_tip = landmark_list[4]  # id 4 is thumb tip in MediaPipe
        dx = thumb_tip[1] - wrist[1]
        dy = thumb_tip[2] - wrist[2]
        angle = math.degrees(math.atan2(dy, dx))
        if -45 <= angle < 45:
            return 'RIGHT'
        elif 45 <= angle < 135:
            return 'DOWN'
        elif angle >= 135 or angle < -135:
            return 'LEFT'
        elif -135 <= angle < -45:
            return 'UP'
        return None
