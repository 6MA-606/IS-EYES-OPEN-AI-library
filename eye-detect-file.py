import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Function to calculate eye aspect ratio (EAR)
def calculate_ear(eye_landmarks):
    A = np.linalg.norm(np.array(eye_landmarks[1]) - np.array(eye_landmarks[5]))
    B = np.linalg.norm(np.array(eye_landmarks[2]) - np.array(eye_landmarks[4]))
    C = np.linalg.norm(np.array(eye_landmarks[0]) - np.array(eye_landmarks[3]))
    return (A + B) / (2.0 * C)

# Function to process a single image
def process_image(image_path):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return None
    
    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image with MediaPipe
    result = face_mesh.process(image_rgb)
    
    if not result.multi_face_landmarks:
        print("No face detected in the image.")
        return None

    for face_landmarks in result.multi_face_landmarks:
        # Get landmarks for both eyes
        left_eye_landmarks = [
            face_landmarks.landmark[i] for i in [362, 385, 387, 263, 373, 380]
        ]
        right_eye_landmarks = [
            face_landmarks.landmark[i] for i in [33, 160, 158, 133, 153, 144]
        ]

        # Convert normalized landmarks to pixel coordinates
        h, w, _ = image.shape
        left_eye = [(int(lm.x * w), int(lm.y * h)) for lm in left_eye_landmarks]
        right_eye = [(int(lm.x * w), int(lm.y * h)) for lm in right_eye_landmarks]

        # Calculate EAR for both eyes
        left_ear = calculate_ear(left_eye)
        right_ear = calculate_ear(right_eye)
        ear = (left_ear + right_ear) / 2.0

        # Determine if eyes are closed
        result_text = "Eyes Closed" if ear < 0.25 else "Eyes Open"

        # Draw landmarks and annotate result on the image
        for (x, y) in left_eye + right_eye:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

        cv2.putText(image, result_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if ear >= 0.25 else (0, 0, 255), 2)

    # Save the processed image
    output_path = "output_image.jpg"
    cv2.imwrite(output_path, image)
    print(f"Processed image saved as {output_path}")
    return result_text

# Example usage
image_path = "input_image.jpg"  # Replace with your image file path
result = process_image(image_path)
if result:
    print(f"Result: {result}")
