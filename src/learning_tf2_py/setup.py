from setuptools import find_packages, setup
import os
from glob import glob


package_name = 'learning_tf2_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
	(os.path.join('share', package_name, 'launch'), glob(os.path.join('launch','*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arms',
    maintainer_email='arms@todo.todo',
    description='Package description',
    license='License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'static_turtle_tf2_broadcaster = learning_tf2_py.static_turtle_tf2_broadcaster:main',
        'turtle_tf2_broadcaster = learning_tf2_py.turtle_tf2_broadcaster:main',
        'turtle_tf2_listener = learning_tf2_py.turtle_tf2_listener:main',
        'turtle_tf2_controller= learning_tf2_py.turtle_tf2_controller:main',
        'turtle_tf2_constant_dist= learning_tf2_py.turtle_tf2_constant_dist:main',
        ],
    },
)
