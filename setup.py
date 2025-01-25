from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blaze-cicd",
    version="0.1.0",
    description="A CLI tool for managing CI/CD pipelines with Docker, GitHub, and ArgoCD.",
    author="Ahmed Rakan",
    author_email="ar.aldhafeeri11@gmail.com",
    packages=find_packages(where="src"),  # Find packages in the `src` directory
    package_dir={"": "src"},  # Specify the root of the packages
    install_requires=[
        "requests>=2.31.0", 
        "PyYAML>=6.0.0",  
    ],
    entry_points={
        "console_scripts": [
            "blazer=blaze_cicd.cli:main", 
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True, 
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8", 
    project_urls={
        "Source": "https://github.com/yourusername/blaze-cicd",
        "Bug Reports": "https://github.com/araldhafeeri/blaze-cicd/issues",
    },
)