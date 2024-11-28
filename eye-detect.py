import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# Function to calculate eye aspect ratio (EAR)
def calculate_ear(eye_landmarks):
    # Vertical distances
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    # Horizontal distance
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    # EAR formula
    return (A + B) / (2.0 * C)

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    result = face_mesh.process(frame_rgb)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            # Get landmarks for eyes (refer to MediaPipe documentation for indices)
            left_eye_landmarks = [
                face_landmarks.landmark[i] for i in [362, 385, 387, 263, 373, 380]
            ]
            right_eye_landmarks = [
                face_landmarks.landmark[i] for i in [33, 160, 158, 133, 153, 144]
            ]

            # Convert normalized landmarks to pixel coordinates
            h, w, _ = frame.shape
            left_eye = [(int(lm.x * w), int(lm.y * h)) for lm in left_eye_landmarks]
            right_eye = [(int(lm.x * w), int(lm.y * h)) for lm in right_eye_landmarks]

            # Calculate EAR for both eyes
            left_ear = calculate_ear(left_eye)
            right_ear = calculate_ear(right_eye)

            # Average EAR
            ear = (left_ear + right_ear) / 2.0

            # Draw eye landmarks
            for (x, y) in left_eye + right_eye:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            # Determine if eyes are closed (threshold typically ~0.25)
            if ear < 0.25:
                cv2.putText(frame, "Eyes Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Eyes Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Eye Blink Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
