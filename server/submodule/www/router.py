from . import Adanos
from flask import render_template

@Adanos.route('/', methods=['GET'])
def index():
    return render_template('index.html')