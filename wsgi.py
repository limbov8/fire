from lib import create_app

application = create_app('production')
application.run()