import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'nutrilog.db'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # ensure the upload folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, app.config['IMG_UPLOAD_PATH']))
    except OSError:
        pass

    # initialize the database
    from . import db
    db.init_app(app)

    # register the blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import diary
    app.register_blueprint(diary.bp)
    app.add_url_rule('/', endpoint='index')

    return app
