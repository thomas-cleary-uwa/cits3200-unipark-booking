"""
script to run a fresh version of the application

NOTE: Run this when you are in /flask-app, NOT /run
(path variables are set for this)

Authors: Thomas Cleary,

"""

import os
import subprocess


def make_fresh_db():
    """ create a fresh instance of the database """
    commands = [
        'rm db-dev.sqlite',
        'flask db migrate',
        'flask db upgrade',
        'flask run'
    ]

    if not os.path.exists('db-dev.sqlite'):
        commands = commands[1:]

    for cmd in commands:
        try:
            print("\n", cmd, sep="")
            exit_value = subprocess.run(cmd.split(), check=True)
            print("Exit Value: {}".format(exit_value))

        except subprocess.CalledProcessError as error:
            print("Error: {}".format(error))

    print() # final newline

def main():
    """
    delete db-dev.sqlite
    create new db.dev.sqlite
    """

    make_fresh_db()


if __name__ == "__main__":
    main()
