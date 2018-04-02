from setuptools import setup, find_packages

setup(
    name = 'boi',
    version = '0.1',
    description = 'Command line interface for getting Binding of Isaac information.',
    packages = ['boi'],
    entry_points = {
        'console_scripts': ['boi=boi.__main__:boi']
    },
    include_package_data = True
)