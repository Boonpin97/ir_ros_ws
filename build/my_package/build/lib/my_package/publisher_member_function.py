import rclpy
from rclpy.node import Node # To use the Node class
from std_msgs.msg import String # imports the built-in string message type
class MinimalPublisher(Node): # creates a class that inherits from Node
	def __init__(self):
		super().__init__('minimal_publisher') # defines the node name
		# topic name = ‘topic’
		# queue size = 10
		self.publisher_ = self.create_publisher(int, 'topic', 10)
		timer_period = 0.5 # seconds # executes every 500ms
		self.timer = self.create_timer(timer_period, self.timer_callback)
		self.i = 0 # a counter used in the callback function below
	def timer_callback(self): # creates a message with the counter value appended
		msg = int()
		msg.data = self.i
		self.publisher_.publish(msg)
		self.get_logger().info('Publishing: "%s"' % msg.data) # published to console
		self.i += 1
def main(args=None): # main function
	rclpy.init(args=args)
	minimal_publisher = MinimalPublisher()
	rclpy.spin(minimal_publisher) # loops until destroyed
	# Destroy the node explicitly
	# (optional - otherwise it will be done automatically
	# when the garbage collector destroys the node object)
	minimal_publisher.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
