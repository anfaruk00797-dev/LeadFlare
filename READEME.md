Leader Platform

A Flask-based Productivity & Personal Leadership Management Website

* Project Overview

Leader Platform คือเว็บแอปพลิเคชันสำหรับจัดการงาน เป้าหมาย และนิสัย
พัฒนาด้วย Flask Framework และใช้ Bootstrap 5 เป็น CSS Framework

ผู้ใช้สามารถ:

จัดการ Project

จัดการ Task

ติดตาม Habit

ดู Dashboard สรุปภาพรวมงานของตนเอง

 Technologies Used

Python 3

Flask

Flask-Login

Flask-SQLAlchemy

SQLite Database

Bootstrap 5

Git (Commit Early & Commit Often)

 Database

ใช้ SQLite เป็นฐานข้อมูล
ไฟล์ฐานข้อมูล:

database.db

Models ที่ใช้:

User

Project

Task

Habit

มีการบันทึกข้อมูลจริงลงฐานข้อมูลทุกฟีเจอร์

 Website Pages (มากกว่า 10 หน้า)

ระบบมีอย่างน้อย 12 หน้า:

Home (/)

Register (/register)

Login (/login)

Logout (/logout)

Main Dashboard (/dashboard)

Personal Dashboard (/personal)

Team Dashboard (/team)

Create Project (/project/create)

Project Detail (/project/<id>)

Create Task (/project/<id>/task/create)

Edit Task (/task/<id>/edit)

Create Habit (/habit/create)

Edit Habit (/habit/<id>/edit)

 มากกว่า 10 หน้า ตามโจทย์กำหนด

 Features
 Authentication System

สมัครสมาชิก

เข้าสู่ระบบ

ออกจากระบบ

ใช้ Flask-Login ในการจัดการ session

 Project Management

สร้าง Project

ดูรายละเอียด Project

สร้าง Task ภายใน Project

เปลี่ยนสถานะ Task (Todo / Doing / Done)

 Dashboard Summary

Dashboard หลักแสดง:

จำนวน Project ทั้งหมด

จำนวน Task ทั้งหมด

จำนวน Task ที่เสร็จแล้ว

จำนวนงานที่เลยกำหนด (Overdue)

 Habit Tracking

เพิ่ม Habit

แก้ไข Habit

ติดตามสถานะความสม่ำเสมอ

▶️ How to Run This Project
1️⃣ Clone Project
git clone <your-git-url>
cd leader-platform
2️⃣ Create Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt

ถ้ายังไม่มี requirements.txt ให้ใช้:

pip install flask flask-login flask-sqlalchemy
4️⃣ Create Database

เปิด Python shell:

python

พิมพ์:

from app import db
db.create_all()
exit()
5️⃣ Run Application
python app.py

เข้าเว็บที่:

http://127.0.0.1:5000
 Git Development Strategy

โปรเจกต์นี้ใช้หลักการ:

✅ Commit Early
✅ Commit Often

มีจำนวน Commit มากกว่า 50 Commit
และทำงานต่อเนื่องมากกว่า 10 วัน

ตัวอย่างลักษณะ commit:

create user model

add login route

add dashboard summary

improve UI layout

fix task overdue logic

add habit tracking

📌 Folder Structure
leader-platform/
│
├── app.py
├── models.py
├── database.db
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── project_detail.html
│   ├── create_project.html
│   ├── create_task.html
│   ├── edit_task.html
│   ├── personal_dashboard.html
│   ├── team_dashboard.html
│   ├── create_habit.html
│   └── edit_habit.html
│
└── README.md