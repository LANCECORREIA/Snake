from distutils.core import setup
import py2exe

setup(
    console=['snake.py'],
    packages=['Font', 'Sound', 'Graphics']
)
