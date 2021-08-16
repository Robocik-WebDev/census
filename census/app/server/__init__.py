from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('server.config.Config')
db = SQLAlchemy(app)
