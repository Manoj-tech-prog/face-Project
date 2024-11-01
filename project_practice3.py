import cv2
import face_recognition

# Load the known image
known_image_path = 'Images/image3.jpg'
known_image = face_recognition.load_image_file(known_image_path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Find face locations in the frame
    face_locations = face_recognition.face_locations(frame)

    # If at least one face is found
    if face_locations:
        # Encode the found face
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

        # Compare the face encoding with the known face encoding
        matches = face_recognition.compare_faces([known_encoding], face_encoding)

        if matches[0]:
            print("Known face detected!")
        else:
            print("Unknown face detected!")

        # Draw rectangles around the detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Live Face Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
