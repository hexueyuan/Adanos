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
elif root == '/':
    root = ''
if root[-1] == '/':
    root = root[:-1]

httpMsg = {
    400: 'Bad Request',
    404: 'Not Found',
    500: 'Server Error'
}

def httpResponse(code):
    return httpMsg.get(code, 'unknown code'), code

def realPath(path):
    return os.path.join(root, path)

def mergePath(first, second):
    if first[-1] == '/':
        first = first[:-1]
    if second[0] != '/':
        second = '/' + second
    return first + second

class FileMonitorView(MethodView):
    def ls(self, dir):
        if dir[-1] == '/':
            dir = dir[:-1]
        rv = []
        if dir != root:
            rv.append({
                'name': '..',
                'path': os.path.dirname(dir).replace(root, '') + '/',
                'type': 'folder'
            })
        for subPath in Path(dir).iterdir():
            rv.append({
                'name': subPath.name,
                'path': str(subPath).replace(root, '') + ('/' if subPath.is_dir() else ''),
                'type': 'folder' if subPath.is_dir() else 'file'
            })
        return rv

    def cat(self, file):
        f = open(file, 'w')
        content = f.read()
        f.close()
        return content

    def get(self):
        logger = dashboard.getPlugin(name, 'logger')
        if not request.args.has_key('path') or not request.args.has_key('type'):
            logger.info('Client send a bad request. which path = {} and type = {}.'\
                .format(request.args.get('path'), request.args.get('type')))
            return httpResponse(400)
        else:
            pathStr = mergePath(root, request.args['path'])
            logger.info('GET path: ' + pathStr)

        if not Path(pathStr).exists():
            logger.info('Client request a nonexistent path:' + pathStr)
            return httpResponse(404)
        
        if request.args['type'] == "folder":
            dir = pathStr
            rv = Result({'record': self.ls(dir)})
            logger.info('Response subitems of folder, count={}.'.format(len(rv.record)))
            logger.debug(rv.dump())
            return jsonify(rv.dump())
        else:
            file = pathStr
            logger.info('Response content of file.')
            logger.debug(rv.record[:30] + '...')
            return jsonify(Result({'record': self.cat(file)}).dump())

    def post(self):
        logger = dashboard.getPlugin(name, 'logger')
        if not request.args.has_key('path') or not request.args.has_key('type'):
            logger.info('Client send a bad request. which path = {} and type = {}.'\
                .format(request.args.get('path'), request.args.get('type')))
            return httpResponse(400)
        else:
            pathStr = mergePath(root, request.args['path'])
            logger.info('POST path: ' + pathStr)

        if os.path.exists(pathStr):
            logger.info('POST but object is exists.')
            return jsonify(Result({'result': False, 'errmsg': 'Object is exists.'}).dump())

        if request.args['type'] == "folder":
            Path(pathStr).mkdir()
            logger.info('New folder is created.')
            return jsonify(Result({}).dump())
        elif request.args['type'] == "file":
            with open(pathStr ,'w') as f:
                f.write(request.data.decode('utf-8'))
            logger.info('New file is Created.')
            return jsonify(Result({}).dump())
        else:
            return httpResponse(400)

    def put(self):
        logger = dashboard.getPlugin(name, 'logger')
        if not request.args.has_key('path') or not request.args.has_key('type'):
            logger.info('Client send a bad request. which path = {} and type = {}.'\
                .format(request.args.get('path'), request.args.get('type')))
            return httpResponse(400)
        
        if request.args['type'] == "move":
            oldPath = mergePath(root, request.args['path'])
            newPath = mergePath(root, request.json.get('newPath'))
            logger.info('move {} to {}'.format(oldPath, newPath))
            if not os.path.exists(oldPath):
                logger.info('Source path is not exists.')
                return jsonify(Result({'result': False, 'errmsg': 'Object is not exists.'}).dump())
            else:
                shutil.move(oldPath, newPath)
                logger.info('Move successful.')
                return jsonify(Result({}).dump())
        elif request.args['type'] == "update":
            return httpResponse(404)
        else:
            logger.info('A unknown request type.')
            return httpResponse(400)

    def delete(self):
        logger = dashboard.getPlugin(name, 'logger')
        if not request.args.has_key('path') or not request.args.has_key('type'):
            logger.info('Client send a bad request. which path = {} and type = {}.'\
                .format(request.args.get('path'), request.args.get('type')))
            return httpResponse(400)
        if not request.args.has_key('path'):
            return httpResponse(400)
        pathStr = mergePath(root, request.args['path'])
        logger.info('DELETE path: ' + pathStr)

        if request.args['type'] == "file" and os.path.isfile(pathStr):
            os.remove(pathStr)
            logger.info('Delete file success.')
            return jsonify(Result({}).dump())
        elif request.args['type'] == "folder" and os.path.isdir(pathStr):
            shutil.rmtree(pathStr)
            logger.info('Delete folder success.')
            return jsonify(Result({}).dump())
        else:
            return httpResponse(400)

fileMonitor.add_url_rule('/' + name, view_func=FileMonitorView.as_view(name))