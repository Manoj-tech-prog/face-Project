import cv2
import face_recognition
import psycopg2
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to PostgreSQL
def connect_to_postgresql():
    hostname = os.getenv('DB_HOST')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    database = os.getenv('DB_NAME')

    try:
        connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )
        connection.autocommit = True
        return connection
    except psycopg2.Error as error:
        print("Error connecting to PostgreSQL:", error)
        return None

# Load known face encodings and names from the database
def load_known_faces_from_database():
    connection = connect_to_postgresql()
    if connection is None:
        return None, None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT name, face_encoding FROM faces")
        rows = cursor.fetchall()
        names = []
        face_encodings = []

        for row in rows:
            names.append(row[0])
            face_encodings.append(np.frombuffer(row[1], dtype=np.float64))

        cursor.close()
        connection.close()
        return names, face_encodings
    except psycopg2.Error as error:
        print("Error loading known faces from database:", error)
        return None, None

# Add face encoding and name to the database
def add_face_to_database(name, face_encoding):
    connection = connect_to_postgresql()
    if connection is None:
        return

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO faces (name, face_encoding) VALUES (%s, %s)", (name, face_encoding.tobytes()))
        cursor.close()
        connection.close()
    except psycopg2.Error as error:
        print("Error adding face to database:", error)

# Capture video from webcam
video_capture = cv2.VideoCapture(0)

# Load known faces from database
known_face_names, known_face_encodings = load_known_faces_from_database()

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face found in the frame
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, use the name of the known face
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
