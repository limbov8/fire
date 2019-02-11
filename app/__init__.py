from flask import render_template

from lib.utils.update import update_context

from .models import db
from .assets import create_assets
from .jobs import rq_instance

def init_app(app, csrf, assets):
    with app.app_context():
        app.jinja_env.add_extension('jinja2.ext.do')
        create_assets(assets)
        db.init_app(app)
        rq_instance.init_app(app)
        update_context(app, {"db": db, "assets": assets, "rq_instance": rq_instance})

def internal_render():
    if internal_render.page:
        return render_template(internal_render.page)
    else:
        return render_template('error/404.html', title='Page Not Found'), 404

__all__ = [
    'init_app',
    'internal_render'
]