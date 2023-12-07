#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from yolov8_msgs.msg import Yolov8Inference  # Updated message type
from geometry_msgs.msg import Twist, Vector3

global vel_msg
vel_msg = Twist()


class FollowMeNode(Node):
    def __init__(self):
        super().__init__('follow_me_node')

        self.error_history_x = []
        self.error_history_y = []  
        self.prev_error_x = 0
        self.prev_error_y = 0
        self.subscription = self.create_subscription(
            Yolov8Inference,  # Updated message type
            '/Yolov8_Inference',
            self.inference_callback,
            10  # QoS profile, adjust if necessary
        )
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def inference_callback(self, msg):
        # Process YOLOv8 inference message
        # You can access inference information from the 'msg' object

		#Params Constants

        self.Kp_angular = -0.01
        self.Kp_linear = 0.004  
        self.Ki_angular = -0.00005
        self.Ki_linear = 0.00004  
        self.Kd_angular = 0.002
        self.Kd_linear = -0.0001  

        self.target_x = 160
        self.target_y = 210
        self.max_angular = 2.0
        self.max_linear = -0.17
        self.recovery_angular = 0.6
        self.error_range_x = 10
        self.error_range_y = 5
        self.integral_data_point = 50
        self.confidence_threshold = 0

        #Variables
        self.proportional_angular = 0
        self.proportional_linear = 0
        self.integral_angular = 0
        self.integral_linear = 0
        self.deravative_angular = 0
        self.deravative_linear = 0
        self.x_speed = 0.0
        self.z_speed = 0.0

        self.count = 0
        for objects in msg.yolov8_inference:
             if (objects.class_name == "person" and objects.conf > self.confidence_threshold):
                  self.count += 1
             
        for objects in msg.yolov8_inference:
            if (objects.class_name == "person" and objects.conf > self.confidence_threshold):

                #PID
                self.width = objects.bottom - objects.top
                self.height = objects.right - objects.left
                self.center_x = self.width/2 + objects.top
                self.center_y = self.height/2 + objects.left
                self.error_x = self.center_x - self.target_x
                self.error_y = objects.right - self.target_y
                if (abs(self.error_x) < self.error_range_x):
                        self.z_speed = 0.0
                elif (abs(self.error_y) < self.error_range_y):
                        self.x_speed = 0.0
                self.error_history_x.append(self.error_range_x)
                self.error_history_x = self.error_history_x[-self.integral_data_point:]
                self.error_history_y.append(self.error_range_y)
                self.error_history_y = self.error_history_y[-self.integral_data_point:]

                self.proportional_angular = self.error_x * self.Kp_angular
                self.integral_angular = sum(self.error_history_x) * self.Ki_angular
                self.deravative_angular = (self.error_x - self.prev_error_x) * self.Kd_angular
                self.z_speed = self.proportional_angular + self.integral_angular + self.deravative_angular
                
                self.proportional_linear = self.error_y * self.Kp_linear
                self.integral_linear = sum(self.error_history_y) * self.Ki_linear
                self.deravative_linear = (self.error_y - self.prev_error_y) * self.Kd_linear
                self.x_speed = self.proportional_linear + self.integral_linear + self.deravative_linear

                #Cap-ing the maximum velocity
                if (abs(self.z_speed) > self.max_angular and self.z_speed < 0.0 or self.error_x > 40):
                        self.z_speed = -self.max_angular
                elif (abs(self.z_speed) > self.max_angular and self.z_speed > 0.0 or self.error_x < -40):
                        self.z_speed = self.max_angular
                if (self.x_speed < self.max_linear or self.error_y < -40):
                        self.x_speed = self.max_linear
                vel_msg.angular.z = self.z_speed
                vel_msg.linear.x = self.x_speed
                self.publisher_.publish(vel_msg)

                self.prev_error_x = self.error_x
                self.prev_error_y = self.error_y
                self.get_logger().info("x error:{} y error:{}".format(self.error_x,self.error_y))
                #self.get_logger().info('I found a person!')
                #self.get_logger().info("X:{} Y:{} W:{} H:{}".format(self.center_x,self.center_y,self.width,self.height))
                #self.get_logger().info("top:{} left:{} btm:{} right:{}".format(objects.top, objects.left, objects.bottom, objects.right))
                break
            elif (self.count == 0):
                self.get_logger().info('No human detected!')
                self.x_speed = 0.0
                if self.z_speed > 0:
                    self.z_speed = self.recovery_angular
                else:
                    self.z_speed = -self.recovery_angular
                self.z_speed = -self.recovery_angular
                vel_msg.linear.x = self.x_speed
                vel_msg.angular.z = self.z_speed
                self.publisher_.publish(vel_msg)

        # if (len(msg.yolov8_inference)==0):
        #     self.get_logger().info('Length is 0')
        #     vel_msg.linear.x = 0.0
        #     if vel_msg.angular.z > 0.0:
        #         vel_msg.angular.z = self.recovery_angular
        #     else:
        #         vel_msg.angular.z = -self.recovery_angular
        # else:
        #     for objects in msg.yolov8_inference:
        #         if (objects.class_name == "person" and objects.conf > self.confidence_threshold):

        #             #PID
        #             self.width = objects.bottom - objects.top
        #             self.height = objects.right - objects.left
        #             self.center_x = self.width/2 + objects.top
        #             self.center_y = self.height/2 + objects.left
        #             self.error_x = self.center_x - self.target_x
        #             self.error_y = objects.right - self.target_y
        #             if (abs(self.error_x) < self.error_range_x):
        #                  vel_msg.angular.z = 0.0
        #             elif (abs(self.error_y) < self.error_range_y):
        #                  vel_msg.linear.x = 0.0
        #             self.error_history_x.append(self.error_range_x)
        #             self.error_history_x = self.error_history_x[-self.integral_data_point:]
        #             self.error_history_y.append(self.error_range_y)
        #             self.error_history_y = self.error_history_y[-self.integral_data_point:]

        #             self.proportional_angular = self.error_x * self.Kp_angular
        #             self.integral_angular = sum(self.error_history_x) * self.Ki_angular
        #             self.deravative_angular = (self.error_x - self.prev_error_x) * self.Kd_angular
        #             vel_msg.angular.z = self.proportional_angular + self.integral_angular + self.deravative_angular
                    
        #             self.proportional_linear = self.error_y * self.Kp_linear
        #             self.integral_linear = sum(self.error_history_y) * self.Ki_linear
        #             self.deravative_linear = (self.error_y - self.prev_error_y) * self.Kd_linear
        #             vel_msg.linear.x = self.proportional_linear + self.integral_linear + self.deravative_linear

        #             #Cap-ing the maximum velocity
        #             if (abs(vel_msg.angular.z) > self.max_angular and vel_msg.angular.z < 0.0):
        #                     vel_msg.angular.z = -self.max_angular
        #             elif (abs(vel_msg.angular.z) > self.max_angular and vel_msg.angular.z > 0.0):
        #                     vel_msg.angular.z = self.max_angular
        #             if (vel_msg.linear.x < self.max_linear):
        #                     vel_msg.linear.x = self.max_linear
        #             self.publisher_.publish(vel_msg)

        #             self.prev_error_x = self.error_x
        #             self.prev_error_y = self.error_y
        #             self.get_logger().info("x error:{} y error:{}".format(self.error_x,self.error_y))
        #             #self.get_logger().info('I found a person!')
        #             #self.get_logger().info("X:{} Y:{} W:{} H:{}".format(self.center_x,self.center_y,self.width,self.height))
        #             #self.get_logger().info("top:{} left:{} btm:{} right:{}".format(objects.top, objects.left, objects.bottom, objects.right))
        #             break
        #         else:
        #             pass
        #             self.get_logger().info('No human detected!')
        #             vel_msg.linear.x = 0.0
        #             if vel_msg.angular.z > 0:
        #                 vel_msg.angular.z = self.recovery_angular
        #             else:
        #                 vel_msg.angular.z = -self.recovery_angular
        self.publisher_.publish(vel_msg)
def main(args=None):
    rclpy.init(args=args)
    node = FollowMeNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
