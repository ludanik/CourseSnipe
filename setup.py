import setuptools
# PyPi upload Command
# rm -r dist
# python3 -m build --sdist
# python -m twine upload dist/*

setuptools.setup(
    name="CourseSnipe",
    packages=setuptools.find_packages(),
    version="1.0.4",
    license="MIT",
    description="CLI utility for automated enrollment with REM",
    author="Ian Ludanik",
    url="https://github.com/ludanik/CourseSnipe",
    install_requires=[
        "selenium",
        "Click",
        "python-dotenv",
        "webdriver_manager"
    ],
    entry_points={
        'console_scripts': [
            'csnipe = CourseSnipe.main:cli',
        ],
    },
    )
