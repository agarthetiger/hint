from setuptools import setup

setup(
    name='hint',
    version='0.1',
    py_modules=['hint'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hint=hint:cli
    ''',
)
