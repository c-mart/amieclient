from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='amieclient',
    version='0.5.1',
    packages=find_packages(),
    install_requires=[
        'requests>=2.20.0,<3',
        "python-dateutil>=2.6.1,<2.7;python_version<'3.7'",
        "python-dateutil>=2.8.1,<2.9;python_version>='3.7'"
    ],
    extras_require={
        'tests': ['requests-mock>=1.9.3,<1.10.0']
    },
    author='G. Ryan Sablosky',
    author_email='sablosky@psc.edu',
    python_requires='>=3.5,<3.10',
    description='Library for the XSEDE AMIE REST API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache Software License v2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Documentation & Examples': 'https://xsede.github.io/amieclient/',
        'Source': 'https://github.com/xsede/amieclient/',
        'Tracker': 'https://github.com/xsede/amieclient/issues',
    },
)
