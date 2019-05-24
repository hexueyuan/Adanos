from flask import request, jsonify
from flask.views import MethodView

from pathlib2 import Path
from common import Result

from .. import dashboard
from . import fileMonitor

import json
import shutil
import os

name = 'fileMonitor'
config = dashboard.getPlugin(name, 'config')
root = config.get('root', "~")
if root == "~":
    root = str(Path.home())

class FileMonitorView(MethodView):
    def get(self):
        path = Path(root + request.args.get('path', '/'))

        if not path.exists():
            return "Not Found", 404
        
        if path.is_dir():
            return self.file_list(path)
        else:
            return self.file_content(path)

    def post(self):
        if not request.args.has_key('path') or not request.args.has_key('type'):
            return 'Bad Request:key', 400
        else:
            path = Path(root + '/' + request.args['path'])

        try:
            print str(path)
            if request.args['type'] == "folder":
                path.mkdir()
                return jsonify(Result({}).dump())
            elif request.args['type'] == "file":
                with path.open(mode='w') as f:
                    f.write(request.data.decode('utf-8'))
                return jsonify(Result({}).dump())
            else:
                return "Bad Request:type", 400
        except Exception:
            return "server error:Unknown exception", 500

    def put(self):
        if not request.args.has_key('path') or not request.args.has_key('type'):
            return 'Bad Request:key', 400
        if request.args['type'] == "move":
            oldPath = request.args['path']
            newPath = request.json.get('newPath')
            if not os.path.exists(root + oldPath):
                return "bad Request:path", 400
            else:
                shutil.move(root + oldPath, root + newPath)
                return jsonify(Result({}).dump())
        elif request.args['type'] == "update":
            return "debug", 404
        else:
            return "Bad Request:type", 400

    def delete(self):
        if not request.args.has_key('path') or not request.args.has_key('type'):
            return 'Bad Request:key', 400
        if request.args['type'] == "file" and os.path.isfile(root + request.args['path']):
            os.remove(root + request.args['path'])
            return jsonify(Result({}).dump())
        elif request.args['type'] == "directory" and os.path.isdir(root + request.args['path']):
            shutil.rmtree(root + request.args['path'])
            return jsonify(Result({}).dump())
        else:
            return "Bad request", 400

    def file_list(self, path):
        items = []
        if str(path) != root:
            items.append({
                'name': '..',
                'path': str(path.parent).replace(root, ''),
                'type': 'directory'
            })
        for subPath in path.iterdir():
            item = {
                'name': subPath.name,
                'path': str(subPath).replace(root, '')
            }
            if subPath.is_dir():
                item['type'] = 'directory'
            else:
                item['type'] = 'file'
            items.append(item)
        return json.dumps(items)

    def file_content(self, path):
        with open(str(path)) as f:
            return f.read()

fileMonitor.add_url_rule('/' + name, view_func=FileMonitorView.as_view(name))