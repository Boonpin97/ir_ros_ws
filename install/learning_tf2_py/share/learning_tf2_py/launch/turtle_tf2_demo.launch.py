from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument # ADD THIS LINE
from launch.substitutions import LaunchConfiguration # ADD THIS LINE

def generate_launch_description():
	return LaunchDescription([
		Node(
			package='turtlesim',
			executable='turtlesim_node',
			name='sim'
		),
		Node(
			package='learning_tf2_py',
			executable='turtle_tf2_broadcaster',
			name='broadcaster1',
			parameters=[
				{'turtlename': 'turtle1'}
			]
		),
		# ADD lines BELOW this comment !!!!!! ---------------------------
		# declares launch arg: ‘target frame’ = turtle1
		DeclareLaunchArgument(
			'target_frame', default_value='turtle1',
			description='Target frame name.'
		),
		# broadcasts: world >>> turtle2 pose
		#Node(
		#	package='learning_tf2_py',
		#	executable='turtle_tf2_broadcaster',
		#	name='broadcaster2',
		#	parameters=[
		#		{'turtlename': 'turtle2'}
		#	]
		#),
		# listens to
			Node(
			package='learning_tf2_py',
			executable='turtle_tf2_listener',
			name='listener',
			parameters=[
				{'target_frame': LaunchConfiguration('target_frame')}
			]
		),
	])
