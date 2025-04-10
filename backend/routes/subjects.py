from flask import jsonify, request
from models import db, Subjects
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@jwt_required()
def manage_subjects():
    current_user = get_jwt_identity()
    if current_user != "-1":
        return jsonify({"error": "Unauthorized"}), 403

    ############# GET ####################
    if request.method == "GET":
        subjects = Subjects.query.all()
        subject_list = [
            {
                "id": subject.id,
                "name": subject.name,
                "description": subject.description,
                "chapters": [
                    {
                        "id": chapter.id,
                        "name": chapter.name,
                        "quizz_count": len(chapter.quizzes)
                    } for chapter in subject.chapters
                ]
            } for subject in subjects
        ]
        return jsonify(subject_list)

    ############### POST #################
    elif request.method == "POST":
        data = request.json
        
        if not data or 'name' not in data:
            return jsonify({"error": "Subject name is required"}), 400
        
        try:
            new_subject = Subjects(
                name=data['name'],
                description=data.get('description', '')
            )
            
            db.session.add(new_subject)
            db.session.commit()
            
            return jsonify({
                "id": new_subject.id,
                "name": new_subject.name,
                "description": new_subject.description,
                "chapters": []
            }), 201
        
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Subject with this name already exists"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    ############### PUT (UPDATE) #################
    elif request.method == "PUT":
        data = request.json
        subject_id = data.get('id')
        
        if not subject_id:
            return jsonify({"error": "Subject ID is required"}), 400
        
        subject = Subjects.query.get(subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404

        if 'name' in data:
            subject.name = data['name']
        if 'description' in data:
            subject.description = data['description']
        
        try:
            db.session.commit()
            return jsonify({
                "id": subject.id,
                "name": subject.name,
                "description": subject.description
            })
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Subject with this name already exists"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    ############### DELETE #################
    elif request.method == "DELETE":
        data = request.json
        subject_id = data.get('id')
        
        if not subject_id:
            return jsonify({"error": "Subject ID is required"}), 400
        
        subject = Subjects.query.get(subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404
        
        try:
            db.session.delete(subject)
            db.session.commit()
            return jsonify({"message": "Subject deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
