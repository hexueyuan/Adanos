# -*- coding: utf-8 -*-

from flask import Flask
import markdown2

import sys

app = Flask(__name__)
file = ''

def generate_html_content(path):
    with open(path, 'r') as f:
        mdContent = f.read()
        try:
            html = markdown2.markdown(mdContent.decode('utf-8'), extras=['fenced-code-blocks'])
        except:
            return 'Server Error:markdown convert fail.'
    return html

@app.route('/', methods=['GET'])
def index():
    if file == '':
        return '', 404
    else:
        return generate_html_content(file)

@app.route('/<path:path>', methods=['GET'])
def staticfile(path):
    with open(path, 'r') as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "bad argv"
    else:
        file = sys.argv[1]
    app.run(host='0.0.0.0', port=5051)