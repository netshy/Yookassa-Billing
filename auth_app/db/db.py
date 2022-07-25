from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

sql_db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    sql_db.init_app(app)
    migrate.init_app(app, sql_db)
