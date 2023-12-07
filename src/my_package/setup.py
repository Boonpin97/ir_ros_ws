from setuptools import find_packages, setup

package_name = 'my_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='arms',
    maintainer_email='arms@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = my_package.my_node:main',
	    'talker = my_package.publisher_member_function:main',
	    'listener = my_package.subscriber_member_function:main',
	    'talker2 = my_package.assignment_pub:main',
	    'listener2 = my_package.assignment_sub:main',
	    'server = my_package.add_three_ints_server:main',
	    'client = my_package.add_three_ints_client:main',
	    'server2 = my_package.time_request_server:main',
	    'client2 = my_package.time_request_client:main',
        ],
    },
)
