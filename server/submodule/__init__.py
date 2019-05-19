from flask import Flask, current_app
from flask_socketio import SocketIO

socketio = SocketIO()
dashboard = None

__all__ = ['socketio', 'create_app', 'setDashboard']

def create_app():
    global dashboard
    config = dashboard.getPlugin('main', 'config')

    app = Flask(__name__)
    app.debug = (config.get('mode') == 'debug')

    app.extensions['dashboard'] = dashboard

    from .fileMonitor import fileMonitor
    app.register_blueprint(fileMonitor)
    from .www import Adanos
    app.register_blueprint(Adanos)
    import dataWatcher

    socketio.init_app(app)

    return app

def getDashboard():
    global dashboard
    return dashboard

def setDashboard(db):
    global dashboard
    dashboard = db