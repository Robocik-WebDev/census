import re
import click
import sqlalchemy
import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import choice, randint

app = Flask(__name__)
app.config.from_object('server.config.Config')
db = SQLAlchemy(app)


def execute_query(query):
    conn = db.engine.connect()
    return conn.execute(query)


def email_exists(email):
    query = sqlalchemy.text(f"SELECT count(id) FROM mail WHERE address = '{email}'")
    if execute_query(query).first()[0] > 0:
        return True
    else:
        return False


def add_email(user_id, email):
    query = sqlalchemy.text(f"INSERT INTO mail (address, user_id) VALUES\
         ('{email}', '{user_id}') returning id;")
    return execute_query(query)


def salt_password(password):
    salt = app.config['PASSWORD_SALT']
    salted_password = hashlib.sha512(password.encode(
        'utf-8') + salt.encode('utf-8')).hexdigest()
    return salted_password

def insert_user(password, name, last_name):
    query = sqlalchemy.text(f"INSERT INTO users (name, last_name, password)\
         VALUES ('{name}', '{last_name}', '{salt_password(password)}') returning id;")
    return execute_query(query)


def set_primary_mail(user_id, email_id):
    query = sqlalchemy.text(
        f"UPDATE users SET primary_mail_id = {email_id} WHERE id = {user_id};")
    return execute_query(query)


def addUser(email, password, name, last_name):
    if email_exists(email):
        return False
    else:
        user_id = insert_user(password, name, last_name).first()[0]
        mail_id = add_email(user_id, email).first()[0]
        set_primary_mail(user_id, mail_id)
        return True


def execute_sql_file(filename):
    engine = db.engine
    with engine.connect() as con:
        sql_file = open(f'server/{filename}.sql', 'r')
        escaped_sql = sqlalchemy.text(sql_file.read())
        con.execute(escaped_sql)


@app.cli.command('createdb')
def create_db():
    """Creates database by running `flask createdb`"""
    execute_sql_file('schema')
    print()


@app.cli.command('adduser')
@click.argument('email', nargs=1)
@click.argument('password', nargs=1)
@click.argument('name', nargs=1)
@click.argument('last_name', nargs=1)
def addCLIUser(email, password, name, last_name):
    if addUser(email, password, name, last_name):
        click.echo("Success")
    else:
        click.echo("Error")
