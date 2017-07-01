from setuptools import setup


setup(
    name='photo_migrator',
    version='0.1',
    py_modules=['photo_migrator'],
    install_requires=[
        'click',
    ],
    entry_points={
        "console_scripts": [
            "photom=photo_migrator.cli:main",
        ],
    },
)
