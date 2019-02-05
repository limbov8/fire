from flask import Flask

def create_app(config):

	app = Flask('__main__')

	return app