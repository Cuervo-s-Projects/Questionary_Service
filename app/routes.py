from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
import os 
import requests

from app.service import QuestionaryService

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
swagger_path = os.path.join(root_path, "docs")

class_bp = Blueprint('quiz', __name__, url_prefix='/api/test')


@class_bp.route('/create', methods=['POST'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'create.yaml')) 
def create():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        token = request.authorization
        headers = {"Authorization": f"{token}"}
        response = requests.get("http://127.0.0.1:5000/api/profile", headers=headers)
        data_rp = response.json()

        questionary_service = QuestionaryService()
        status = questionary_service.create(
            id=str(data.get('id')),
            title=data.get('title'),
            author_id=data_rp.get('_id'),
            questions=data.get('questions'),
        )

        return jsonify({
            "msg": status
        })

    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400
    
@class_bp.route('/assess', methods=['POST'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'assess.yaml')) 
def assess():
    try:

        token = request.authorization
        headers = {"Authorization": f"{token}"}
        response = requests.get("http://127.0.0.1:5000/api/profile", headers=headers)
        data_rp = response.json()
        user_id = data_rp.get('_id')

        data = request.get_json()
        
        questionary_service = QuestionaryService()
        quiz_id = data.get('quiz_id')
        quiz = questionary_service.get_by_id(quiz_id)

        questions = quiz.questions
        length_questions = len(questions)

        reply = data.get('reply')
        length_reply = len(reply)

        value = 0
        array = []

        for y in range(length_reply):
            temp_rp = reply[y]

            for x in range(length_questions):
                temp_qtn = questions[x]
                question = temp_qtn.get('question')

                if temp_rp['question'] == question:
                    correct = temp_qtn['correct']

                    if correct == temp_rp['response']:
                        value += int(temp_qtn['value'])
                        result = {'question': question, 'correct':temp_qtn['correct'], 'result': True, 'value': temp_qtn['value']} 
                        array.append(result)
                    else:
                        result = {'question': question,'correct':temp_qtn['correct'], 'result': False, 'value': 0} 
                        array.append(result)

        return jsonify({
            "result": array,
            "value": value,
        })

    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400
    
@class_bp.route('/quiz/<quiz_id>', methods=['GET'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'get_quiz.yaml')) 
def get_quiz(quiz_id):
    try:
        quizservice = QuestionaryService()
        quiz = quizservice.get_by_id(quiz_id)
        print(quiz)

        return jsonify ({
            "quiz_id": str(quiz._id),
            'title': quiz.title,
            'author_id': str(quiz.author_id),
            'created_at': quiz.created_at,
            'questions': quiz.questions
        }),200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }),400
    