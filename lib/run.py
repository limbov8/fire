from . import create_app

application = create_app('development')

application.run(host='0.0.0.0', port=65522, debug=True)