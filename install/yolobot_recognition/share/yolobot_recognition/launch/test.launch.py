from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Launch the image_transport republish node
        Node(
            package='image_transport',
            executable='republish',
            name='image_transport_republish',
            #output='screen',
            arguments=[
            	'compressed','raw',
                '--ros-args',
                '-r', 'in/compressed:=/image_raw/compressed',
                '-r', 'out:=/transport/uncompressed'
            ],
        ),

        # Launch the yolov8_ros2_control.py script
        Node(
            package='yolobot_recognition',
            executable='yolov8_ros2_control.py',
            name='yolov8_ros2_control_node',
            output='screen',
        ),
    ])
