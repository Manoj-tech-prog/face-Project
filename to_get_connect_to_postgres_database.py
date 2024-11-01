import cv2
import face_recognition
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
# Connect to PostgreSQL database
conn = psycopg2.connect(
    hostname=os.getenv('DB_HOST'),
    username = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS faces (
        id SERIAL PRIMARY KEY,
        name TEXT,
        encoding TEXT
    )
""")
conn.commit()

# Load known faces and their encodings from database
known_face_encodings = []
known_face_names = []

cursor.execute("SELECT name, encoding FROM faces")
for name, encoding in cursor.fetchall():
    known_face_names.append(name)
    known_face_encodings.append(eval(encoding))

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, assign the name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Display the name and rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
