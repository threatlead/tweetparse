from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tweetparse',
    version='0.1',
    description='Twitter Parser',
    long_description=readme,
    author='threatlead',
    author_email='threatlead@gmail.com',
    url='https://github.com/threatlead/',
    license=license,
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'requests_html',
        'fake-useragent',
    ],
)
