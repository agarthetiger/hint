from setuptools import setup, find_packages

setup(
    name='hint-cli',
    version='0.11.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'gitpython',
        'pygments',
    ],
    entry_points={
        'console_scripts': [
            'hint = hint_cli.hint:cli_entrypoint',
        ],
    },
)
