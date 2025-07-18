# src/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# init packages


def create_app():
    # init app creation
    app = Flask(__name__, static_folder='static', 
            template_folder='templates')

    # configs
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # switch to 'True' for logging
    app.config['SECRET_KEY'] = 'your-secret-key'  # required for forms

    with app.app_context():

        # import blueprints
        from .routes.home import home_bp
        app.register_blueprint(home_bp)

        from .routes.about import about_bp
        app.register_blueprint(about_bp)

        from .routes.teams import teams_bp
        app.register_blueprint(teams_bp)

        from .routes.schedule import schedule_bp
        app.register_blueprint(schedule_bp)

        from .routes.contact_us import contact_us_bp
        app.register_blueprint(contact_us_bp)

        from .routes.sponsors import sponsors_bp
        app.register_blueprint(sponsors_bp)

        from .routes.uploads import upload_svg_bp
        app.register_blueprint(upload_svg_bp)
    
    return app