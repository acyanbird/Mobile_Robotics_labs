#!/usr/bin/env python
import threading

import rclpy
from sensor_msgs.msg import LaserScan


class Turtlebot3():
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node("turtlebot3_lab51")
        self.node.get_logger().info("Press Ctrl + C to terminate")
        self.logging_counter = 0

        # subscribe to laser scan
        self.laser_sub = self.node.create_subscription(LaserScan, "scan", self.laser_callback, 10)

        t = threading.Thread(target=rclpy.spin, args=(self.node,), daemon=True)
        t.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print('Interrupted')
        finally:
            self.node.destroy_node()
            rclpy.shutdown()

    def laser_callback(self, msg):
        # print the distance to the first obstacle in front of the robot
        front = msg.ranges[0]
        left = msg.ranges[89]
        back = msg.ranges[179]
        right = msg.ranges[269]

        # logging once every 25 times (Gazebo runs at 1000Hz; we save it at 10Hz)
        self.logging_counter += 1
        if self.logging_counter == 25:
            self.logging_counter = 0
            self.node.get_logger().info(f"Front: {front:.4f}, Left: {left:.4f}, Back: {back:.4f}, Right: {right:.4f}")



def main(args=None):
    turtlebot = Turtlebot3()





if __name__ == '__main__':
    main()
