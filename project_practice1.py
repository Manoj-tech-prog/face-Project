import dlib
import cv2
import numpy as np

# Load the pre-trained shape predictor model for facial landmarks
shape_predictor_model = "Resources/shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat"
shape_predictor = dlib.shape_predictor(shape_predictor_model)

# Load the pre-trained face recognition model
face_recognition_model = "resources1/dlib_face_recognition.dat/dlib_face_recognition.dat"
face_recognizer = dlib.face_recognition_model_v1(face_recognition_model)

# Load the face detection model from Dlib
face_detector = dlib.get_frontal_face_detector()

# Load the image
image_path = "Images/image.png.png"
img = cv2.imread(image_path)

# Convert the image to RGB (Dlib uses RGB format)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Detect faces in the image
faces = face_detector(img_rgb)

# Iterate over each detected face
for face in faces:
    # Get facial landmarks using the shape predictor
    landmarks = shape_predictor(img_rgb, face)

    # Convert the landmarks to a NumPy array
    landmarks_np = np.array([[point.x, point.y] for point in landmarks.parts()])

    # Display the landmarks on the image
    for point in landmarks_np:
        x, y = point
        cv2.circle(img, (x, y), 2, (0, 255, 0), -1)

# Display the image with facial landmarks
cv2.imshow("Face Recognition", img)
cv2.waitKey(0)
cv2.destroyAllWindows()


