from setuptools import setup, find_packages

setup(
    name="dexact",
    version="0.1.1",
    author="Robert J. Hardwick",
    author_email="umbralcalc@gmail.com",
    description="A very simple Python package which provides the necessary tools to interact with dexetera",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/umbralcalc/dexetera",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "websockets",
        "protobuf",
    ],
)