import sys

from os import path
from setuptools import setup
from wheel.bdist_wheel import bdist_wheel

base_dir = path.dirname(__file__)
src_dir = path.join(base_dir, 'pyvips')

# When executing the setup.py, we need to be able to import ourselves, this
# means that we need to add the pyvips/ directory to the sys.path.
sys.path.insert(0, src_dir)

# Try to install in API mode first, then if that fails, fall back to ABI

# API mode requires a working C compiler plus all the libvips headers whereas
# ABI only needs the libvips shared library to be on the system


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith('cp'):
            # on CPython, our wheels are abi3 and compatible back to 3.7
            return 'cp37', 'abi3', plat

        return python, abi, plat


try:
    setup(
        cffi_modules=['pyvips/pyvips_build.py:ffibuilder'],
        cmdclass={'bdist_wheel': bdist_wheel_abi3},
    )
except Exception as e:
    print('Falling back to ABI mode. Details: {0}'.format(e))
    setup()
