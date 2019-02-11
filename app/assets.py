from flask_assets import Bundle

def create_assets(assets):
    # js = Bundle(
    #     'js/viztype.js',
    #     filters='jsmin',
    #     output='bundle/viztype_libs.js'
    # )
    # assets.register('JS_FRAMEWORS', js)

    css = Bundle(
        'css/main.css',
        filters='cssmin',
        output='bundle/main.min.css'
    )
    assets.register('CSS_FRAMEWORKS', css)