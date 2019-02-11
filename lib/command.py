import urllib
import sys, os
from . import create_app
from flask import url_for
from flask import current_app
import konch
import click

dev_app = create_app('testing')

def list_routes():
    with dev_app.app_context():
        output = []
        for rule in dev_app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)
        
        for line in sorted(output):
            print(line)

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def new_app(type, name):
    with dev_app.app_context():
        name = name.lower()
        folder = current_app.config['APP_FOLDER'] + name
        if not os.path.exists(folder):
            os.makedirs(folder)
            click.secho('Creating folder %s ...' % folder, fg='green')
            python_files = ["controllers", "__init__"]
            for i, file in enumerate(python_files):
                click.secho('Creating file %s.py ...' % file, fg='green')
                with open(os.path.join(folder, file + ".py"), 'w') as temp_file:
                    if file is "controllers":
                        click.secho('Writing into file %s.py...' % file, fg='green', bold=True)
                        if type == 'app':
                            temp_file.write("from flask.views import MethodView\n"
                                            "from flask import render_template, make_response, jsonify, request, redirect, url_for, flash\n")
                        elif type == 'scaffold': 
                            name_captialized = name.capitalize()
                            temp_file.write("from flask.views import MethodView\n"
                                            "from flask import render_template, make_response, jsonify, request, redirect, url_for, flash\n\n"
                                            "class %sIndex(MethodView):\n    def get(self):\n        return render_template('%s/index.html')\n\nclass %sView(MethodView):\n    def get(self, id):\n        return render_template('%s/view.html')\n\n\nclass %sEdit(MethodView):\n    def get(self, id):\n        return render_template('%s/edit.html')\n\n    def post(self, id):\n        return jsonify({'status': 'ok'})\n\n\nclass %sDelete(MethodView):\n    def delete(self, id):\n        return jsonify({'status': 'ok'})\n" % (name_captialized, name, name_captialized, name, name_captialized, name, name_captialized))
            templates_path = folder + "/templates/" + name
            if type == 'app':
                click.secho('Creating folder %s ...' % templates_path, fg='green')
                os.makedirs(templates_path)
            elif type == 'scaffold':
                click.secho('Creating folder %s ...' % templates_path, fg='green')
                os.makedirs(templates_path)
                click.secho('Creating templates files in %s ...' % templates_path, fg='green')
                touch(templates_path + '/index.html')
                touch(templates_path + '/edit.html')
                touch(templates_path + '/view.html')
                click.secho('Writing scaffold routes into config/routes.yml ...', fg='green', bold=True)
                with open(current_app.config['APP_FOLDER'] + '../config/routes.yml', 'a') as routes:
                    routes.write("\n/%s:\n  scope: true\n  "
                        "app: %s\n  suffix:\n    /:\n      "
                        "controller: %sIndex\n      "
                        "methods: get\n      "
                        "endpoint: %s_index\n    "
                        "/view/<id>:\n      "
                        "controller: %sView\n      "
                        "methods: get\n      "
                        "endpoint: %s_view\n    "
                        "/edit/<id>:\n      "
                        "controller: %sEdit\n      "
                        "methods: get, post\n      "
                        "endpoint: %s_edit\n    "
                        "/delete/<id>:\n      "
                        "controller: %sDelete\n      "
                        "methods: delete\n      "
                        "endpoint: %s_delete\n" % (name, name, name_captialized, name, name_captialized, name, name_captialized, name, name_captialized, name))
        
        else:
            click.secho('%s already exists' % name, fg='red')

def console():
    import flask
    from flask.globals import _app_ctx_stack
    from flask.cli import with_appcontext
    import click
    DEFAULTS = dict(
        KONCH_FLASK_IMPORTS=True,
        KONCH_FLASK_SHELL_CONTEXT=True,
        KONCH_CONTEXT={},
        KONCH_SHELL="auto",
        KONCH_BANNER=None,
        KONCH_PROMPT=None,
        KONCH_OUTPUT=None,
        KONCH_CONTEXT_FORMAT=None,
        KONCH_IPY_AUTORELOAD=False,
        KONCH_IPY_EXTENSIONS=None,
        KONCH_IPY_COLORS=None,
        KONCH_IPY_HIGHLIGHTING_STYLE=None,
        KONCH_PTPY_VI_MODE=False,
    )

    def get_flask_imports():
        ret = {}
        for name in [e for e in dir(flask) if not e.startswith("_")]:
            ret[name] = getattr(flask, name)
        return ret

    with dev_app.app_context():

        app = _app_ctx_stack.top.app
        options = {key: app.config.get(key, DEFAULTS[key]) for key in DEFAULTS.keys()}

        base_context = {"app": dev_app}
        if options["KONCH_FLASK_IMPORTS"]:
            base_context.update(get_flask_imports())

        context = dict(base_context)

        if options["KONCH_FLASK_SHELL_CONTEXT"]:
            flask_context = app.make_shell_context()
            context.update(flask_context)

        context.update(options["KONCH_CONTEXT"])

        def context_formatter(ctx):
            formatted_base = ", ".join(sorted(base_context.keys()))
            ret = "\n{FLASK}\n{base_context}\n".format(
                FLASK=click.style("Flask:", bold=True), base_context=formatted_base
            )
            if options["KONCH_FLASK_SHELL_CONTEXT"]:
                variables = ", ".join(sorted(flask_context.keys()))
                ret += "\n{ADDITIONAL}\n{variables}\n".format(
                    ADDITIONAL=click.style(
                        "Flask shell context (see shell_context_processor()):", bold=True
                    ),
                    variables=variables,
                )
            if options["KONCH_CONTEXT"]:
                variables = ", ".join(sorted(options["KONCH_CONTEXT"].keys()))
                ret += "\n{ADDITIONAL}\n{variables}".format(
                    ADDITIONAL=click.style(
                        "Additional variables (see KONCH_CONTEXT):", bold=True
                    ),
                    variables=variables,
                )
            return ret

        context_format = options["KONCH_CONTEXT_FORMAT"] or context_formatter
        konch.start(
            context=context,
            shell=options["KONCH_SHELL"],
            banner=options["KONCH_BANNER"],
            prompt=options["KONCH_PROMPT"],
            output=options["KONCH_OUTPUT"],
            ptpy_vi_mode=options["KONCH_PTPY_VI_MODE"],
            context_format=context_format,
            ipy_extensions=options["KONCH_IPY_EXTENSIONS"],
            ipy_autoreload=options["KONCH_IPY_AUTORELOAD"],
            ipy_colors=options["KONCH_IPY_COLORS"],
            ipy_highlighting_style=options["KONCH_IPY_HIGHLIGHTING_STYLE"],
        )