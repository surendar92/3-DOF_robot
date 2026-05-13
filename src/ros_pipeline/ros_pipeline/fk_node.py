import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
import math

D1 = 0.5
A2 = 0.4
A3 = 0.3


class FKNode(Node):

    def __init__(self):
        super().__init__('fk_node')

        self.sub = self.create_subscription(
            JointState, '/joint_states', self.compute_fk, 10)

        self.pub = self.create_publisher(
            Point, '/end_effector_position', 10)

        self.get_logger().info('fk_node started')

    def compute_fk(self, msg):
        t1 = msg.position[0]
        t2 = msg.position[1]
        t3 = msg.position[2]

        r = A2 * math.cos(t2) + A3 * math.cos(t2 + t3)
        x = math.cos(t1) * r
        y = math.sin(t1) * r
        z = D1 + A2 * math.sin(t2) + A3 * math.sin(t2 + t3)

        point = Point()
        point.x = x
        point.y = y
        point.z = z
        self.pub.publish(point)


def main(args=None):
    rclpy.init(args=args)
    node = FKNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()