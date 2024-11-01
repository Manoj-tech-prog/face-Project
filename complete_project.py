import cv2
import numpy as np
import psycopg2
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

# Retrieve image data from PostgreSQL
def retrieve_image_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT image_name, image_data FROM faces")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except psycopg2.Error as error:
        print("Error retrieving image data:", error)
        return []

# Compare images
def compare_images(image1, image2):
    img1 = cv2.imdecode(np.frombuffer(image1, np.uint8), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imdecode(np.frombuffer(image2, np.uint8), cv2.IMREAD_GRAYSCALE)
    # Use another method for image comparison here
    # Example: Mean Squared Error (MSE)
    mse = np.mean((img1 - img2) ** 2)
    return mse

# View captured image
def view_captured_image(image_data):
    img_array = np.frombuffer(image_data, dtype=np.uint8)
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    cv2.imshow('Captured Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
    live_image_data = encoded_image.tobytes()

    # Store image data in PostgreSQL
    image_name = "captured_image.jpg"
    store_image_data(connection, image_name, live_image_data)
    print("Image stored successfully.")

    # View captured image
    view_captured_image(live_image_data)

    # Release the video capture
    video_capture.release()

    # Close the PostgreSQL connection
    connection.close()
