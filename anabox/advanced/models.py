from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'tbl_users'

    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    regDate = db.Column(db.Date, default=datetime.utcnow, nullable=True)
    usertype = db.Column(db.Integer, nullable=False)

    # 메시지 보낸 관계 설정
    messages_sent = db.relationship('Message', backref='sender', foreign_keys='Message.sendid', cascade='all, delete-orphan')


class Messenger(db.Model):
    __tablename__ = 'tbl_messenger'

    messengernum = db.Column(db.Integer, primary_key=True)
    bookingnum = db.Column(db.Integer, nullable=False)
    id1 = db.Column(db.String(100), db.ForeignKey('tbl_users.id', ondelete='CASCADE'), nullable=False)
    id2 = db.Column(db.String(100), db.ForeignKey('tbl_users.id', ondelete='CASCADE'), nullable=False)
    createtime = db.Column(db.DateTime, default=datetime.utcnow)

    # message 연동
    messages = db.relationship('Message', backref='chatroom', cascade='all, delete-orphan')


class Message(db.Model):
    __tablename__ = 'tbl_message'

    messagenum = db.Column(db.Integer, primary_key=True)
    messengernum = db.Column(db.Integer, db.ForeignKey('tbl_messenger.messengernum', ondelete='CASCADE'), nullable=False)
    sendid = db.Column(db.String(100), db.ForeignKey('tbl_users.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text)
    regtime = db.Column(db.DateTime, default=datetime.utcnow)