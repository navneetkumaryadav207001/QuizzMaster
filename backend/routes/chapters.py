from flask import jsonify, request
from models import db, Chapters, Subjects
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError

@jwt_required()
def manage_chapters(subject_id):
    # Verify admin access
    current_user = get_jwt_identity()
    if current_user != "-1":
        return jsonify({"error": "Unauthorized"}), 403
    
    # Check if subject exists
    subject = Subjects.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Subject not found"}), 404
    
    if request.method == "GET":
        # Fetch chapters for the subject
        chapters = Chapters.query.filter_by(subject_id=subject_id).all()
        chapter_list = [
            {
                "id": chapter.id,
                "name": chapter.name,
                "question_count": len(chapter.quizzes)  # Fix: Count quizzes, not questions
            } for chapter in chapters
        ]
        return jsonify(chapter_list)
    
    elif request.method == "POST":
        # Add new chapter to subject
        data = request.json
        
        # Validate input
        if not data or 'name' not in data:
            return jsonify({"error": "Chapter name is required"}), 400
        
        try:
            # Create new chapter
            new_chapter = Chapters(
                name=data['name'],
                subject_id=subject_id
            )
            
            db.session.add(new_chapter)
            db.session.commit()
            
            # Prepare response
            response_data = {
                "id": new_chapter.id,
                "name": new_chapter.name,
                "subject_id": subject_id,
                "question_count": 0
            }
            
            return jsonify(response_data), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "PUT":
        # Update chapter details
        data = request.json
        chapter_id = data.get("id")
        
        if not chapter_id:
            return jsonify({"error": "Chapter ID is required"}), 400
        
        chapter = Chapters.query.get(chapter_id)
        if not chapter or chapter.subject_id != subject_id:
            return jsonify({"error": "Chapter not found"}), 404
        
        if "name" in data:
            chapter.name = data["name"]
        
        try:
            db.session.commit()
            return jsonify({
                "id": chapter.id,
                "name": chapter.name,
                "subject_id": subject_id,
                "question_count": len(chapter.quizzes)
            })
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Chapter with this name already exists"}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    
    elif request.method == "DELETE":
        # Delete a chapter by its ID
        data = request.json
        chapter_id = data.get("id")

        if not chapter_id:
            return jsonify({"error": "Chapter ID is required"}), 400

        chapter = Chapters.query.get(chapter_id)
        if not chapter or chapter.subject_id != subject_id:
            return jsonify({"error": "Chapter not found"}), 404

        try:
            db.session.delete(chapter)
            db.session.commit()
            return jsonify({"message": "Chapter deleted successfully"}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Failed to delete chapter due to database constraints"}), 500
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
