import sys
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute
import random
import math
import time


class RandomGoalClient(Node):
    def __init__(self):
        super().__init__('random_goal_client')

        # Create client for the teleport service
        self.cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = TeleportAbsolute.Request()

    def send_request(self):
        # Generate random goal
        self.req.x = random.uniform(1.0, 10.0)
        self.req.y = random.uniform(1.0, 10.0)
        self.req.theta = random.uniform(-math.pi, math.pi)

        return self.cli.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)
    client_node = RandomGoalClient()

    try:
        for i in range(5):  # move 5 random goals, 10 seconds apart
            future = client_node.send_request()
            rclpy.spin_until_future_complete(client_node, future)

            if future.result() is not None:
                client_node.get_logger().info(
                    f"Turtle moved to random goal: "
                    f"x={client_node.req.x:.2f}, y={client_node.req.y:.2f}, theta={client_node.req.theta:.2f}"
                )
            else:
                client_node.get_logger().error('Service call failed')

            time.sleep(10.0)

    finally:
        client_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
