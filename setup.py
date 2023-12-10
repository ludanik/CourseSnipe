import setuptools

# PyPi upload Command
# rm -r dist ; python setup.py sdist ; python -m twine upload dist/*

setuptools.setup(
    name="CourseSnipe",
    packages=setuptools.find_packages(),
    version="1.0.0",
    license="MIT",
    description="CLI utility for automated enrollment with REM",
    author="Ian Ludanik",
    url="https://github.com/ludanik/CourseSnipe",
    install_requires=[
        "selenium",
        "click",
        "python-dotenv"
    ],
    ]
