import importlib
from flask import Blueprint
from app import internal_render
class RouteSettingException(Exception):
    def __init__(self, message):
        super(RouteSettingException, self).__init__(message)
        
class Route():
    def __init__(self, routes):
        self.routes = routes
        
    def init_app(self, app):
        for url, settings in self.routes.items():
            url = url.strip()
            if len(url) < 1:
                raise RouteSettingException('URL can not be empty, for nothing please use / instead')
            if url[0] != '/':
                url = '/' + url

            scope = False
            if 'scope' in settings:
                scope = settings['scope']

            if scope:
                module = None
                _app_name = None
                if 'app' in settings:
                    _app_name = settings['app']
                    module = importlib.import_module('app.' + settings['app'] + '.controllers', 'fire')
                if 'suffix' not in settings:
                    raise RouteSettingException('Nothing in route ' + url)
                for suffix, sub_settings in settings['suffix'].items():
                    suffix = suffix.strip()
                    if len(suffix) < 1:
                        raise RouteSettingException('URL suffix can not be empty, for nothing please use / instead')
                    if suffix[0] != '/':
                        suffix = '/' + suffix
                    
                    _url = url.rstrip('/') + suffix
                    if not module and 'app' not in sub_settings:
                        raise RouteSettingException('App is not set in routes neither in "%s" nor "%s"' % (url, _url)) 

                    if 'app' in sub_settings:
                        _app_name = sub_settings['app']
                        module = importlib.import_module('app.' + sub_settings['app'] + '.controllers', 'fire')
                    
                    if 'controller' not in sub_settings:
                        raise RouteSettingException('Controller is not set in routes in "%s"' % (_url))

                    if 'endpoint' not in sub_settings:
                        raise RouteSettingException('Endpoint is not set in routes in "%s"' % (_url))
                    
                    methods = ['GET']
                    if 'methods' in sub_settings:
                        methods = list(map(lambda x: x.strip().upper(), sub_settings['methods'].split(',')))

                    _class = getattr(module, sub_settings['controller'])
                    app.add_url_rule(_url, view_func=_class.as_view(_app_name + sub_settings['endpoint']), methods=methods)
                    if _app_name not in app.blueprints:
                        bp = Blueprint(_app_name, 'app.' + _app_name, template_folder='templates')
                        app.register_blueprint(bp)
                    if suffix == '/':
                        app.add_url_rule(url.rstrip('/'), view_func=_class.as_view(sub_settings['endpoint']), methods=methods)
            else:
                if 'app' not in settings or len(settings['app']) < 1:
                    raise RouteSettingException('App is not set in routes in "%s"' % (url))
                if settings['app'] == 'internal_render':
                    if 'file' in settings and 'endpoint' in settings:
                        app.add_url_rule(url, settings['endpoint'], view_func=internal_render, defaults={'page': settings['file']})
                    else:
                        raise RouteSettingException('Internal Render needs a filename')
                    continue
                if 'controller' not in settings:
                    raise RouteSettingException('Controller is not set in routes in "%s"' % (url))
                if 'endpoint' not in settings:
                    raise RouteSettingException('Endpoint is not set in routes in "%s"' % (url))

                methods = ['GET']
                if 'methods' in settings:
                    methods = list(map(lambda x: x.strip().upper(), settings['methods'].split(',')))

                module = importlib.import_module('app.' + settings['app'] + '.controllers', 'fire')
                _class = getattr(module, settings['controller'])
                app.add_url_rule(url, view_func=_class.as_view(settings['app'] + settings['endpoint']), methods=methods)
                if settings['app'] not in app.blueprints:
                    bp = Blueprint(settings['app'], 'app.' + settings['app'], template_folder='templates')
                    app.register_blueprint(bp)
