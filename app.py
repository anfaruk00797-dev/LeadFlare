from flask import Flask, render_template, redirect, url_for, request
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

from models import db, User, Event

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
@login_required
def dashboard():
    today = date.today()
    upcoming_events = []

    events = current_user.events

    for event in events:
        reminder_start = event.event_date - timedelta(days=event.reminder_days)

        if reminder_start <= today <= event.event_date:
            days_left = (event.event_date - today).days
            upcoming_events.append((event, days_left))

    return render_template("dashboard.html", upcoming_events=upcoming_events)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/create_event", methods=["GET", "POST"])
@login_required
def create_event():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        event_date = datetime.strptime(
            request.form.get("event_date"), "%Y-%m-%d"
        ).date()
        reminder_days = int(request.form.get("reminder_days"))

        new_event = Event(
            title=title,
            description=description,
            event_date=event_date,
            reminder_days=reminder_days,
            user=current_user,
        )

        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("create_event.html")


@app.route("/event/<int:event_id>", methods=["GET", "POST"])
@login_required
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)

    # ป้องกันดู event ของคนอื่น
    if event.user != current_user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        event.preparation_note = request.form.get("preparation_note")
        db.session.commit()
        return redirect(url_for("event_detail", event_id=event.id))

    return render_template("event_detail.html", event=event)


if __name__ == "__main__":
    app.run(debug=True)
