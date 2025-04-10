from flask import jsonify, request
from models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

def register():
        try:
            data = request.json
            hashed_password = generate_password_hash(data["password"])
            user = User(username=data["email"], password=hashed_password,qualification=data["qualification"],fullname=data["fullname"],dob=data["dob"])
            db.session.add(user)
            db.session.commit()
            return jsonify({"message": "User registered!"})
        except IntegrityError:
            return jsonify({"message": "User Already Exists!"}), 200