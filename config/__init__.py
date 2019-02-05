from environments import DevelopmentConfig, ProductionConfig
import yaml


database_settings = {}
with open('database.yml', 'r') as f:
	database_settings = yaml.load(f)


app_config = {
	'development': DevelopmentConfig
	'production': ProductionConfig
}


all = [
	'app_config'
]