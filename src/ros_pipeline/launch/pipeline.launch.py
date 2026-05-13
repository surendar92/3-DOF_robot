from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():        
    return LaunchDescription([
        Node(
            package='ros_pipeline',
            executable='mock_publisher',
            name='mock_publisher',
            output='screen',
        ),
        Node(
            package='ros_pipeline',
            executable='fk_node',
            name='fk_node',
            output='screen',
        ),
        Node(
            package='ros_pipeline',
            executable='data_collector',
            name='data_collector',
            output='screen',
        ),
    ])