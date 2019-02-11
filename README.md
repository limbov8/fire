# fire
Flask on Fire, a MVC template for Flask

# Setup

## Run
- rename `config/database.yml.default` to `config/database.yml`
- use `bin/fire server` to setup a development server

## Settings

- use `config/routes.yml` to register routes
- change `config/config.yml` accordingly
- write static files in `public/`
- change static file bundle settings in `app/assets.py`
- use `app/jobs.py` to setup aync jobs using rq (redis queue)

### RQ Workers

```shell
.venv/bin/rq worker --url redis://127.0.0.1:6379/0 --name %(program_name)s-%(process_num)s  high normal low
```

# Commands

```shell
(.venv) $ bin/fire 
Usage: fire [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  console  Open a test console with flask context
  new      Create a new app/scaffold
  routes   List all routes
  server   Run a development fire server.

(.venv) $ bin/fire new
Usage: fire new [OPTIONS] [app|scaffold] APP_NAME
Try "fire new --help" for help.

Error: Missing argument "[app|scaffold]".  Choose from:
	app,
	scaffold.

(.venv) $ bin/fire new app test
Creating folder app/test ...
Creating file controllers.py ...
Writing into file controllers.py...
Creating file __init__.py ...
Creating folder app/test/templates/test ...

(.venv) $ bin/fire new scaffold test
Creating folder app/test ...
Creating file controllers.py ...
Writing into file controllers.py...
Creating file __init__.py ...
Creating folder app/test/templates/test ...
Creating templates files in app/test/templates/test ...
Writing scaffold routes into config/routes.yml ...
```

# Contributor

Thanks 
- [CharlyJazz/Flask-MVC-Template](https://github.com/CharlyJazz/Flask-MVC-Template)
- [sloria/flask-konch](https://github.com/sloria/flask-konch)