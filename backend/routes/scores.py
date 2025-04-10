
from flask import jsonify, request
from models import db, Scores, Quiz ,Question
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from datetime import datetime


@jwt_required()
def get_user_scores():
    userId = get_jwt_identity()
    scores = Scores.query.filter_by(user_id = userId).all()
    
    if not scores:
        return jsonify({"message": "No scores found for this user."}), 404

    scores_list = [{
        "id": score.id,
        "quiz_id": score.quiz_id,
        "score": score.score,
        "total_questions": score.total_questions,
        "attempted_at": score.attempted_at.strftime('%Y-%m-%d %H:%M:%S')
    } for score in scores]

    return jsonify(scores_list), 200

# ✅ POST a new quiz score

@jwt_required()
def submit_score():
    data = request.get_json()
    user_id = get_jwt_identity()  # Get current logged-in user ID
    quiz_id = data.get("quiz_id")
    total_questions = data.get("total_questions")
    answers = data.get("answers")  # List of selected answers
    
    if not quiz_id or not total_questions or answers is None:
        return jsonify({"message": "Missing required fields."}), 400

    # Fetch quiz and its questions
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({"message": "Quiz not found."}), 404

    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if len(questions) != total_questions:
        return jsonify({"message": "Mismatch in total questions."}), 400

    # Calculate score
    score = 0
    attempted_questions = 0

    for i, question in enumerate(questions):
        user_answer = answers[i]

        if user_answer:  # Only count attempted questions
            attempted_questions += 1
            correct_answer = getattr(question, f"option_{question.correct_option.lower()}")  # Get correct option value
            
            if user_answer == correct_answer:
                score += 1  # Correct answer

    # Save the score in the database
    new_score = Scores(
        user_id=user_id,
        quiz_id=quiz_id,
        score=score,
        total_questions=total_questions,
        attempted_at=datetime.utcnow()
    )

    db.session.add(new_score)
    db.session.commit()

    return jsonify({
        "message": "Score submitted successfully!",
        "score": score,
        "total_questions": total_questions,
        "attempted_questions": attempted_questions
    }), 201