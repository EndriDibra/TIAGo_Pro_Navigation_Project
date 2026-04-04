# Importing the required libraries
import cv2 
from ultralytics import YOLO


camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

model = YOLO("yolo11n-pose.pt")

if not camera:

    print("Error! Camera did not open.")

    exit()

while camera.isOpened():

    success, frame = camera.read()

    if not success:

        print("Error! Camera stopped.")

        break

    yolo_frame = model(frame, save=False)

    yolo_frame = yolo_frame[0].plot()

    cv2.imshow("Video Display", yolo_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break

camera.release()
cv2.destroyAllWindows() 
