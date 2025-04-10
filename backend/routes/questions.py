from flask import jsonify, request
from models import db, Question, Quiz
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@jwt_required()
def manage_questions():
    current_user = get_jwt_identity()
    if current_user != "-1":
        return jsonify({"error": "Unauthorized"}), 403

    ############# GET ####################
    
    if request.method == "GET":
        questions = Question.query.all()
        question_list = []

        for question in questions:
            question_data = {
                "id": question.id,
                "title" :question.title,
                "text": question.text,
                "option_a": question.option_a,
                "option_b": question.option_b,
                "option_c": question.option_c,
                "option_d": question.option_d,
                "correct_option": question.correct_option,
                "quiz_id": question.quiz_id
            }
            question_list.append(question_data)

        return jsonify(question_list)

    ############### POST #################

    elif request.method == "POST":
        data = request.json

        print(data)
        if not data or 'text' not in data or 'correct_option' not in data or 'quiz_id' not in data:
            return jsonify({"error": "All fields (text, options, answer, quiz_id) are required"}), 400

        # Validate quiz existence
        quiz = Quiz.query.get(data['quiz_id'])
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        try:
            new_question = Question(
                title = data["question_title"],
                text=data['text'],
                option_a=data['option_a'],
                option_b = data['option_b'],
                option_c = data['option_c'],
                option_d = data['option_d'],
                correct_option=data['correct_option'],
                quiz_id=data['quiz_id']
            )
            
            db.session.add(new_question)
            db.session.commit()

            response_data = {
                "id": new_question.id,
                "text": new_question.text,
                "correct_option": new_question.correct_option,
                "quiz_id": new_question.quiz_id
            }

            return jsonify(response_data), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Duplicate question"}), 400
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    ############### PUT (UPDATE) #################
    elif request.method == "PUT":
        data = request.json
        question_id = data.get("id")

        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400

        question = Question.query.get(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        if "text" in data:
            question.text = data["text"]
        if "option_a" in data:
            question.option_a = data["option_a"]
        if "option_b" in data:
            question.option_b = data["option_b"]
        if "option_c" in data:
            question.option_c = data["option_c"]
        if "option_d" in data:
            question.option_d = data["option_d"]
        if "correct_option" in data:
            question.correct_option = data["correct_option"]
        
        try:
            db.session.commit()
            return jsonify({
                "id": question.id,
                "text": question.text,
                "correct_option": question.correct_option,
                "quiz_id": question.quiz_id
            })
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Question update failed due to database constraints"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    ############### DELETE #################
    elif request.method == "DELETE":
        data = request.json
        question_id = data.get("id")

        if not question_id:
            return jsonify({"error": "Question ID is required"}), 400

        question = Question.query.get(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        try:
            db.session.delete(question)
            db.session.commit()
            return jsonify({"message": "Question deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
