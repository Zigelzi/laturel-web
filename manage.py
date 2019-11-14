from flask.cli import FlaskGroup

from laturel import app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()

# This is a test