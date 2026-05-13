import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Point
from std_msgs.msg import Bool
import json
import os
from datetime import datetime

SAVE_DIR = os.path.expanduser('~/episodes')


class DataCollector(Node):

    def __init__(self):
        super().__init__('data_collector')

        self.recording     = False
        self.episode       = []
        self.latest_joints = None
        self.latest_ee     = None

        self.create_subscription(
            JointState, '/joint_states', self.cb_joints, 10)
        self.create_subscription(
            Point, '/end_effector_position', self.cb_ee, 10)
        self.create_subscription(
            Bool, '/leader/recording', self.cb_recording, 10)

        os.makedirs(SAVE_DIR, exist_ok=True)
        self.get_logger().info(f'data_collector started. Saving to {SAVE_DIR}')

    def cb_joints(self, msg):
        self.latest_joints = list(msg.position)
        self.try_record()

    def cb_ee(self, msg):
        self.latest_ee = [msg.x, msg.y, msg.z]
        self.try_record()

    def cb_recording(self, msg):
        was_recording    = self.recording
        self.recording   = msg.data

        if was_recording and not self.recording:
            self.save_episode()

    def try_record(self):
        if self.recording and self.latest_joints and self.latest_ee:
            entry = {
                'joint_states': self.latest_joints,
                'ee_position':  self.latest_ee,
            }
            self.episode.append(entry)
            self.latest_joints = None
            self.latest_ee     = None

    def save_episode(self):
        if not self.episode:
            self.get_logger().warn('No data to save.')
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename  = os.path.join(SAVE_DIR, f'episode_{timestamp}.json')

        with open(filename, 'w') as f:
            json.dump(self.episode, f, indent=2)

        self.get_logger().info(
            f'Saved {len(self.episode)} steps → {filename}')
        self.episode = []


def main(args=None):
    rclpy.init(args=args)
    node = DataCollector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()