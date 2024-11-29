from glob import glob
from setuptools import setup

package_name = "forward_position_controller"

setup(
    name=package_name,
    version="2.33.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name, glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*.*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="Denis Štogl",
    author_email="denis@stogl.de",
    maintainer="Denis Štogl",
    maintainer_email="denis@stogl.de",
    keywords=["ROS"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    description="Demo nodes for showing and testing functionalities of ros2_control framework.",
    long_description="Demo nodes for showing and testing functionalities of the ros2_control framework.",
    license="Apache License, Version 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "publisher_forward_position_controller = forward_position_controller.publisher_forward_position_controller:main",
        ],
    },
    scripts=[
        'forward_position_controller/publisher_forward_position_controller.py'
    ],
)
