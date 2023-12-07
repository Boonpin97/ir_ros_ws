import math
import rclpy
from rclpy.node import Node
import sys
from rclpy.qos import ReliabilityPolicy, QoSProfile

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

# from tf2_ros import TransformException
# from tf2_ros.buffer import Buffer
# # We are using a listener node to listen to the broadcasted transformation.
# from tf2_ros.transform_listener import TransformListener
# # Required to spawn the turtle2
# from turtlesim.srv import Spawn

class TurtleBotCoord(Node):
    def __init__(self):
        # Here you have the class constructor
        # call super() in the constructor to initialize the Node object
        # the parameter you pass is the node name
        super().__init__('turtlebot_controller')

        self.velocity_publisher = self.create_publisher(Twist,'/turtle1/cmd_vel',10)
        #creates a subscriber object that subscribes to '/turtle1/pose' and sends received info to update_pose method
        self.pose_subscriber = self.create_subscription(Pose,'/turtle1/pose',self.update_pose, QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE))
        self.pose = Pose()
        #create a timer sending 2 parameters: duration between 2 callbacks, timer function(timer_callback)
        self.timer = self.create_timer(0.5, self.moveToGoal)
        self.check = False

    def update_pose(self,data):
        self.pose.x = data.x
        self.pose.y = data.y
        self.pose.theta = data.theta
        msg  = 'X: {:.3f}, Y: {:.3f}, 0: {:.3f}'.format(data.x, data.y, data.theta)
        self.get_logger().info(msg) #print the position of the turtle everytime it reads the info on the topic

    def get_distance(self, target_pose):
        return math.sqrt(pow((target_pose.x - self.pose.x), 2) + pow((target_pose.y - self.pose.y), 2))

    def linear_vel(self, target_pose, speed_constant = 1.0):
        return speed_constant * self.get_distance(target_pose)
    
    def steering_angle(self, target_pose): #used to calculate angular velocity of turtle later
        return math.atan2(target_pose.y - self.pose.y, target_pose.x - self.pose.x)
    
    def angular_vel(self, target_pose, speed_constant = 1.0):
        return speed_constant*(self.steering_angle(target_pose)-self.pose.theta)
    
    def moveToGoal(self):

        target_pose = Pose()

        #User input here
        target_pose.x = float(sys.argv[1])
        target_pose.y = float(sys.argv[2])
        target_pose.theta = float(sys.argv[3])

        dist_tolerance = 0.1
        angular_tolerance = 0.1
        vel_msg = Twist()

        if abs(self.steering_angle(target_pose) - self.pose.theta) > angular_tolerance:
            vel_msg.linear.x = 0.0
            vel_msg.angular.z = self.angular_vel(target_pose)

        else:
            vel_msg.angular.z = 0.0
            if self.get_distance(target_pose) >= dist_tolerance:
                vel_msg.linear.x = self.linear_vel(target_pose)
            
            else:
                vel_msg.linear.x = 0.0
                self.check = True

        if self.check:
            vel_msg.angular.z=target_pose.theta-self.pose.theta
            if abs(target_pose.theta - self.pose.theta) <= angular_tolerance:
                quit()
        
        self.velocity_publisher.publish(vel_msg)
            


        # while self.get_distance(target_pose) >= dist_tolerance:

        #     vel_msg.linear.x = self.linear_vel(target_pose)
        #     vel_msg.linear.y = 0.0
        #     vel_msg.linear.z = 0.0

        #     vel_msg.angular.x = 0.0
        #     vel_msg.angular.y = 0.0
        #     vel_msg.angular.z = self.angular_vel(target_pose)


        #     self.velocity_publisher.publish(vel_msg)

def main():
    rclpy.init()
    node = TurtleBotCoord()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    rclpy.shutdown()






















    

















