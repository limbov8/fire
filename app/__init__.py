from flask import render_template
from .models import db
from .assets import create_assets

def init_app(app, csrf, assets):
    app.jinja_env.add_extension('jinja2.ext.do')
    create_assets(assets)
    with app.app_context():
        db.init_app(app)

def internal_render(page):
    return render_template(page)

__all__ = [
    'init_app',
    'internal_render'
]