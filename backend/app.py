import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from database import init_db
from routes.contact import contact_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for frontend API calls
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database
    init_db(app)

    # Register Contact Blueprint
    app.register_blueprint(contact_bp)

    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "message": "Kathiresan Portfolio REST API is operational",
            "recipient": app.config.get("MAIL_TO", "kathiresantoto@gmail.com"),
            "database": "connected"
        }), 200

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    print(f"[INFO] Kathiresan Portfolio Backend API starting on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
