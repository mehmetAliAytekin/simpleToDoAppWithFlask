from flask import Flask, session
from application.models import db, User, ToDo, db
from flask_sessionstore import Session
import redis

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_to_do.db"
db.init_app(app)
SECRET_KEY = '123456789012345678901234'
SESSION_TYPE = 'redis'
SESSION_REDIS = redis.from_url('redis://localhost:6379')

app.config.from_object(__name__)
Session(app)

with app.app_context():
    db.create_all()

import application.views
