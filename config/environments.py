class DevelopmentConfig(object):
	SECRET_KEY = 'SECRET_KEY'
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    ENV = ""
    SEND_FILE_MAX_AGE_DEFAULT = 0

    #Flask-Assets

    ASSETS_DEBUG = False


class ProductionConfig(object):
	pass