from os import environ, path
from brigade import create_app
from flask.ext.script import Manager, Server

# grab environment variables from the .env file if it exists
if path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            environ[var[0]] = var[1]

app = create_app(environ)
manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port='4000', use_debugger=True))

@manager.command
def runtests():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=1).run(tests)

if __name__ == '__main__':
    manager.run()
