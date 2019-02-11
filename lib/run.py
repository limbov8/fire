from . import create_app

def run(host='0.0.0.0', port=65522, debug=True):
	application = create_app('development')
	application.run(host=host, port=port, debug=debug)