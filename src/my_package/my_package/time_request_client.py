from my_interfaces.srv import TimeReq
import sys
import rclpy
from rclpy.node import Node
class MinimalClientAsync(Node):
	def __init__ (self):
		super().__init__('minimal_client_async')
		self.cli = self.create_client(TimeReq, 'request_time')
		while not self.cli.wait_for_service(timeout_sec=1.0):
			self.get_logger().info('service not available, waiting again...')
		self.req = TimeReq.Request()
	def send_request(self):
		# Gets the variables (arguments) typed at the commandline
		self.future = self.cli.call_async(self.req)
def main(args=None):
	rclpy.init(args=args)
	minimal_client = MinimalClientAsync()
	minimal_client.send_request()
	while rclpy.ok(): # waiting for future responses from the service
		rclpy.spin_once(minimal_client)
		if minimal_client.future.done():
			try:
				response = minimal_client.future.result()
				minimal_client.get_logger().info('The current time is %s' %(response.time))
			except Exception as e:
				minimal_client.get_logger().info('Service call failed %r' % (e,))
		else:
			minimal_client.get_logger().info(f"current time is {response.time}")
		break
	minimal_client.destroy_node()
	rclpy.shutdown()
if __name__ == '__main__':
	main()
