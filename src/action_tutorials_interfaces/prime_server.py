import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('prime_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'prime',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        prime = [2,3,5,7,11,13,17,19,23,29,31,37,41]
        feedback_msg.partial_sequence = []

        for i in range(0, goal_handle.request.order):
            feedback_msg.partial_sequence.append(prime[i])
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info('Feedback: {0}'.format(feedback_msg.partial_sequence))
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)

    fibonacci_action_server = FibonacciActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == '__main__':
    main()
