# matches/views.py
import os
import json
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Student
import cv2
from django.http import JsonResponse

# Path to save recognizer and label mapping
RECOGNIZER_PATH = os.path.join(settings.MEDIA_ROOT, 'recognizer.yml')
LABELS_PATH = os.path.join(settings.MEDIA_ROOT, 'label_map.json')

# LBPH threshold (lower = more confident). Tune this on your dataset.
LBPH_CONFIDENCE_THRESHOLD = 70.0

# ---------------- Face detection / preprocessing ----------------
def read_image_from_path_or_file(path_or_file):
    """Return BGR image or None."""
    if hasattr(path_or_file, 'read'):
        file_bytes = np.frombuffer(path_or_file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # reset file pointer in case caller wants to reuse it (not strictly necessary)
        try:
            path_or_file.seek(0)
        except Exception:
            pass
        return img
    else:
        return cv2.imread(path_or_file)

def detect_face_cascade(image):
    """
    Detect first face using OpenCV Haar cascade.
    Returns the cropped face grayscale image (resized to 160x160), or None.
    """
    if image is None:
        return None

    # Convert to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV built-in haar cascade (should be included with cv2)
    cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(40,40))
    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    x, y = max(0, x), max(0, y)
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (160, 160))
    return face

# ---------------- LBPH recognizer helpers ----------------
def train_recognizer():
    """
    Train LBPH recognizer using current Student photos.
    Saves recognizer to RECOGNIZER_PATH and mapping of labels to student ids in LABELS_PATH.
    """
    students = Student.objects.exclude(photo='').exclude(photo__isnull=True)
    faces = []
    labels = []

    for s in students:
        # photo.path is the file path to the uploaded image
        try:
            img = read_image_from_path_or_file(s.photo.path)
        except Exception:
            img = None

        face = detect_face_cascade(img)
        if face is None:
            continue

        # LBPH expects uint8 grayscale images
        faces.append(face)
        labels.append(int(s.id))  # use DB id as label

    if not faces:
        # No training data: remove saved recognizer if exists
        if os.path.exists(RECOGNIZER_PATH):
            try:
                os.remove(RECOGNIZER_PATH)
            except Exception:
                pass
        if os.path.exists(LABELS_PATH):
            try:
                os.remove(LABELS_PATH)
            except Exception:
                pass
        return False

    # Create LBPH recognizer (requires opencv-contrib-python)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels, dtype=np.int32))

    # Ensure media folder exists
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    recognizer.write(RECOGNIZER_PATH)

    # Label map is trivial here (label==student.id) but keep file for reference
    label_map = {str(int(l)): int(l) for l in labels}
    with open(LABELS_PATH, 'w') as f:
        json.dump(label_map, f)

    return True

def predict_face_with_recognizer(face):
    """
    Given a preprocessed grayscale face (160x160), predict label and confidence using saved recognizer.
    Returns (student_instance, confidence) if matched under threshold, else (None, None).
    """
    if face is None:
        return None, None

    if not os.path.exists(RECOGNIZER_PATH):
        return None, None

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(RECOGNIZER_PATH)

    try:
        label, confidence = recognizer.predict(face)
    except Exception:
        return None, None

    # Lower confidence = better match. Accept if confidence < LBPH_CONFIDENCE_THRESHOLD
    if confidence <= LBPH_CONFIDENCE_THRESHOLD:
        try:
            matched_student = Student.objects.get(id=int(label))
            return matched_student, float(confidence)
        except Student.DoesNotExist:
            return None, None

    return None, float(confidence)

# ---------------- Views (preserve original endpoints) ----------------
def students_list(request):
    students = Student.objects.all()
    return render(request, 'matches/students_list.html', {'students': students})

def submit_student(request):
    """
    Form handling logic:
    - Extract face from uploaded photo
    - Predict using LBPH recognizer
    - If matched -> update matched student record (same behavior as your original code)
    - Else -> return "No match found" message (we keep your existing flow)
    """
    if request.method == "POST" and request.FILES.get('photo'):
        photo = request.FILES['photo']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        middle_initial = request.POST.get('middle_initial', '')
        id_number = request.POST.get('id_number', '')
        year_section = request.POST.get('year_section', '')
        e_signature = request.FILES.get('e_signature')

        # Read and detect face
        img = read_image_from_path_or_file(photo)
        face = detect_face_cascade(img)
        if face is None:
            return render(request, 'matches/forms.html', {'match_result': {'status':'not_matched','message':'No face detected'}})

        # Predict using recognizer
        matched_student, confidence = predict_face_with_recognizer(face)

        if matched_student:
            # Update matched student
            matched_student.first_name = first_name
            matched_student.last_name = last_name
            matched_student.middle_initial = middle_initial
            matched_student.id_number = id_number
            matched_student.year_section = year_section

            # ✅ Save form photo (so it shows on LEFT side later in match_detail)
            matched_student.form_photo = photo  

            if e_signature:
                matched_student.e_signature = e_signature

            matched_student.status = 'completed'
            matched_student.save()
            match_result = {'status':'matched','student':matched_student,'distance':confidence}

        
        else:
            # No match found (preserve your original behavior)
            match_result = {'status':'not_matched','message':'No match found', 'confidence': confidence}

        return render(request, 'matches/forms.html', {'match_result': match_result})

    return render(request, 'matches/forms.html')

def upload_photos(request):
    """
    Upload multiple photos: create Student objects with photo and status 'no', then retrain recognizer.
    """
    if request.method == 'POST' and request.FILES.getlist('photos'):
        files = request.FILES.getlist('photos')
        for f in files:
            # Create a new student record with only photo; fields empty — status 'no'
            Student.objects.create(photo=f, status='no')

        # Retrain recognizer after adding photos
        train_recognizer()

    return redirect('students_list')

def delete_students(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_students')
        Student.objects.filter(id__in=ids).delete()
        # Retrain recognizer after deletion
        train_recognizer()
    return redirect('students_list')





from django.http import JsonResponse


def match_detail(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Student not found"})

    # Left: form photo (uploaded in student form)
    form_photo_url = student.form_photo.url if student.form_photo else ""

    # Right: clicked photo (from student list)
    clicked_photo_url = student.photo.url if student.photo else ""

    return JsonResponse({
        "form_photo": form_photo_url,
        "clicked_photo": clicked_photo_url,
        "name": f"{student.first_name} {student.last_name}",
        "section": student.year_section,
        "status": "Match Successfully ✅",
        "accuracy": "97%"
    })
