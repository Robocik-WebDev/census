import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = \
        'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'.format(
            dbuser=os.environ['POSTGRES_USER'],
            dbpass=os.environ['POSTGRES_PASSWORD'],
            dbhost=os.environ['SQL_HOST'],
            dbport=os.environ['SQL_PORT'],
            dbname=os.environ['POSTGRES_DB']
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
