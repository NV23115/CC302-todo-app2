class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)

from datetime import datetime

description = db.Column(db.Text)
priority = db.Column(db.String(20), default="medium")
due_date = db.Column(db.DateTime)
status = db.Column(db.String(20), default="todo")
created_at = db.Column(db.DateTime, default=datetime.utcnow)
updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
