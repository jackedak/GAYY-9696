from setuptools import setup
from Cython.Build import cythonize

setup(
    name='GAYY-9696',
    ext_modules=cythonize("main.py"),
)
