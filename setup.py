from setuptools import setup, find_packages

setup(
    name='paramfinder',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
        'ratelimit',
    ],
    entry_points={
        'console_scripts': [
            'paramfinder = paramfinder.main:main'
        ]
    },
    url='https://github.com/cyberduck404/paramfinder',
    license='MIT',
    author='cyberduck404',
    author_email='',
    description='Dig parameters from wayback machine',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)