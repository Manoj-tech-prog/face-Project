import cv2
import os

# Construct the path to the Haarcascades XML file
haarcascades_path = os.path.join('resources2/opencv-4.x/opencv-4.x/data/haarcascades_cuda/haarcascade_frontalface_default.xml')

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(haarcascades_path)

# Function to detect faces in an image
def detect_faces(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return image

# Capture a single frame
cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Detect faces in the captured frame
    frame_with_faces = detect_faces(frame)

    # Display the frame with faces
    cv2.imshow('Live Face Detection', frame_with_faces)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()

# Destroy all OpenCV windows
cv2.destroyAllWindows()
