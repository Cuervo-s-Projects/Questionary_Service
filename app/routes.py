from flask import Blueprint, request, jsonify
from flasgger import swag_from
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
import os 
import requests
import uuid

from app.service import QuestionaryService

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
swagger_path = os.path.join(root_path, "docs")

class_bp = Blueprint('quiz', __name__)


@class_bp.route('/create', methods=['POST'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'create.yaml')) 
def create():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Obtener el token Bearer del header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token de autorizacion requerido"}), 401
            
        headers = {"Authorization": auth_header}
        
        # Verificar perfil del usuario
        try:
            response = requests.get("http://127.0.0.1:5000/api/profile", headers=headers)
            if response.status_code != 200:
                return jsonify({"message": "Error al verificar perfil de usuario"}), 401
            data_rp = response.json()
        except requests.exceptions.RequestException:
            return jsonify({"message": "Error de conexion con servicio de usuarios"}), 500

        # Verificar tipo de usuario
        try:
            response = requests.get("http://127.0.0.1:5000/api/type_user", headers=headers)
            if response.status_code != 200:
                return jsonify({"message": "Error al verificar tipo de usuario"}), 401
            data_tp = response.json()
            user = data_tp.get('roles')
        except requests.exceptions.RequestException:
            return jsonify({"message": "Error de conexion con servicio de usuarios"}), 500
        
        if user and user[0] == "student":
            return jsonify({
                "message": "El usuario no puede crear cuestionarios"
            }), 403

        # Validar datos requeridos
        if not data.get('title'):
            return jsonify({"message": "El titulo es requerido"}), 400
            
        if not data.get('questions') or len(data.get('questions')) == 0:
            return jsonify({"message": "Debe incluir al menos una pregunta"}), 400

        # Generar ID único para el quiz
        quiz_id = str(uuid.uuid4())

        questionary_service = QuestionaryService()
        status = questionary_service.create(
            id=quiz_id,
            title=data.get('title'),
            author_id=data_rp.get('_id'),
            questions=data.get('questions'),
        )

        return jsonify({
            "message": "Quiz creado exitosamente",
            "quiz_id": quiz_id,
            "status": status
        }), 201

    except Exception as e:
        print(f"Error en create_quiz: {str(e)}")  # Para debugging
        return jsonify({
            "message": f"Error interno del servidor: {str(e)}"
        }), 500
    
@class_bp.route('/assess', methods=['POST'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'assess.yaml')) 
def assess():
    try:
        # Obtener el token Bearer del header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Token de autorizacion requerido"}), 401
            
        headers = {"Authorization": auth_header}
        
        try:
            response = requests.get("http://127.0.0.1:5000/api/profile", headers=headers)
            if response.status_code != 200:
                return jsonify({"message": "Error al verificar perfil de usuario"}), 401
            data_rp = response.json()
            user_id = data_rp.get('_id')
        except requests.exceptions.RequestException:
            return jsonify({"message": "Error de conexion con servicio de usuarios"}), 500

        data = request.get_json()
        
        if not data.get('quiz_id'):
            return jsonify({"message": "quiz_id es requerido"}), 400
            
        if not data.get('reply'):
            return jsonify({"message": "reply es requerido"}), 400
        
        questionary_service = QuestionaryService()
        quiz_id = data.get('quiz_id')
        quiz = questionary_service.get_by_id(quiz_id)

        if not quiz:
            return jsonify({"message": "Quiz no encontrado"}), 404

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
            "total_score": value,
            "max_score": sum(int(q.get('value', 0)) for q in questions),
            "percentage": round((value / sum(int(q.get('value', 0)) for q in questions)) * 100, 2) if questions else 0
        }), 200

    except Exception as e:
        print(f"Error en assess: {str(e)}")  # Para debugging
        return jsonify({
            "message": f"Error interno del servidor: {str(e)}"
        }), 500
    
@class_bp.route('/quiz/<quiz_id>', methods=['GET'])
@jwt_required()
@swag_from(os.path.join(swagger_path, 'get_quiz.yaml')) 
def get_quiz(quiz_id):
    try:
        if not quiz_id:
            return jsonify({"message": "quiz_id es requerido"}), 400
            
        quizservice = QuestionaryService()
        quiz = quizservice.get_by_id(quiz_id)
        
        if not quiz:
            return jsonify({"message": "Quiz no encontrado"}), 404

        return jsonify({
            "quiz_id": str(quiz._id),
            'title': quiz.title,
            'author_id': str(quiz.author_id),
            'created_at': quiz.created_at,
            'questions': quiz.questions
        }), 200

    except Exception as e:
        print(f"Error en get_quiz: {str(e)}")  # Para debugging
        return jsonify({
            "message": f"Error interno del servidor: {str(e)}"
        }), 500
