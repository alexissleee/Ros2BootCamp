import rclpy
from rclpy.node import Node

from custom_states.msg import State7D, State6D  # our custom msg


class StateSubscriber(Node):
    def __init__(self):
        super().__init__('state_subscriber')

        self.publisher = self.create_publisher(
            State6D,
            '/six_dim_state',
            10
        )

        self.subscription = self.create_subscription(
            State7D,
            '/seven_dim_state',
            self.listener_callback,
            10
        )

    def listener_callback(self, msg):
        out_msg = State6D()

        # copy all fields except yaw
        out_msg.x = msg.x
        out_msg.y = msg.y
        out_msg.z = msg.z
        out_msg.vx = msg.vx
        out_msg.vy = msg.vy
        out_msg.vz = msg.vz

        # publish 6D state without yaw
        self.publisher.publish(out_msg)

        self.get_logger().info(
            f"Received 7D state -> Published 6D: "
            f"x={out_msg.x:.2f}, y={out_msg.y:.2f}, z={out_msg.z:.2f}, "
            f"vx={out_msg.vx:.2f}, vy={out_msg.vy:.2f}, vz={out_msg.vz:.2f}"
        )


def main(args=None):
    rclpy.init(args=args)

    state_subscriber = StateSubscriber()
    rclpy.spin(state_subscriber)

    state_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
