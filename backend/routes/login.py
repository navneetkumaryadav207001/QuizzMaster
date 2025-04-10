from flask import jsonify, request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models import db, User
from sqlalchemy.exc import IntegrityError

def login():
    data = request.json
    user = User.query.filter_by(username=data["email"]).first()
    if data['email'] == "Admin@qm.com" and data["password"] == "Admin123":
        access_token = create_access_token(identity="-1")
        return jsonify({"access_token": access_token,"is_admin": True })
    if user and check_password_hash(user.password, data["password"]):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({"access_token": access_token,"is_admin" :False})
    return jsonify({"error": "Invalid credentials"}), 200