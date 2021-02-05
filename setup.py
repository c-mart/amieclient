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
    python_requires='>=3.5',
    description='Library for the XSEDE AMIE REST API.',
    license='Apache Software License v2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
