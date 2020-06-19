from setuptools import setup

setup(
    name='amieclient',
    version='0.1',
    packages=['amieclient'],
    install_requires=[
        'requests>=2.23.0',
        'python-dateutil>=2.8.1'
    ],
    author='G. Ryan Sablosky',
    author_email='sablosky@psc.edu',
    python_requires=">=3.5",
)
