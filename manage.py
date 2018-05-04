import sys
from os import environ, path
from brigade import create_app
from flask_script import Manager, Server

# grab environment variables from the .env file if it exists
if path.exists('.env'):
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2 and not var[0].startswith('#'):
            environ[var[0]] = var[1]

app = create_app()
manager = Manager(app)
manager.add_command('runserver', Server(host='localhost', port='4000', use_debugger=True))


@manager.command
def runtests():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    runner = unittest.TextTestRunner(verbosity=1).run(tests)

    if len(runner.errors) or len(runner.failures):
        sys.exit(1)


if __name__ == '__main__':
    manager.run()
