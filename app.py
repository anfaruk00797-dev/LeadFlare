from flask import Flask, render_template, redirect, url_for, request, flash
from datetime import datetime
from config import Config
from models import db, User, Habit, Project, Task
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        # ป้องกัน username ซ้ำ
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registered successfully!")
        return redirect(url_for("login"))

    return render_template("register.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("main_dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")


# ================= LOGOUT =================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# ================= MAIN DASHBOARD =================
@app.route("/dashboard")
@login_required
def main_dashboard():
    # ===== PERSONAL =====
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    total_habits = len(habits)
    total_fire = sum(h.fire_count for h in habits)
    longest_fire = max([h.longest_fire for h in habits], default=0)

    # ===== TEAM =====
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    total_projects = len(projects)

    total_tasks = 0
    completed_tasks = 0
    overdue_tasks = 0

    today = datetime.today().date()

    for project in projects:
        for task in project.tasks:
            total_tasks += 1
            if task.status == "Done":
                completed_tasks += 1
            if task.deadline and task.deadline < today and task.status != "Done":
                overdue_tasks += 1

    completion_rate = (
        round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
    )

    return render_template(
        "dashboard.html",
        total_fire=total_fire,
        longest_fire=longest_fire,
        total_habits=total_habits,
        total_projects=total_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        completion_rate=completion_rate,
    )


# ================= PERSONAL DASHBOARD =================
@app.route("/personal/dashboard")
@login_required
def personal_dashboard():
    habits = Habit.query.filter_by(user_id=current_user.id).all()
    return render_template("personal_dashboard.html", habits=habits)


# ================= CREATE HABIT =================
@app.route("/habit/create", methods=["GET", "POST"])
@login_required
def create_habit():
    if request.method == "POST":
        habit = Habit(name=request.form["name"], user_id=current_user.id)
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for("personal_dashboard"))

    return render_template("create_habit.html")


# ================= COMPLETE HABIT =================
@app.route("/habit/complete/<int:id>")
@login_required
def complete_habit(id):
    habit = Habit.query.get_or_404(id)

    # กัน user อื่นมาแก้
    if habit.user_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for("personal_dashboard"))

    habit.complete_today()
    db.session.commit()
    return redirect(url_for("personal_dashboard"))


# ================= TEAM DASHBOARD =================
@app.route("/team/dashboard")
@login_required
def team_dashboard():
    projects = Project.query.filter_by(owner_id=current_user.id).all()
    return render_template("team_dashboard.html", projects=projects)


# ================= CREATE PROJECT =================
@app.route("/project/create", methods=["GET", "POST"])
@login_required
def create_project():
    if request.method == "POST":
        project = Project(
            name=request.form["name"],
            description=request.form["description"],
            owner_id=current_user.id,
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for("team_dashboard"))

    return render_template("create_project.html")


# ================= PROJECT DETAIL =================
@app.route("/project/<int:id>")
@login_required
def project_detail(id):
    project = Project.query.get_or_404(id)

    if project.owner_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for("team_dashboard"))

    return render_template("project_detail.html", project=project)


# ================= CREATE TASK =================
@app.route("/task/create/<int:project_id>", methods=["GET", "POST"])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)

    if project.owner_id != current_user.id:
        flash("Unauthorized")
        return redirect(url_for("team_dashboard"))

    if request.method == "POST":
        deadline = request.form.get("deadline")

        task = Task(
            title=request.form["title"],
            description=request.form["description"],
            deadline=datetime.strptime(deadline, "%Y-%m-%d") if deadline else None,
            project_id=project.id,
            assigned_to=current_user.id,
            status="Todo",
        )

        db.session.add(task)
        db.session.commit()

        return redirect(url_for("project_detail", id=project.id))

    return render_template("create_task.html", project=project)


# ================= UPDATE TASK STATUS =================
@app.route("/task/update/<int:id>/<status>")
@login_required
def update_task_status(id, status):
    task = Task.query.get_or_404(id)
    task.status = status
    db.session.commit()
    return redirect(url_for("project_detail", id=task.project_id))


# ================= RUN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
