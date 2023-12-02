from setuptools import setup

setup(
    name='CourseSnipe',
    version='0.1.0',
    py_modules=['CourseSnipe'],
    install_requires=[
        'Click',
        'selenium',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'main = main:cli',
        ],
    },
)