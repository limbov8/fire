from lib.utils.conversions import dict2obj
import yaml


database_settings = {}
with open('config/database.yml', 'r') as f:
    database_settings = yaml.load(f)

app_config = {}
with open('config/config.yml', 'r') as f:
    app_config = yaml.load(f)

for k,v in app_config.items():
	app_config[k].update(database_settings[k])

routes = {}
with open('config/routes.yml', 'r') as f:
    routes = yaml.load(f)

app_config = {
    'development': dict2obj(app_config['development']),
    'production': dict2obj(app_config['production']),
    'testing': dict2obj(app_config['testing'])
}

all = [
    'app_config',
    'routes'
]