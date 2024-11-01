import dlib
import cv2
import numpy as np

# Load the pre-trained shape predictor model for facial landmarks
shape_predictor_model = "Resources/shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
shape_predictor = dlib.shape_predictor(shape_predictor_model)

# Load the face detection model from Dlib
face_detector = dlib.get_frontal_face_detector()

# Open a connection to the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to RGB (Dlib uses RGB format)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    faces = face_detector(frame_rgb)

    # Iterate over each detected face
    for face in faces:
        # Get facial landmarks using the shape predictor
        landmarks = shape_predictor(frame_rgb, face)

        # Convert the landmarks to a NumPy array
        landmarks_np = np.array([[point.x, point.y] for point in landmarks.parts()])

        # Display the landmarks on the frame
        for point in landmarks_np:
            x, y = point
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    # Display the frame with facial landmarks
    cv2.imshow("Live Face Detection", frame)

    # Break the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
