from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PSPhasor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.20.0",
        "matplotlib>=3.4.0",
    ],
    author="Ahmed M. Elkholy",
    author_email="ahm_elkholy@outlook.com",
    description="A powerful Python tool for creating phasor diagrams in electrical engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmelkholy/PSPhasor.git",
    project_urls={
        "Bug Tracker": "https://github.com/ahmelkholy/PSPhasor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
)
