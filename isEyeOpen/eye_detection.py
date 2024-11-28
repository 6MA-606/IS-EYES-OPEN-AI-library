import os
import cv2
import mediapipe as mp
import numpy as np
import sys
import absl.logging

# Suppress TensorFlow and MediaPipe logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings
absl.logging.set_verbosity(absl.logging.ERROR)  # Suppress MediaPipe warnings

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

def calculate_ear(eye_landmarks):
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    return (A + B) / (2.0 * C)

def is_eye_open(image_binary, ear_threshold=0.23):
    # Decode the image from binary data
    image = cv2.imdecode(np.frombuffer(image_binary, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Could not decode image.")

    # Convert to RGB as MediaPipe expects RGB format
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(image_rgb)

    if not result.multi_face_landmarks:
        return "No face detected"

    for face_landmarks in result.multi_face_landmarks:
        # Extract eye landmarks for left and right eyes
        left_eye_landmarks = [
            face_landmarks.landmark[i] for i in [362, 385, 387, 263, 373, 380]
        ]
        right_eye_landmarks = [
            face_landmarks.landmark[i] for i in [33, 160, 158, 133, 153, 144]
        ]

        h, w, _ = image.shape
        left_eye = [(int(lm.x * w), int(lm.y * h)) for lm in left_eye_landmarks]
        right_eye = [(int(lm.x * w), int(lm.y * h)) for lm in right_eye_landmarks]

        # Calculate the Eye Aspect Ratio (EAR) for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Return 'true' if eyes are open, otherwise 'false'
        return "true" if ear >= ear_threshold else "false"

if __name__ == "__main__":
    # Read image data from stdin
    image_binary = sys.stdin.buffer.read()
    # Read EAR threshold from command line
    ear_threshold = float(sys.argv[1]) if len(sys.argv) > 1 else 0.23
    try:
        result = is_eye_open(image_binary, ear_threshold)
        print(result)
    except Exception as e:
        print(f"error: {e}")
