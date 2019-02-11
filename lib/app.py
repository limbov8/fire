from flask import Flask, Blueprint, render_template
from flask_wtf import CSRFProtect
from flask_assets import Environment

from config import app_config, routes
from .route import Route
import app as user_app

def create_app(config_name):
    app_name = app_config[config_name].APP_NAME or __name__
    app = Flask(app_name)
    app.config.from_object(app_config[config_name])

    csrf = CSRFProtect()
    csrf.init_app(app)

    assets = Environment(app)

    app.static_folder = 'public'
    
    blueprint = Blueprint('public', 'public', static_url_path='/public', static_folder='public')
    app.register_blueprint(blueprint)
    blueprint = Blueprint('app', 'app', template_folder='templates')
    app.register_blueprint(blueprint)

    rt = Route(routes)
    rt.init_app(app)

    user_app.init_app(app, csrf, assets)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('error/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template('error/500.html', title='Server Error'), 500

    return app