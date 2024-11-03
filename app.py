from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database and login manager
db.init_app(app)
login_manager = LoginManager(app)

# Import and register blueprints if needed
# from routes import main as main_blueprint
# app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
