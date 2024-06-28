# hook-pyserial.py

from PyInstaller.utils.hooks import copy_metadata

datas = copy_metadata('pyserial')
