import cv2
import psycopg2
from psycopg2 import sql
import numpy as np
from PIL import Image
from io import BytesIO
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

# Retrieve image data from PostgreSQL
def retrieve_image_data(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT image_name, image_data FROM faces")
        return cursor.fetchall()
    except psycopg2.Error as error:
        print("Error retrieving image data:", error)
        return None

if __name__ == "__main__":
    # Connect to PostgreSQL
    connection = connect_to_postgresql()
    if connection is None:
        exit()

    # Retrieve image data from PostgreSQL
    image_records = retrieve_image_data(connection)

    if image_records:
        # Iterate through retrieved images
        for image_record in image_records:
            image_name, image_data = image_record

            # Decode image dataq
            image_buffer = BytesIO(image_data)
            pil_image = Image.open(image_buffer)
            cv_image = np.array(pil_image)

            # Display image using OpenCV
            cv2.imshow(image_name, cv_image)
            cv2.waitKey(0)  # Wait for any key press to close the window

    # Close the PostgreSQL connection
    connection.close()
