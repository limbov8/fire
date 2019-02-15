from sqlalchemy.sql import func
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property , hybrid_method

db = SQLAlchemy()

def get_mongo_connection():
    try:
        from flask import current_app
        return current_app.MONGODB_DATABASE_URI
    except Exception as e:
        from config import app_config
        return app_config['production'].MONGODB_DATABASE_URI

def get_postgre_connection():
    try:
        from flask import current_app
        return current_app.SQLALCHEMY_DATABASE_URI
    except Exception as e:
        from config import app_config
        return app_config['production'].SQLALCHEMY_DATABASE_URI

def get_db_session_instance():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(get_postgre_connection()).connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# class Blog(db.Model):
#     __tablename__='blog'
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
