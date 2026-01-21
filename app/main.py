from flask import Flask
from config import Config

from app.pages.login import login_bp
from app.pages.register import register_bp
from app.pages.dashboard import dashboard_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)
