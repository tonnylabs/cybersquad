from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cybersquad.db"
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Cloudinary configuration
cloudinary.config(
    cloud_name='dfsj1bf3m',
    api_key='YOUR_API_KEY_HERE',
    api_secret='Rpcv6JADM752Y5bGJqiHEX4vEro'
)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Reel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300))
    likes = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='reel', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reel_id = db.Column(db.Integer, db.ForeignKey('reel.id'), nullable=False)
    username = db.Column(db.String(100))
    content = db.Column(db.String(300))

# Routes
@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            session["user"] = user.username
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(username=request.form["username"], password=request.form["password"])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    reels = Reel.query.all()
    return render_template("dashboard.html", reels=reels)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["reel"]
    if file:
        upload_result = cloudinary.uploader.upload(file, resource_type="video")
        new_reel = Reel(filename=upload_result["secure_url"])
        db.session.add(new_reel)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/like/<int:reel_id>")
def like(reel_id):
    reel = Reel.query.get_or_404(reel_id)
    reel.likes += 1
    db.session.commit()
    return redirect("/dashboard")

@app.route("/comment/<int:reel_id>", methods=["POST"])
def comment(reel_id):
    content = request.form["comment"]
    new_comment = Comment(reel_id=reel_id, username=session["user"], content=content)
    db.session.add(new_comment)
    db.session.commit()
    return redirect("/dashboard")

# Real-time chat
@socketio.on("send_message")
def handle_message(data):
    socketio.emit("receive_message", data, broadcast=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)
