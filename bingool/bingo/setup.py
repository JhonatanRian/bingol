from distutils.core import setup
from Cython.Build import cythonize

modules = ['cbingo.pyx']

setup(
    ext_modules=cythonize(modules),
    name="cbingo",
    description="bingo orientado a objeto.",

)