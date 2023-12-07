import math
import sys
# Below import: TransformStamped provides a template for the message to be published to the transformation tree
from geometry_msgs.msg import TransformStamped
import numpy as np
import rclpy
from rclpy.node import Node # To create a Node
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
def quaternion_from_euler(ai, aj, ak): # Converts quaternions to Euler angles
	ai /= 2.0
	aj /= 2.0
	ak /= 2.0
	ci = math.cos(ai)
	si = math.sin(ai)
	cj = math.cos(aj)
	sj = math.sin(aj)
	ck = math.cos(ak)
	sk = math.sin(ak)
	cc = ci*ck
	cs = ci*sk
	sc = si*ck
	ss = si*sk
	q = np.empty((4, ))
	q[0] = cj*sc - sj*cs
	q[1] = cj*ss + sj*cc
	q[2] = cj*cs - sj*sc
	q[3] = cj*cc + sj*ss
	return q
class StaticFramePublisher(Node):
	"""
	Broadcast transforms that never change.
	This example publishes transforms from `world` to a static turtle frame.
	The transforms are only published once at startup, and are constant for all time.
	"""
	def __init__(self, transformation):
		#super().__init__('static_turtle_tf2_broadcaster')
		super().__init__('/broadcaster1')
		self.tf_static_broadcaster = StaticTransformBroadcaster(self) # Broadcaster object
		# Publish static transforms once at startup
		self.make_transforms(transformation) # Function is defined later
	def make_transforms(self, transformation):
		t = TransformStamped() # Creates the transformation object
		t.header.stamp = self.get_clock().now().to_msg() # Current time
		t.header.frame_id = 'world' # Parent frame
		t.child_frame_id = transformation[1] # Child frame, given as a user input
		t.transform.translation.x = float(transformation[2])
		t.transform.translation.y = float(transformation[3])
		t.transform.translation.z = float(transformation[4])
		quat = quaternion_from_euler(
		float(transformation[5]), float(transformation[6]), float(transformation[7]))
		t.transform.rotation.x = quat[0]
		t.transform.rotation.y = quat[1]
		t.transform.rotation.z = quat[2]
		t.transform.rotation.w = quat[3]
		# Uses the broadcaster object to broadcast the transform
		self.tf_static_broadcaster.sendTransform(t)
def main():
	logger = rclpy.logging.get_logger('logger')
	# Error handling notifications
	# obtain parameters from command line arguments
	if len(sys.argv) != 8:
		logger.info('Invalid number of parameters. Usage: \n'
			'$ ros2 run learning_tf2_py static_turtle_tf2_broadcaster'
			'child_frame_name x y z roll pitch yaw')
		sys.exit(1)
	if sys.argv[1] == 'world':
		logger.info('Your static turtle name cannot be "world"')
		sys.exit(2)
	# Create the broadcaster node using the user-input arguments. Check the e.g. command
	# pass parameters and initialize node
	rclpy.init()
	node = StaticFramePublisher(sys.argv)
	try:
		rclpy.spin(node) # Runs the node
	except KeyboardInterrupt:
		pass
	rclpy.shutdown()
	
