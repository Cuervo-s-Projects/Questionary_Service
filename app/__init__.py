from flask import Flask
from flask_cors import CORS
from config import Config
from app.extensions import jwt, swagger
from app.routes import class_bp
from app.document_routes import documents_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    swagger.init_app(app)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    app.register_blueprint(class_bp, url_prefix="/api/class")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    #print(app.url_map)
    return app
