# matches/recognizer.py
import face_recognition
import pickle
import numpy as np
import os
from .models import Student

def recognize_face(image_path):
    encodings_file = os.path.join(os.path.dirname(__file__), "encodings.pkl")
    if not os.path.exists(encodings_file):
        return None  # No trained data yet

    with open(encodings_file, "rb") as f:
        known_encodings, known_ids = pickle.load(f)

    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encodings = face_recognition.face_encodings(unknown_image)
    if not unknown_encodings:
        return None

    unknown_encoding = unknown_encodings[0]
    distances = face_recognition.face_distance(known_encodings, unknown_encoding)
    if len(distances) == 0:
        return None

    min_idx = np.argmin(distances)
    if distances[min_idx] < 0.5:
        return known_ids[min_idx]

    return None
