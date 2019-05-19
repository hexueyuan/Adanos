from flask import Blueprint

Adanos = Blueprint('Adanos', __name__)

from . import router

__all__ = ['Adanos']