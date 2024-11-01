# Face Recognition and Detection System

This project is a **Face Recognition and Detection System** designed to detect and recognize faces in real-time. It utilizes a combination of computer vision and image processing libraries to accurately identify faces, allowing for real-time comparisons and database-based face recognition.

## Features

- **Real-Time Face Detection** using OpenCV for capturing live video frames and processing images.
- **Facial Landmark Detection** with Dlib for improved facial recognition accuracy.
- **Database Integration** with PostgreSQL to store and retrieve facial data, allowing comparisons with saved faces.
- **Environment Variable Management** with Python-dotenv for secure handling of sensitive information.
- **Data Visualization** using Matplotlib for displaying images, plots, or analysis.

## Technology Stack

- **Computer Vision**: OpenCV (`opencv-python`)
- **Facial Landmark Detection**: Dlib (`dlib`)
- **Image Processing**: Numpy, Scikit-Image, Pillow
- **Data Visualization**: Matplotlib
- **Database**: PostgreSQL with Psycopg2
- **Dependency Management**: CMake for building Dlib and other dependencies

## Installation

### Prerequisites
1. **Python**: Install Python (version 3.8 or above).
2. **Database**: PostgreSQL installed and configured.
3. **Face Models**: Ensure any required face models are available.

### Dependency Installation

Install the necessary dependencies listed in `requirements.txt`:

```bash
pip install opencv-python~=4.10.0.84 numpy~=2.0.1 setuptools~=69.0.3 matplotlib~=3.8.2 scikit-image~=0.22.0 psycopg2~=2.9.9 dlib~=19.24.2 Pillow~=10.1.0 python-dotenv~=1.0.1 cmake~=3.30.2
