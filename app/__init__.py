from flask import Flask
from flask_cors import CORS
from config import Config
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

from app.metrics import setup_metrics
from app.document_routes import documents_bp
from app.routes import class_bp
from app.extensions import jwt, swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    jwt.init_app(app)
    swagger.init_app(app)

    # Inicializar Prometheus
    setup_metrics(app)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    })

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    app.register_blueprint(class_bp, url_prefix="/api/class")
    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    print("Rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(rule)
    return app
