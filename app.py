from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta

from models import db, User, Event  # 👈 ดึง db จาก models

app = Flask(__name__)
app.config["SECRET_KEY"] = "secretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# 👇 ผูก db กับ app ที่นี่
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 👇 สร้าง table หลังจาก init_app แล้ว
with app.app_context():
    db.create_all()
