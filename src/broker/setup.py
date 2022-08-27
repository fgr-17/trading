from setuptools import find_packages, setup  

setup(
    name="broker", 
    version="1.0.0", 
    description="Broker wrapper for pyhomebroker", 
    package_dir={"": "."}, 
    packages=find_packages(where="."), 
)