from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from sqlalchemy import inspect

from app.settings.constants import DB_URL
from app.core import db
from app.models.actor import Actor
from app.models.movie import Movie


from datetime import datetime as dt
from app.controllers.movie import *


app = Flask(__name__, instance_relative_config=False)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db.init_app(app)

with app.app_context():
    db.create_all()
    print(get_all_movies())
    print(get_movie_by_id())
    print(add_movie())
    print(update_movie())
    print(movie_add_relation())
    print(movie_clear_relations())
    print(delete_movie())

