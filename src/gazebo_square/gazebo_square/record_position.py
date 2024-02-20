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

    def listener_callback(self, msg):
        position = msg.pose.pose.position
        with open('position.txt', 'a') as f:
            f.write(f'x: {float(position.x)}, y: {float(position.y)}\n')
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
