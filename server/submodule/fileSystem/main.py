from flask import Flask, request
from flask.views import MethodView

from pathlib2 import Path

import os
import json
import logging

app = Flask(__name__)
module_name    = "fileSystem"
module_conf    = {}
#module_mode    = 'DEBUG' #'RELEASE'
module_mode    = 'RELEASE'

module_debug_path   = '/Users/hexueyuan/workroot/github/smws/test/fileSysMountPoint'
module_release_path = str(Path.home())

class FileSystem(MethodView):
    def get(self):
        if module_mode == "DEBUG":
            #p = os.path.join(module_debug_path, request.args.get('path', '/'))
            p = module_debug_path + request.args.get('path', '/')
        else:
            #p = os.path.join(module_release_path, request.args.get('path', '/'))
            p = module_release_path + request.args.get('path', '/')
        print p
        path = Path(p)

        if not path.exists():
            return "Not Found", 404
        
        if path.is_dir():
            return self.file_list(path)
        else:
            return self.file_content(path)

    def post(self):
        post_data = request.data
        data = json.loads(post_data)

        if not data.has_key('path') or not data.has_key('type'):
            return 'Bad Request:key', 400
        else:
            if module_mode == "DEBUG":
                p = os.path.join(module_debug_path, data['path'])
            else:
                p = os.path.join(module_release_path, data['path'])
            path = Path(p)

        try:
            if data['type'] == "directory":
                path.mkdir()
            elif data['type'] == "file":
                with path.open(mode='w') as f:
                    f.write(data.get('content', ''))
            else:
                return "Bad Request:type", 400
        except Exception:
            return "server error:Unknown exception", 500

    def file_list(self, path):
        prefix = module_debug_path if module_mode == 'DEBUG' else module_release_path
        items = []
        if str(path) != module_release_path:
            items.append({
                'name': '..',
                'path': str(path.parent).replace(prefix, ''),
                'type': 'directory'
            })
        for subPath in path.iterdir():
            item = {
                'name': subPath.name,
                'path': str(subPath).replace(prefix, '')
            }
            if subPath.is_dir():
                item['type'] = 'directory'
            else:
                item['type'] = 'file'
            items.append(item)
        return json.dumps(items)

    def file_content(self, path):
        return 'test'

app.add_url_rule('/' + module_name, view_func=FileSystem.as_view(module_name))

def run(name, dashboard):
    app.run(port=8082)

if __name__ == "__main__":
    run('fileSystem', None)