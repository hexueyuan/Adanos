from flask import request
from flask.views import MethodView

from pathlib2 import Path

from .. import dashboard
from . import fileMonitor

import json

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
        post_data = request.json_data()

        if not post_data.has_key('path') or not post_data.has_key('type'):
            return 'Bad Request:key', 400
        else:
            path = Path(root + post_data['path'])

        try:
            if post_data['type'] == "directory":
                path.mkdir()
            elif post_data['type'] == "file":
                with path.open(mode='w') as f:
                    f.write(post_data.get('content', ''))
            else:
                return "Bad Request:type", 400
        except Exception:
            return "server error:Unknown exception", 500

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