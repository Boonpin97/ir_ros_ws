from my_interfaces.srv import TimeReq
import rclpy
from rclpy.node import Node
from datetime import datetime

class MinimalService(Node):
	def __init__(self):
		super().__init__('minimal_service') # node name
		self.srv = self.create_service(TimeReq, 'request_time',self.add_three_ints_callback)
# service callback receives the request data, sums it, and returns the sum as a response.
	def add_three_ints_callback(self, request, response):
		self.get_logger().info('Incoming request')
		response.time  = str(datetime.now().strftime("%H:%M:%S"))
		return response
def main(args=None):
	rclpy.init(args=args)
	minimal_service = MinimalService()
	rclpy.spin(minimal_service)
	rclpy.shutdown()
if __name__ == '__main__':
	main()
