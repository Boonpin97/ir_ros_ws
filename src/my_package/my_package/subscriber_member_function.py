import rclpy
from rclpy.node import Node
from std_msgs.msg import String
# nearly identical to the publisher
class MinimalSubscriber(Node):
	# Uses the same topic: ‘topic’
	def __init__(self):
		super().__init__('minimal_subscriber')
		self.subscription = self.create_subscription(
			String,
			'topic',
			self.listener_callback,
			10)
		self.subscription # prevent unused variable warning
	def listener_callback(self, msg):
		# prints an info message to the cosole along with the data received
		self.get_logger().info('I heard: "%s"' % msg.data)
def main(args=None):
	rclpy.init(args=args)
	minimal_subscriber = MinimalSubscriber()
	rclpy.spin(minimal_subscriber)
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	minimal_subscriber.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
