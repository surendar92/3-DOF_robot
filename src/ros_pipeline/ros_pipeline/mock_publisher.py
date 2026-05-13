import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
from ros_pipeline_interfaces.srv import SetRecording
import random
import math


class MockPublisher(Node):

    def __init__(self):
        super().__init__('mock_publisher')

        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.rec_pub   = self.create_publisher(Bool, '/leader/recording', 10)

        self.srv = self.create_service(
            SetRecording, '/set_recording', self.handle_set_recording)

        self.recording = False
        self.timer = self.create_timer(0.1, self.publish_joints)
        self.get_logger().info('mock_publisher started')

    def handle_set_recording(self, request, response):
        self.recording = request.record

        msg = Bool()
        msg.data = self.recording
        self.rec_pub.publish(msg)

        status = 'STARTED' if self.recording else 'STOPPED'
        self.get_logger().info(f'Recording {status}')

        response.success = True
        response.message = f'Recording {status}'
        return response

    def publish_joints(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3']
        msg.position = [
            random.uniform(-math.pi,     math.pi),
            random.uniform(-math.pi / 2, math.pi / 2),
            random.uniform(-math.pi / 2, math.pi / 2),
        ]
        self.joint_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MockPublisher()
    rclpy.spin(node)
    rclpy.shutdown()