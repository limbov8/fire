from sqlalchemy.sql import func
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property , hybrid_method

db = SQLAlchemy()
