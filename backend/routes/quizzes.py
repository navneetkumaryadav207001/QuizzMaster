from flask import jsonify, request
from models import db, Quiz, Question
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@jwt_required()
def manage_quizzes():
    current_user = get_jwt_identity()
    
    if request.method == "GET":
        quizzes = Quiz.query.all()
        quizzes_list = []
        for quiz in quizzes:
            quiz_data = {
                "id": quiz.id,
                "name": quiz.name,
                "chapter_id": quiz.chapter_id,
                "duration": quiz.duration,
                "date": quiz.date,
                "questions": [
                    {
                        "id": question.id,
                        "text": question.text,
                        "option_a": question.option_a,
                        "option_b": question.option_b,
                        "option_c": question.option_c,
                        "option_d": question.option_d
                    } for question in quiz.questions
                ]
            }
            quizzes_list.append(quiz_data)
        return jsonify(quizzes_list)

    elif request.method == "POST":
        data = request.json
        if not data or 'name' not in data or 'chapter_id' not in data:
            return jsonify({"error": "Title and chapter_id are required"}), 400
        try:
            new_quiz = Quiz(
                name=data['name'],
                chapter_id=data['chapter_id'],
                description=data.get('description', ""),
                date=data.get('date'),
                duration=data.get('duration'),
            )
            db.session.add(new_quiz)
            db.session.commit()
            return jsonify({"id": new_quiz.id, "name": new_quiz.name, "chapter_id": new_quiz.chapter_id, "questions": []}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Quiz with this title already exists"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    elif request.method == "PUT":
        data = request.json
        if not data or 'id' not in data:
            return jsonify({"error": "Quiz ID is required"}), 400
        quiz = Quiz.query.get(data['id'])
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404
        
        try:
            quiz.name = data.get('name', quiz.name)
            quiz.chapter_id = data.get('chapter_id', quiz.chapter_id)
            quiz.description = data.get('description', quiz.description)
            quiz.date = data.get('date', quiz.date)
            quiz.duration = data.get('duration', quiz.duration)
            
            db.session.commit()
            return jsonify({"message": "Quiz updated successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "DELETE":
        quiz_id = request.json['id']
        if not quiz_id:
            return jsonify({"error": "Quiz ID is required"}), 400
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404
        
        try:
            db.session.delete(quiz)
            db.session.commit()
            return jsonify({"message": "Quiz deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
