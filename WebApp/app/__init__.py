from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)

logging.basicConfig(level=logging.DEBUG)


from app import views, models
