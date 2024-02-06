from setuptools import setup, find_packages

setup(
    name='pf',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'ratelimit',
    ],
    entry_points={
        'console_scripts': [
            'pf = pf.main:main'
        ]
    },
    url='https://github.com/pyscr1pt3r/pf',
    license='MIT',
    author='pyscr1pt3r',
    author_email='',
    description='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)