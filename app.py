from flask import Flask, render_template, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from routes.routes import routes_bp
from models.models import db

app = Flask(__name__)

# Configure session and database
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
Session(app)
db.init_app(app)

# Register routes
app.register_blueprint(routes_bp)

# Initialize the database
with app.app_context():
    db.create_all()

# Home route to render the chat interface
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
