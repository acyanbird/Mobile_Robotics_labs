#!/usr/bin/env python
from math import pi, sqrt, atan2, cos, sin
import numpy as np
import threading

import rclpy
from tf_transformations import euler_from_quaternion
from std_msgs.msg import Empty
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose2D

distance = 4.0
angle = pi / 2.0
l_noise = 0.02
a_noise = 0.01
frq = 10  # frequency: Hz
fwd_time = 8
rot_time = 5
angle_count = 0
final_pos = list()

class Turtlebot3():
    def __init__(self):
        rclpy.init()
        self.node = rclpy.create_node("turtlebot3_move_square")
        self.node.get_logger().info("Press Ctrl + C to terminate")
        self.vel_pub = self.node.create_publisher(Twist, "cmd_vel", 10)
        self.rate = self.node.create_rate(frq)



        t = threading.Thread(target=rclpy.spin, args=(self.node,), daemon=True)
        t.start()

        # subscribe to odometry
        self.pose = Pose2D()
        self.logging_counter = 0
        self.trajectory = list()
        self.odom_sub = self.node.create_subscription(Odometry, "odom", self.odom_callback, 10)

        # init controller
        self.controller = Controller()
        self.controller.setPD(0.38, 0.03)
        # initial angle should be same to robot prevent turning at the beginning
        self.controller.setPoint(0)

        try:
            self.run()
        except KeyboardInterrupt:
            print('Interrupted')
        finally:
            # save trajectory to csv file
            np.savetxt('trajectory_close.csv', np.array(self.trajectory), delimiter=',')
            with open('close_final3.txt', 'a') as f:
                f.write(str(self.final_pos[0]) + ' ' + str(self.final_pos[1]) + '\n')  # write new line

            self.node.destroy_node()
            rclpy.shutdown()

    def run(self, angle_count=0):
        # add your code here to adjust your movement based on 2D pose feedback
        msg = Twist()
        for i in range(4 * fwd_time * frq):
            noise = np.random.normal(0, l_noise)
            msg.linear.x = distance / fwd_time + noise
            msg.angular.z = 0.0
            self.vel_pub.publish(msg)  # publish the message

            self.node.get_logger().info('[Translation] Publishing: "%s"' % i)
            self.rate.sleep()  # the code will sleep to keep the frequency, in this case 10Hz

            if (i + 1) % (fwd_time * frq) == 0:
                self.rate.sleep()
                angle_count += 1
                desired_angle = pi / 2 * angle_count
                self.controller.setPoint(desired_angle)
                for _ in range(rot_time * frq):
                    noise = np.random.normal(0, a_noise)
                    msg.linear.x = 0.0
                    # msg.angular.z = angle / rot_time + noise
                    msg.angular.z = self.controller.update(self.pose.theta) + noise
                    self.vel_pub.publish(msg)

                    self.node.get_logger().info('[Rotation] Publishing: "%s"' % i)
                    self.rate.sleep()

        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.vel_pub.publish(msg)
        self.node.get_logger().info('[Stop] Publishing: "%s"' % i)
        self.final_pos = [float(self.pose.x), float(self.pose.y)]  # save last position

    def odom_callback(self, msg):
        # get pose = (x, y, theta) from odometry topic
        quaternion = [msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, \
                      msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]
        (roll, pitch, yaw) = euler_from_quaternion(quaternion)
        # Convert yaw to a value between 0 and 2*pi
        yaw = atan2(sin(yaw), cos(yaw))
        if yaw < 0:
            yaw += 2 * pi

        self.pose.theta = yaw
        self.pose.x = msg.pose.pose.position.x
        self.pose.y = msg.pose.pose.position.y

        # logging once every 100 times (Gazebo runs at 1000Hz; we save it at 10Hz)
        self.logging_counter += 1
        if self.logging_counter == 100:
            self.logging_counter = 0
            self.trajectory.append([self.pose.x, self.pose.y, self.pose.theta])  # save trajectory
            self.node.get_logger().info("odom: x=" + str(self.pose.x) + \
                                        ";  y=" + str(self.pose.y) + ";  theta=" + str(yaw))


def main(args=None):
    turtlebot = Turtlebot3()


class Controller:
    def __init__(self, P=0.0, D=0.0, set_point=0):
        self.Kp = P
        self.Kd = D
        self.set_point = set_point  # reference (desired value)
        self.previous_error = 0

    def update(self, current_value):
        # calculate P_term and D_term
        error = self.set_point - current_value
        P_term = self.Kp * error
        D_term = self.Kd * (error - self.previous_error)
        self.previous_error = error
        return P_term + D_term

    def setPoint(self, set_point):
        self.set_point = set_point
        self.previous_error = 0

    def setPD(self, P=0.0, D=0.0):
        self.Kp = P
        self.Kd = D


if __name__ == '__main__':
    main()
