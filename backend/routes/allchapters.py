from flask import jsonify, request
from models import db, Chapters, Subjects
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError


@jwt_required()
def get_all_chapters():
    # Verify admin access
    current_user = get_jwt_identity()
    if current_user != "-1":
        return jsonify({"error": "Unauthorized"}), 403

    # Fetch all chapters
    chapters = Chapters.query.all()
    
    chapter_list = [
        {
            "id": chapter.id,
            "name": chapter.name,
            "subject_id": chapter.subject_id,  # Keep subject_id for reference
            "question_count": len(chapter.quizzes)  # Assuming `quizzes` relationship exists
        }
        for chapter in chapters
    ]
    
    return jsonify(chapter_list)
