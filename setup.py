from setuptools import setup, find_packages

setup(
    name="python-extended-stats",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click",
        "pytest",
        "radon",
        "vulture"
    ],
    entry_points={
        "console_scripts": [
            "python-extended-stats=python_ext_stats.main:main",
        ],
    },
)
