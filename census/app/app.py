#!/usr/bin/env python3
import sqlalchemy
from sqlalchemy.sql.expression import false
import jwt
import datetime
from functools import wraps
from flask.cli import FlaskGroup
from server.utils import send_file
from server import app, salt_password, execute_query
from flask import Flask, jsonify, request, make_response


def decode_token(token):
    return jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256", verify=True)


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.json['token']
        if not token:
            return {'WWW-Authenticate': 'Missing token!'}, 403
        data = decode_token(token)
        return func(*args, **kwargs)
    return wrapped


cli = FlaskGroup(app)


@app.route('/<path:path>')
def static_file(path):
    return send_file(path)


@app.route('/')
def root():
    return send_file('index.html')


@app.post('/api/census/login')
def login():
    request_msg = request.json
    if 'mail' in request_msg and 'password' in request_msg:
        mail = request_msg['mail']
        password = request_msg['password']
        query = sqlalchemy.text(f"SELECT u.id, u.name, u.last_name\
            FROM users u INNER JOIN mail m on u.id = m.user_id\
            WHERE m.address = '{mail}' AND u.password = '{salt_password(password)}';")
        result = execute_query(query).first()
        if(result == None):
            return {'WWW-Authenticate': 'Login error'}, 401
        else:
            token = jwt.encode({
                'user_id': result[0],
                'name': f'{result[1]}',
                'last_name': f'{result[2]}',
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return {'token': token}, 200
    return {'WWW-Authenticate': 'Login required'}, 401


@app.post('/api/census/auth')
@check_for_token
def auth():
    return {'Message': 'Good'}, 200


@app.post('/api/census/user/password')
@check_for_token
def change_password():
    data = decode_token(request.json['token'])
    query = sqlalchemy.text(f"SELECT id FROM users\
         WHERE id = {data['user_id']} AND password = '{salt_password(request.json['old_password'])}'")
    if execute_query(query).first() == None:
        return {'message': 'Bad password!'}, 402
    else:
        query = sqlalchemy.text(f"UPDATE users\
             SET password = '{salt_password(request.json['new_password'])}'\
             WHERE id = {data['user_id']}")
        execute_query(query)
        return {'message': 'Password changed'}, 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    cli()
