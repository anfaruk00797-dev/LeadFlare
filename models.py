from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()


# ================= USER =================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


# ================= HABIT (FIRE SYSTEM) =================
class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    fire_count = db.Column(db.Integer, default=0)
    longest_fire = db.Column(db.Integer, default=0)
    shield_remaining = db.Column(db.Integer, default=3)
    last_completed_date = db.Column(db.Date)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="habits")

    def complete_today(self):
        today = date.today()

        if self.last_completed_date == today:
            return

        if self.last_completed_date:
            diff = (today - self.last_completed_date).days
            if diff == 1:
                self.fire_count += 1
            else:
                if self.shield_remaining > 0:
                    self.shield_remaining -= 1
                else:
                    self.fire_count = 1
        else:
            self.fire_count = 1

        self.last_completed_date = today

        if self.fire_count > self.longest_fire:
            self.longest_fire = self.fire_count


# ================= PROJECT =================
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="Planning")

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner = db.relationship("User", backref="projects")


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default="To Do")
    deadline = db.Column(db.Date)

    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", backref="tasks")

    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"))
