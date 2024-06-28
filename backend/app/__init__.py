from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS  # Add this line
from config import Config
import logging


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

# Set up basic configuration for logging
logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

# Now, use logging in your application
logging.info("Starting the app...")


def create_app():
    print("Creating Flask app...")  # Print statement to confirm function is called
    app = Flask(__name__)
    app.config.from_object(Config)
    print("Configured Flask app from object.")  # Confirm configuration is loaded

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CORS(app)

    from . import routes  # Import inside to avoid circular dependencies
    app.register_blueprint(routes.bp)
    print("Registered blueprint.")  # Confirm blueprint registration

    return app
