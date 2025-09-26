import os
import pickle
import numpy as np

# Example: you must already have 128-d vectors for each student
# Replace this with your actual face encoding extraction process
# For demo purposes, let's assume you already have the encodings

known_encodings = []
known_ids = []

# Loop through all student images
media_dir = "media/student_photos"
for filename in os.listdir(media_dir):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        student_id = filename.split(".")[0]  # use filename as ID
        # For demonstration, use a random vector (replace with real encoding)
        encoding = np.random.rand(128)
        known_encodings.append(encoding)
        known_ids.append(student_id)

# Save encodings to file
with open("matches/encodings.pkl", "wb") as f:
    pickle.dump((np.array(known_encodings), known_ids), f)

print("encodings.pkl generated!")
