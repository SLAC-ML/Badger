from setuptools import setup, find_packages

setup(
    name='badger-opt',
    version='0.5.0',
    description='Core of the Badger optimizer',
    url='https://github.com/SLAC-ML/Badger',
    author='Zhe Zhang',
    author_email='zhezhang@slac.stanford.edu',
    license='GPL',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'badger': ['gui/images/*.png']
    },
    install_requires=[
        'pandas',
        'pyyaml',
        'coolname',
        'pyqt5',
        'pyqtgraph',
        'qdarkstyle',
        'pillow'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'badger = badger.__main__:main'
        ]
    },
)
