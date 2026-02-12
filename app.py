from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send
from werkzeug.security import generate_password_hash, check_password_hash
import os, base64

app = Flask(__name__)
app.secret_key = "cybersquadsecret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"

db = SQLAlchemy(app)
socketio = SocketIO(app)

# USER MODEL
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

# REEL MODEL
class Reel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200))

# REGISTER ROUTE
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hashed = generate_password_hash(request.form["password"])
        new_user = User(username=request.form["username"], password=hashed)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

# LOGIN ROUTE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user"] = user.username
            return redirect("/dashboard")
    return render_template("login.html")

# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        file = request.files["reel"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            db.session.add(Reel(filename=file.filename))
            db.session.commit()

    reels = Reel.query.all()
    return render_template("dashboard.html", reels=reels)

# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# REAL-TIME CHAT
@socketio.on("message")
def handle_message(msg):
    encrypted = base64.b64encode(msg.encode()).decode()
    send(encrypted, broadcast=True)

# RUN APP ON ALL INTERFACES
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
