from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from project.models.base import db
from project.models.taxi import Taxi
from project.models.tick_tracker import Tick
import markdown
import markdown.extensions.fenced_code
DEFAULT_TAXI_COUNT=3
app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple_taxi.sqlite'
db.init_app(app)
from project.routes import taxi_booking_routes

##Let's create the DB if it's not created yet
with app.app_context():
    if not db.engine.dialect.has_table(db.engine, "taxis"):
        Taxi.__table__.create(db.engine)
        for _ in range(0, DEFAULT_TAXI_COUNT):
            Taxi((0,0))

    if not db.engine.dialect.has_table(db.engine, "tick"):
        Tick.__table__.create(db.engine)
        Tick()

##end DB check

@app.route("/")
def index():
    """This will just load the README.md at the index

    Returns:
        README -- render of the README.md
    """
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string

