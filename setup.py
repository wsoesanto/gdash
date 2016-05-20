from setuptools import setup

setup(
    name="gdash",
    version="0.0.a1",
    author="Willy",
    author_email="opelhoward@yahoo.com",
    packages=["gdash"],
    license="LICENSE",
    description='Gluster Dashboard',
    requires=['requests', 'flask']
)
