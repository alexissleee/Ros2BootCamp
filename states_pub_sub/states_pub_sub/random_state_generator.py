import rclpy
from rclpy.node import Node
from custom_states.msg import State7D
import random


class RandomStateGenerator(Node):
    def __init__(self):
        super().__init__('random_state_generator')

        self.period = 1.0  # seconds (subject to change)

        self.publisher = self.create_publisher(
            State7D,
            '/seven_dim_state',
            10
        )

        self.timer = self.create_timer(
            self.period,
            self.publish_random
        )

    def publish_random(self):
        msg = State7D()

        msg.x = random.uniform(-10.0, 10.0)
        msg.y = random.uniform(-10.0, 10.0)
        msg.z = random.uniform(-10.0, 10.0)

        msg.vx = random.uniform(-5.0, 5.0)
        msg.vy = random.uniform(-5.0, 5.0)
        msg.vz = random.uniform(-5.0, 5.0)

        msg.yaw = random.uniform(-3.14, 3.14)

        self.publisher.publish(msg)

        self.get_logger().info(
            f"Published 7D state: "
            f"x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}, "
            f"vx={msg.vx:.2f}, vy={msg.vy:.2f}, vz={msg.vz:.2f}, "
            f"yaw={msg.yaw:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)

    random_state_generator = RandomStateGenerator()
    rclpy.spin(random_state_generator)

    random_state_generator.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
