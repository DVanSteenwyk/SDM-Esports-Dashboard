# src/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# init packages
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    # init app creation
    app = Flask(__name__, static_folder='static', 
            template_folder='templates')

    # configs
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esports_dashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # switch to 'True' for logging
    app.config['SECRET_KEY'] = 'your-secret-key'  # required for forms

    # link db with app
    db.init_app(app)
    migrate.init_app(app, db)

    # login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
          return User.query.get(int(user_id))


    with app.app_context():
        # import models to register
        from .models.user import User

        # import blueprints
        from .routes.home import home_bp
        app.register_blueprint(home_bp)

        from .routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    
    

    return app
