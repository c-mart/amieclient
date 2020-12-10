from setuptools import setup, find_packages

setup(
    name='amieclient',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0,<3',
        'python-dateutil>=2.6.1,<2.7'
    ],
    author='G. Ryan Sablosky',
    author_email='sablosky@psc.edu',
    python_requires=">=3.5",
)
