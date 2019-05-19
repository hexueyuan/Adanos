from flask import Blueprint

fileMonitor = Blueprint('fileMonitor', __name__)

from . import main

__all__ = ['fileMonitor']