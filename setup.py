import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MTConnect",
    version="0.2.2",
    author="Michael Honaker",
    author_email="mchonaker@gmail.com",
    description="A python agent for MTConnect",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HonakerM/MTConnect-Python-Agent",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
