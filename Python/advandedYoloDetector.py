# Author: Endri Dibra 
# Project: Person Detection and real-time
# inflation for TIAGo Pro robot for Gazebo-RViz simulation

# Importing the required libraries
import cv2
import rclpy
import numpy as np
from rclpy.node import Node
from ultralytics import YOLO
from cv_bridge import CvBridge
from rclpy.parameter import Parameter
from sensor_msgs.msg import Image, LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy


# Defining a class for the object detector
class YoloDetector(Node):

    def __init__(self):
        
        # Initializing the inherited Node class with the name advancedYoloDetector
        super().__init__('advancedYoloDetector')

        # Forcing the node to synchronize with the Gazebo simulation clock
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])

        # Loading the YOLO11n neural network model for object detection
        self.model = YOLO('yolo11n.pt') 
        
        # Initializing the CvBridge tool for converting ROS images to OpenCV
        self.bridge = CvBridge()

        # Defining the Quality of Service settings for reliable data delivery
        qos_profile = QoSProfile(

            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
            durability=DurabilityPolicy.VOLATILE
        )

        # Subscribing to the head camera RGB topic for visual processing
        self.create_subscription(

            Image, '/head_front_camera/rgb/image_raw', self.image_callback, qos_profile)
        
        # Subscribing to the depth camera topic for measuring spatial distance
        self.create_subscription(

            Image, '/head_front_camera/depth/image_raw', self.depth_callback, qos_profile)

        # Advertising the virtual laser scan topic to the navigation costmap
        self.scan_pub = self.create_publisher(LaserScan, '/human_detection_scan', qos_profile)

        # Initializing the depth frame variable to store the incoming data
        self.last_depth_frame = None
        
        # Logging an informational message confirming the detector is starting
        self.get_logger().info('The Advanced Vision Detector has Started! Synchronized with Gazebo Clock.')

    def depth_callback(self, msg):
        
        # Converting the ROS depth message into a floating-point NumPy array
        self.last_depth_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='32FC1')

    def image_callback(self, msg):
        
        # Checking if the depth frame is missing before proceeding
        if self.last_depth_frame is None:
        
            return

        try:
        
            # Converting the ROS RGB image into an OpenCV BGR format
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            
            # Running the YOLO model to detect only people with high confidence
            results = self.model.predict(cv_image, conf=0.6, classes=[0], verbose=False)

            # Iterating through every result returned by the model
            for result in results:
        
                # Processing each individual bounding box found in the image
                for box in result.boxes:
        
                    # Extracting the box coordinates and converting them to integers
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Calculating the center pixel coordinates of the detected person
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    # Sampling the distance in meters from the stored depth map
                    distance = self.last_depth_frame[cy, cx]

                    # Validating that the distance is a real number and within range
                    if not np.isnan(distance) and 0.4 < distance < 6.0:
        
                        # Getting the total width of the image for angle calculation
                        img_width = cv_image.shape[1]
                        
                        # Calculating the horizontal angle relative to the center of view
                        angle = -((cx / img_width) - 0.5) * 1.0 
                        
                        # Calling the function to publish the virtual laser points
                        self.publish_virtual_scan(distance, angle)
                        
                        # Reporting the detected person and injection status to the console
                        self.get_logger().info(f"PERSON DETECTED at {distance:.2f}m. Injecting to costmap!")

            # Plotting the detection boxes onto the original image frame
            annotated_frame = results[0].plot()
            
            # Rendering the annotated frame in a local OpenCV window
            cv2.imshow("TIAGo Advanced YOLO Detector", annotated_frame)
            
            # Refreshing the window and waiting for 1 millisecond
            cv2.waitKey(1)

        except Exception as e:
        
            # Catching and logging any errors occurring during the image processing
            self.get_logger().error(f'Processing Error: {str(e)}')

    def publish_virtual_scan(self, dist, angle):
        
        # Creating a new LaserScan message object
        scan = LaserScan()
        
        # Stamping the message with the current simulation time
        scan.header.stamp = self.get_clock().now().to_msg()
        
        # Linking the scan data to the robot's base coordinate frame
        scan.header.frame_id = 'base_link'
        
        # Defining the starting angle of the virtual laser slice
        scan.angle_min = angle - 0.05
        
        # Defining the ending angle of the virtual laser slice
        scan.angle_max = angle + 0.05
        
        # Setting the resolution between each laser point in the slice
        scan.angle_increment = 0.01
        
        # Specifying the minimum sensing distance for the laser message
        scan.range_min = 0.1
        
        # Specifying the maximum sensing distance for the laser message
        scan.range_max = 10.0
        
        # Calculating the total number of points based on the angle settings
        num_points = int((scan.angle_max - scan.angle_min) / scan.angle_increment)
        
        # Generating a list of range values representing the distance to the person
        scan.ranges = [float(dist)] * num_points 
        
        # Transmitting the completed laser scan message to the network
        self.scan_pub.publish(scan)

def main(args=None):
    
    # Initializing the rclpy library for ROS 2 communication
    rclpy.init(args=args)
    
    # Creating an instance of the YoloDetector node
    node = YoloDetector()
    
    try:
    
        # Spinning the node to keep it responsive and processing callbacks
        rclpy.spin(node)
    
    except KeyboardInterrupt:
    
        # Allowing the program to exit cleanly when the user presses Ctrl+C
        pass
    
    finally:
    
        # Destroying the visual windows created by OpenCV
        cv2.destroyAllWindows()
        
        # Properly shutting down the ROS node
        node.destroy_node()
        
        # Finalizing the rclpy communication system
        rclpy.shutdown()

# Running the main function
if __name__ == '__main__':
   
    # Starting the main entry point of the script
    main()
