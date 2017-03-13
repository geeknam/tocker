from setuptools import setup

dependencies = [
    'testinfra', 'pytest', 'docker-py'
]

setup(
    name='tocker',
    version='0.2',
    packages=['tocker'],
    license='The MIT License (MIT)',
    author='Nam Ngo',
    author_email='namngology@gmail.com',
    description='TDD for Docker',
    keywords='docker tdd testing test container',
    install_requires=dependencies,
    test_suite='tocker.test',
    entry_points={
        'pytest11': [
            'tocker = tocker.fixtures',
        ]
    },
)
