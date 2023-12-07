import math
# Twist expresses velocity in free space broken into its linear and angular parts
# $ ros2 interface show geometry_msgs/msg/Twist
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
# We are using a listener node to listen to the broadcasted transformation.
from tf2_ros.transform_listener import TransformListener
# Required to spawn the turtle2
from turtlesim.srv import Spawn

class FrameListener(Node):
	def __init__(self):
		super().__init__('turtle_tf2_frame_listener')
		# Check the Usage examples (commandline and the launch file) to see how the
		# ‘target frame’ parameter has been defined/input
		# Declare and acquire `target_frame` parameter
		self.target_frame = self.declare_parameter('target_frame', 'turtle1').get_parameter_value().string_value
		self.tf_buffer = Buffer()
		self.tf_listener = TransformListener(self.tf_buffer, self)
		# Calling the Spawn service, imported in the beginning
		# Create a client to spawn a turtle
		self.spawner = self.create_client(Spawn, 'spawn')
		# Boolean values to store the information
		# if the service for spawning turtle is available
		self.turtle_spawning_service_ready = False
		# if the turtle was successfully spawned
		self.turtle_spawned = False
		# Create turtle2 velocity publisher
		self.publisher = self.create_publisher(Twist, 'turtle2/cmd_vel', 10)
		# Call on_timer function every second
		self.timer = self.create_timer(0.1, self.on_timer)
	def on_timer(self):
		# Store frame names in variables that will be used to
		# compute transformations # from turtle1 >>> turtle2

		from_frame_rel = self.target_frame # Parent frame
		to_frame_rel = 'turtle2' # Child frame
		if self.turtle_spawning_service_ready:
			if self.turtle_spawned:
				# Look up for the transformation between target_frame and turtle2 frames
				# and send velocity commands for turtle2 to reach target_frame
				try:
					t = self.tf_buffer.lookup_transform(
						to_frame_rel,
						from_frame_rel,
						rclpy.time.Time())
				except TransformException as ex:
					self.get_logger().info(f'Could not transform {to_frame_rel} to {from_frame_rel}: {ex}')
					return
				msg = Twist() # The Twist msg type expresses linear and angular velocities
				# Calculate angular velocity about the z axis using the relative angle.
				scale_rotation_rate = 1.5
				msg.angular.z = scale_rotation_rate * math.atan2(t.transform.translation.y,t.transform.translation.x)
				# Calculate angular velocity about the z axis using the relative distance.
				scale_forward_speed = 1
				error_x = t.transform.translation.x-1
				error_y = t.transform.translation.y-1
				if error_x < 1:
					error_x = 0.0
				if error_y < 1:
					error_y = 0.0
				msg.linear.x = scale_forward_speed * math.sqrt((error_x) ** 2 +(error_y) ** 2)
				self.get_logger().info(f'X:{t.transform.translation.x}, Y:{t.transform.translation.y}')
				self.get_logger().info(f'new_X:{t.transform.translation.x-1}, new_Y:{t.transform.translation.y-1}')
				# Send velocity messages to turtle2.
				self.publisher.publish(msg)
			else:
				if self.result.done():
					self.get_logger().info(f'Successfully spawned {self.result.result().name}')
					self.turtle_spawned = True
				else:
					self.get_logger().info('Spawn is not finished')
		else:
			if self.spawner.service_is_ready():
				# Initialize request with turtle name and coordinates
				# Note that x, y and theta are defined as floats in turtlesim/srv/Spawn
				request = Spawn.Request()
				request.name = 'turtle2'
				request.x = float(4)
				request.y = float(2)
				request.theta = float(0)
				# Call request
				self.result = self.spawner.call_async(request)
				self.turtle_spawning_service_ready = True
			else:
				# Check if the service is ready
				self.get_logger().info('Service is not ready')
def main():
	rclpy.init()
	node = FrameListener()
	try:
		rclpy.spin(node)
	except KeyboardInterrupt:
		pass
	rclpy.shutdown()
