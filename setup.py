from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pathfinder-web",
    version="1.0.0",
    description="A lightning-fast web reconnaissance tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zeeshan01001",
    author_email="author@example.com",
    url="https://github.com/Zeeshan01001/pathfinder",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'pathfinder_web': ['wordlists.txt'],
    },
    install_requires=[
        "aiohttp>=3.8.0",
        "rich>=12.0.0",
        "requests>=2.28.0",
        "dnspython>=2.2.0",
    ],
    entry_points={
        "console_scripts": [
            "pathfinder=pathfinder_web.pathfinder:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
) 