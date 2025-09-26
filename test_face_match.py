import cv2
import numpy as np
from mtcnn import MTCNN
import os
# ------------------------
# Functions (same as in views.py)
# ------------------------
def extract_face_embedding(image_path):
    if not os.path.isfile(image_path):
        print(f"Error: File not found -> {image_path}")
        return None
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image -> {image_path}")
        return None
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    detections = detector.detect_faces(image)
    if len(detections) == 0:
        return None
    x, y, w, h = detections[0]['box']
    x, y = max(0, x), max(0, y)
    face = image[y:y+h, x:x+w]
    face = cv2.resize(face, (160, 160))
    face = face / 255.0
    embedding = face.flatten()
    embedding = embedding / np.linalg.norm(embedding)
    return embedding

def compare_faces(emb1, emb2, threshold=0.6):
    if emb1 is None or emb2 is None:
        return False
    similarity = np.dot(emb1, emb2)
    return similarity > (1 - threshold)

# ------------------------
# Test two images
# ------------------------
image1_path = "media/student_photos/student1.png"   # replace with your test image path
image2_path = "media/student_photos/student.png"   # replace with your test image path

emb1 = extract_face_embedding(image1_path)
emb2 = extract_face_embedding(image2_path)

if emb1 is None:
    print(f"No face detected in {image1_path}")
elif emb2 is None:
    print(f"No face detected in {image2_path}")
elif compare_faces(emb1, emb2):
    print("✅ Match found!")
else:
    print("❌ No match")
