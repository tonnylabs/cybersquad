from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO, send


app = Flask(_name_)
app.secret_key = "secretkey"

socketio = SocketIO(app)
 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True)

app.run(debug=True)

socketio.run(app, debug=True)


