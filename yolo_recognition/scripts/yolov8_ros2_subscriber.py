#!/usr/bin/env python3

import cv2
import threading 
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor, SingleThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import time
from yolov8_msgs.msg import Yolov8Inference

bridge = CvBridge()

# class Camera_subscriber(Node):
    
#   def __init__(self):
#       super().__init__('camera_subscriber')

#       self.subscription = self.create_subscription(
#           Image,
#           'camera/color/image_raw',
#           self.camera_callback,
#           10)
#       self.subscription

#   def camera_callback(self, data):
#       global img
#       img = bridge.imgmsg_to_cv2(data, "bgr8")

class Yolo_subscriber(Node):

    def __init__(self):
        super().__init__('yolo_subscriber')

        self.subscription = self.create_subscription(
            Yolov8Inference,
            '/Yolov8_Inference',
            self.yolo_callback,
            10)
        self.subscription

        # self.timer = self.create_timer(1.0, self.timer_callback)

        self.class_name = None
        self.top = None 
        self.left = None
        self.bottom = None
        self.right = None

        self.last_leg_detected = 0.0
        self.leg_detected = False


        # self.img_pub = self.create_publisher(Image, "/inference_result_cv2", 1)

    def yolo_callback(self, data):
        # global img
        # self.get_logger().info(str(data.yolov8_inference.class_name))
        for r in data.yolov8_inference:
            self.class_name = r.class_name
            self.top = r.top
            self.left = r.left
            self.bottom = r.bottom
            self.right = r.right

            if self.class_name == "leg" and self.leg_detected == False:
                time.sleep(3)
                self.leg_detected = True
                self.last_leg_detected == time.time()
                self.get_logger().info(f"{self.class_name} is detected")

            elif self.class_name != "leg" and self.leg_detected == True:
                self.leg_detected = False
                # self.get_logger().infor()
            # cv2.rectangle(img, (top, left), (bottom, right), (255, 255, 0))

        patient = time.time() - self.last_leg_detected
        if not self.leg_detected and patient >= 5:
            self.get_logger().info("No leg connection")

        # self.cnt = 0 
        # img_msg = bridge.cv2_to_imgmsg(img)
        # self.img_pub.publish(img_msg)

        ###### New logic
        # if "leg" in data.yolov8_inference[class_name]:
        #     self.get_logger().info("found leg")
        # else:
        #     self.get_logger().info("No leg found")

    def timer_callback(self):
        # Your periodic processing logic here
        pass

def main(args=None):
    rclpy.init(args=None)
    yolo_subscriber = Yolo_subscriber()
    # camera_subscriber = Camera_subscriber()

    # executor = MultiThreadedExecutor()
    # executor.add_node(yolo_subscriber)
    # executor.add_node(camera_subscriber)

    # executor_thread = threading.Thread(target=executor.spin, daemon=True)
    # executor_thread.start()

    # rate = yolo_subscriber.create_rate(2)
    # try:
    #   while rclpy.ok():
    #       rate.sleep()
    # except KeyboardInterrupt:
    #   pass 

    rclpy.spin(yolo_subscriber)
    rclpy.shutdown()
    # executor_thread.join

if __name__ == '__main__':
    main()

