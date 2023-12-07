#!/usr/bin/env python3

from ultralytics import YOLO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist, Vector3
from yolov8_msgs.msg import InferenceResult
from yolov8_msgs.msg import Yolov8Inference

bridge = CvBridge()
vel_msg = Twist()

class Camera_subscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.model = YOLO('~/yolobot/src/yolobot_recognition/scripts/yolov8n.pt')

        self.yolov8_inference = Yolov8Inference()

#        self.subscription = self.create_subscription(
#            Image,
#            'rgb_cam/image_raw',
#            self.camera_callback,
#            10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.02
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.subscription = self.create_subscription(
            Image,
            #'/camera1/image_raw',
            '/transport/uncompressed',
            self.camera_callback,
            10)
        self.subscription 

        self.yolov8_pub = self.create_publisher(Yolov8Inference, "/Yolov8_Inference", 1)
        self.img_pub = self.create_publisher(Image, "/inference_result", 1)
        
    def timer_callback(self):
        global vel_msg
        self.publisher_.publish(vel_msg)
        
    def camera_callback(self, data):
        img = bridge.imgmsg_to_cv2(data, "bgr8")
        results = self.model(img)

        self.yolov8_inference.header.frame_id = "inference"
        self.yolov8_inference.header.stamp = camera_subscriber.get_clock().now().to_msg()
        
        #Params
        self.target_x = 160
        self.target_y = 200
        self.Kp_angular = -0.01
        self.Kp_linear = 0.01
        self.max_angular = 0.5
        self.max_linear = -0.2
        self.recovery_angular = 0.5
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                self.inference_result = InferenceResult()
                b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                self.inference_result.class_name = self.model.names[int(c)]
                self.inference_result.top = int(b[0])
                self.inference_result.left = int(b[1])
                self.inference_result.bottom = int(b[2])
                self.inference_result.right = int(b[3])
                self.yolov8_inference.yolov8_inference.append(self.inference_result)
                if (self.inference_result.class_name == "person"):
                    self.width = self.inference_result.bottom - self.inference_result.top
                    self.height = self.inference_result.right - self.inference_result.left
                    self.center_x = self.width/2 + self.inference_result.top
                    self.center_y = self.height/2 + self.inference_result.left
                    self.error_x = self.center_x - self.target_x
                    self.error_y = self.inference_result.right - self.target_y
                    vel_msg.angular.z = self.error_x * self.Kp_angular
                    vel_msg.linear.x = self.error_y * self.Kp_linear
                    if (abs(vel_msg.angular.z) > self.max_angular and vel_msg.angular.z < 0.0):
                        vel_msg.angular.z = -self.max_angular
                    elif (abs(vel_msg.angular.z) > self.max_angular and vel_msg.angular.z > 0.0):
                        vel_msg.angular.z = self.max_angular
                    if (vel_msg.linear.x < self.max_linear):
                        vel_msg.linear.x = self.max_linear
                    camera_subscriber.get_logger().info('I found a person!')
                    camera_subscriber.get_logger().info("X:{} Y:{} W:{} H:{}".format(self.center_x,self.center_y,self.width,self.height))
                    camera_subscriber.get_logger().info("top:{} left:{} btm:{} right:{}".format(self.inference_result.top,self.inference_result.left,self.inference_result.bottom,self.inference_result.right))
                else:
                    camera_subscriber.get_logger().info('No human detected!')
                    vel_msg.linear.x = 0.0
                    if vel_msg.angular.z > 0:
                        vel_msg.angular.z = self.recovery_angular
                    else:
                        vel_msg.angular.z = -self.recovery_angular
                	#camera_subscriber.get_logger().info("top:{} left:{} btm:{} right:{}".format(self.inference_result.top,self.inference_result.left,self.inference_result.bottom,self.inference_result.right))
            #camera_subscriber.get_logger().info(f"{self.yolov8_inference}")

        annotated_frame = results[0].plot()
        img_msg = bridge.cv2_to_imgmsg(annotated_frame)  

        self.img_pub.publish(img_msg)
        self.yolov8_pub.publish(self.yolov8_inference)
        self.yolov8_inference.yolov8_inference.clear()

if __name__ == '__main__':
    rclpy.init(args=None)
    camera_subscriber = Camera_subscriber()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()
