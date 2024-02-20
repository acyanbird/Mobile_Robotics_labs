import os
import time

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import threading


class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            'odom',
            self.listener_callback,
            10)
        self.declare_parameter('file_name', 'position.txt')
        self.file_name = self.get_parameter('file_name').get_parameter_value().string_value

    def listener_callback(self, msg):
        position = msg.pose.pose.position
        with open(self.file_name, 'a') as f:
            f.write(f'{float(position.x)} {float(position.y)}\n')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    odom_subscriber = OdomSubscriber()
    t = threading.Thread(target=rclpy.spin, args=(odom_subscriber,), daemon=True)
    t.start()
    time.sleep(0.2)
    os._exit(0)


if __name__ == '__main__':
    main()
