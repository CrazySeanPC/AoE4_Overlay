import json
import os
import pathlib
import sys

import requests
from PyQt5 import QtCore

from overlay.logging_func import get_logger

logger = get_logger(__name__)
ROOT = pathlib.Path(sys.argv[0]).parent.absolute()


def pyqt_wait(miliseconds: int):
    """ Pause executing for `time` in miliseconds"""
    loop = QtCore.QEventLoop()
    QtCore.QTimer.singleShot(miliseconds, loop.quit)
    loop.exec_()


def is_compiled() -> bool:
    """ Checks whether the app is compiled by Nuitka"""
    return '__compiled__' in globals()


def file_path(file: str) -> str:
    """ Returns the path to the main directory regardless of the current working directory """
    return os.path.normpath(os.path.join(ROOT, file))


def version_to_int(version: str):
    """Convets `1.0.1` to an integer """
    return sum([
        int(i) * (1000**idx) for idx, i in enumerate(version.split('.')[::-1])
    ])


def version_check(version: str) -> str:
    """ Checks version. Returns either link for the new version or an empty string. """
    try:
        url = "https://raw.githubusercontent.com/FluffyMaguro/AoE4_Overlay/main/version.json"
        data = json.loads(requests.get(url).text)
        if version_to_int(version) < version_to_int(data['version']):
            return data['link']
    except Exception:
        logger.warning("Failed to check for a new version")
    return ""


def create_custom_files():
    """ Creates custom.css and custom.js files if they don't exist"""
    for file_name in ("custom.css", "custom.js"):
        path = file_path(f"html/{file_name}")
        if not os.path.isfile(path):
            with open(path, "w") as f:
                f.write("")