import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from model.db import db
load_dotenv()


def _database_url_from_env():
    return os.getenv("SQLALCHEMY_DATABASE_URI")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = _database_url_from_env()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    from model.producto import Producto  # noqa: F401
    from model.cliente import Cliente    # noqa: F401
    from model.pedido import Pedido      # noqa: F401
    auto = os.getenv("AUTO_CREATE_DB", "false").lower() in {"1", "true", "yes"}
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "") or ""
    if auto or uri.startswith("sqlite"):
        with app.app_context():
            try:
                db.create_all()
            except Exception:
                pass

    # Register blueprints
    from controllers.producto import api as producto_api
    app.register_blueprint(producto_api, url_prefix="/api")

    from controllers.cliente import cliente_api
    app.register_blueprint(cliente_api, url_prefix="/api")

    from controllers.pedido import pedido_api
    app.register_blueprint(pedido_api, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app

# For gunicorn: app:create_app()
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
