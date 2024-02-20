import subprocess
import rclpy
from geometry_msgs.msg import Twist
from math import pi
import threading
import numpy as np

distance = 4.0
angle = pi / 2.0


def main(args=None):
    rclpy.init(args=args)
    rate_node = rclpy.create_node('rate_node')
    rate_node.declare_parameter('l_noise', 0.0)
    rate_node.declare_parameter('a_noise', 0.0)
    rate_node.declare_parameter('file_name', 'position.txt')

    linear_noise = rate_node.get_parameter('l_noise').get_parameter_value().double_value
    angular_noise = rate_node.get_parameter('a_noise').get_parameter_value().double_value
    file_name = rate_node.get_parameter('file_name').get_parameter_value().string_value

    t = threading.Thread(target=rclpy.spin, args=(rate_node,), daemon=True)  # the rate rely on the spin function
    # running in a separate thread
    t.start()

    frq = 10  # frequency: Hz
    fwd_time = 8
    rot_time = 5

    rate = rate_node.create_rate(frq)  # create a rate object with 10Hz, use rate.sleep() to keep the frequency
    pub = rate_node.create_publisher(Twist, 'cmd_vel', 10)
    try:
        msg = Twist()
        subprocess.run(["ros2", "service", "call", "/reset_simulation", "std_srvs/srv/Empty"])  # reset the simulation
        for i in range(4 * fwd_time * frq):
            noise = np.random.normal(0, linear_noise)
            msg.linear.x = distance / fwd_time + noise
            msg.angular.z = 0.0
            pub.publish(msg)    # publish the message

            rate_node.get_logger().info('[Translation] Publishing: "%s"' % i)
            rate.sleep()  # the code will sleep to keep the frequency, in this case 10Hz

            if (i + 1) % (fwd_time * frq) == 0:
                rate.sleep()
                for _ in range(rot_time * frq):
                    noise = np.random.normal(0, angular_noise)
                    msg.linear.x = 0.0
                    msg.angular.z = angle / rot_time + noise
                    pub.publish(msg)

                    rate_node.get_logger().info('[Rotation] Publishing: "%s"' % i)
                    rate.sleep()

        msg.linear.x = 0.0
        msg.angular.z = 0.0
        pub.publish(msg)
        rate_node.get_logger().info('[Stop] Publishing: "%s"' % i)
        subprocess.run(['ros2', 'run', 'lab32', 'position', '--ros-args', '-p', f'file_name:={file_name}'])

    except KeyboardInterrupt:
        pass

    rate_node.destroy_node()
    rclpy.shutdown()
    t.join()


if __name__ == '__main__':
    main()
