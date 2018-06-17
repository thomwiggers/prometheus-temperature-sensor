from setuptools import setup, find_packages


setup(
    name="prometheus_temp_sensor",
    version="0.1",
    packages=['measure'],
    entry_points={
        'console_scripts': [
            'tempmon = measure:run',
        ],
    },
    install_requires=[
        'prometheus_client',
        'w1',
    ],
)
