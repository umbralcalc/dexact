from setuptools import setup, find_packages

setup(
    name="dexact",
    version="0.1.4",
    author="Robert J. Hardwick",
    author_email="umbralcalc@gmail.com",
    description="A very simple Python package which provides the necessary tools to interact with dexetera",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/umbralcalc/dexact",
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