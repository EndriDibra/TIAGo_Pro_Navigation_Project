# Author: Endri Dibra 
# Project: This is a task for object detection and recognition on gazebo environment for the TIAGo Pro robot to detect obstacles such as, people, chairs, tables, using YOLOv11n AI model

# Importing rclpy for ROS2 functionality 
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# Importing QoS modules for connection reliability
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# Importing CvBridge for image conversion
from cv_bridge import CvBridge

# Importing cv2 for computer vision tasks
import cv2

# Importing YOLO from ultralytics for object detection
from ultralytics import YOLO

# Defining the YoloDetector class inheriting from Node
class YoloDetector(Node):

    # Initializing the class instance
    def __init__(self):

        # Calling the parent class constructor
        super().__init__('yoloDetector')

        # Loading the standard YOLO11n model

        self.model = YOLO('yolo11n.pt') 

        # Initializing the CvBridge instance
        self.bridge = CvBridge()

        # Defining the Reliable QoS Profile for TIAGo camera
        qos_profile = QoSProfile(

            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            durability=DurabilityPolicy.VOLATILE
        )

        # Subscribing to the verified TIAGo RGB camera topic
        self.subscription = self.create_subscription(

            Image,
            '/head_front_camera/rgb/image_raw', 
            self.image_callback,
            qos_profile
        )

        # Logging the start of the detector node
        self.get_logger().info('YOLO11n Detector Started. Searching for all objects.')

    # Defining the callback function for processing images
    def image_callback(self, msg):

        # Starting the try block for error handling
        try:

            # Converting ROS images to OpenCV BGR format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Predicting all objects with 0.5 confidence
            results = self.model.predict(cv_image, conf=0.5, verbose=False)

            # Extracting all detected objects from the first result
            boxes = results[0].boxes

            # Checking if any objects were found
            if len(boxes) > 0:

                # Creating a dictionary to count each object type
                counts = {}

                for box in boxes:

                    # Getting the class ID and converting it to a name
                    class_id = int(box.cls[0])
                    label = self.model.names[class_id]

                    # Incrementing the count for this specific label
                    counts[label] = counts.get(label, 0) + 1 
                
                # Formatting the counts into a readable string
                detection_str = ", ".join([f"{count} {label}(s)" for label, count in counts.items()])

                # Logging the specific objects detected
                self.get_logger().info(f"DETECTION: {detection_str} found!")

            # Plotting the annotated results on the frame
            annotated_frame = results[0].plot()

            # Showing the detection frame in a window
            cv2.imshow("YOLO11 TIAGo Detection", annotated_frame)

            # Waiting for a short delay to refresh the window
            cv2.waitKey(1)

        # Catching exceptions during processing
        except Exception as e:

            # Logging the error message to the console
            self.get_logger().error(f'Error processing image: {str(e)}')

# Defining the main entry point function
def main(args=None):

    # Initializing the rclpy library
    rclpy.init(args=args)

    # Creating an instance of the YoloDetector node
    node = YoloDetector()

    # Starting the try block for running the node
    try:

        # Spinning the node to keep it active
        rclpy.spin(node)

    # Catching keyboard interrupt signals
    except KeyboardInterrupt:

        pass

    # Starting the finally block for cleanup
    finally:

        # Destroying all OpenCV windows
        cv2.destroyAllWindows()

        # Destroying the ROS2 node instance
        node.destroy_node()

        # Shutting down the rclpy library
        rclpy.shutdown()

# Running the main function
if __name__ == '__main__':

    main()
