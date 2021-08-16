#!/usr/bin/env python3
from flask.cli import FlaskGroup
from server.utils import send_file
from server import app


cli = FlaskGroup(app)


@app.route('/<path:path>')
def static_file(path):
    return send_file(path)


@app.route('/')
def root():
    return send_file('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cli()
