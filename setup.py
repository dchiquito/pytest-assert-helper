from setuptools import setup, find_packages

setup(
    author="Daniel Chiquito",
    author_email="daniel.chiquito@kitware.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
    ],
    license="Apache Software License 2.0",
    include_package_data=True,
    name="pytest_assert_helper",
    packages=find_packages(exclude=["test", "test.*"]),
    version="0.1.0",
    zip_safe=False,
)
