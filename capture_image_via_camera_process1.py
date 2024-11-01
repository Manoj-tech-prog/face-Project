import cv2
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
import numpy as np
from psycopg2 import sql

# Connect to PostgreSQL<!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Face Recognition and Detection</title>
#     <!-- Include Face-API.js library -->
#     <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs"></script>
#     <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/face-landmarks-detection"></script>
#     <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/face-expression-recognition"></script>
#     <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/face-api"></script>
# </head>
# <body>
#     <h1>Face Recognition and Detection</h1>
#     <video id="video" width="640" height="480" autoplay></video>
#     <canvas id="canvas" width="640" height="480"></canvas>
#
#     <script>
#         // Load the face-api models
#         Promise.all([
#             faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
#             faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
#             faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
#             faceapi.nets.faceExpressionNet.loadFromUri('/models')
#         ]).then(startVideo)
#
#         async function startVideo() {
#             const video = document.getElementById('video');
#             navigator.getUserMedia(
#                 { video: {} },
#                 stream => video.srcObject = stream,
#                 err => console.error(err)
#             )
#         }
#
#         // Perform face detection and recognition
#         video.addEventListener('play', () => {
#             const canvas = faceapi.createCanvasFromMedia(video);
#             document.body.append(canvas);
#             const displaySize = { width: video.width, height: video.height };
#             faceapi.matchDimensions(canvas, displaySize);
#             setInterval(async () => {
#                 const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors();
#                 const resizedDetections = faceapi.resizeResults(detections, displaySize);
#                 canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
#                 faceapi.draw.drawDetections(canvas, resizedDetections);
#                 faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
#                 resizedDetections.forEach(detection => {
#                     const box = detection.detection.box;
#                     const drawBox = new faceapi.draw.DrawBox(box, { label: 'Face' });
#                     drawBox.draw(canvas);
#                 });
#             }, 100);
#         });
#     </script>
# </body>
# </html>
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

# Create table in PostgreSQL
def create_table(connection):

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faces (
                id SERIAL PRIMARY KEY,
                image_name VARCHAR(255),
                image_data BYTEA
            )
        """)
        cursor.close()
    except psycopg2.Error as error:
        print("Error creating table:", error)

# Store image data in PostgreSQL
def store_image_data(connection, image_name, image_data):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO faces (image_name, image_data)
            VALUES (%s, %s)
        """, (image_name, psycopg2.Binary(image_data)))
        cursor.close()
        print("Image data stored successfully.")
    except psycopg2.Error as error:
        print("Error storing image data:", error)

if __name__ == "__main__":
    # Connect to PostgreSQL
    connection = connect_to_postgresql()
    if connection is None:
        exit()

    # Create table in PostgreSQL
    create_table(connection)

    # Capture image from webcam
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()

    # Encode captured image as JPEG format
    _, encoded_image = cv2.imencode('.jpg', frame)
    image_data = encoded_image.tobytes()

    # Store image data in PostgreSQL
    image_name = "captured_image.jpg"
    store_image_data(connection, image_name, image_data)

    # Release the video capture
    video_capture.release()

    # Close the PostgreSQL connection
    connection.close()
