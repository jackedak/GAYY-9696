from setuptools import setup, find_packages

setup(
    name="gayybot",
    version='0.6.9',
    packages=find_packages(),
    install_requires=['pycord'],
    entry_points={
        "console_scripts": [
            "gayybot = gayybot.main:main"
        ]
    }
)


