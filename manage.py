import os
from server.app import app
from flask_script import Manager, Shell
from scrapper.recipes import TudoGostoso, TudoReceitas

basedir = os.path.abspath(os.path.dirname(__file__))

manager = Manager(app)

def make_shell_context():
    return dict(TudoGostoso=TudoGostoso, TudoReceitas=TudoReceitas, app=app)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
