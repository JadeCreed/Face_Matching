# matches/recognizer.py
import pickle
import numpy as np
import os

def recognize_face(image_encoding):
    """
    Compare a single face encoding (from uploaded image) against known encodings.
    Returns the matched student ID or None if no match.
    
    Parameters:
        image_encoding (np.ndarray): 128-d face encoding vector.
    """
    encodings_file = os.path.join(os.path.dirname(__file__), "encodings.pkl")
    if not os.path.exists(encodings_file):
        return None  # No trained data yet

    # Load known encodings and corresponding student IDs
    with open(encodings_file, "rb") as f:
        known_encodings, known_ids = pickle.load(f)

    # Compute distances
    distances = np.linalg.norm(known_encodings - image_encoding, axis=1)
    if len(distances) == 0:
        return None

    # Find closest match
    min_idx = np.argmin(distances)
    if distances[min_idx] < 0.5:  # threshold for match
        return known_ids[min_idx]

    return None
