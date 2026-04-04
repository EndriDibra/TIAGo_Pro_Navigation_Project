# Author: Endri Dibra
# Project: This is a task for general object detection and recognition using YOLOv11n AI model

# Importing the required libraries
import cv2 
from ultralytics import YOLO

# Using the default camera of the computer system
camera = cv2.VideoCapture(0)

# Loading the YOLOv11n model for
# object detection and recognition
model = YOLO("yolo11n-pose.pt")

# Checking if the camera is working
if not camera:

    print("Error! Camera did not open.")

    exit()

# Looping through camera frames for online streaming
while camera.isOpened():

    # Reading each camera frame
    success, frame = camera.read()

    # Checking if the camera works
    # during the online streaming
    if not success:

        print("Error! Camera stopped.")

        break

    # Applying YOLOv11n on each camera frame
    # for online object detection and recognition
    yolo_Frame = model(frame, save=False)

    # Plotting around each detected
    # object the bounding boxes 
    yolo_Frame = yolo_Frame[0].plot()

    # Displaying the video with the process
    cv2.imshow("Video Display", yolo_Frame)

    # Terminating the process by pressing letter "q"
    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

# Releasing camera and windows resources
camera.release()
cv2.destroyAllWindows() 
