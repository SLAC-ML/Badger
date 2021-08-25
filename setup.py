from setuptools import setup, find_packages

setup(
    name='badger-opt',
    version='0.1',
    description='Core of the Badger optimizer',
    url='https://github.com/SLAC-ML/Badger',
    author='Zhe Zhang',
    author_email='zhezhang@slac.stanford.edu',
    license='GPL',
    package_dir={'': 'badger'},
    packages=find_packages(where='badger'),
    install_requires=[
        'numpy',
        'pyyaml'
    ],
    python_requires='>=3.6',
)
