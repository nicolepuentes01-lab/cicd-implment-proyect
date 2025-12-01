import os
import importlib
import importlib.util
import pathlib
import pytest
from flask import Flask
from model.db import db


def _load_create_app():
    try:
        mod = importlib.import_module("app")
        if hasattr(mod, "create_app"):
            return getattr(mod, "create_app")
    except Exception:
        pass
    try:
        from app import create_app  # type: ignore
        return create_app
    except Exception:
        pass
    app_py = pathlib.Path(__file__).resolve().parents[1] / "app.py"
    if app_py.exists():
        spec = importlib.util.spec_from_file_location("app_fallback", str(app_py))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "create_app"):
                return getattr(mod, "create_app")
    def _factory():
        app = Flask(__name__)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app)
        return app
    return _factory


@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    monkeypatch.setenv("TESTING", "true")
    monkeypatch.setenv("FLASK_ENV", "testing")
    monkeypatch.setenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture
def app():
    create_app = _load_create_app()
    application = create_app()
    application.config["TESTING"] = True
    application.config["PROPAGATE_EXCEPTIONS"] = True
    application.config.setdefault("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
    with application.app_context():
        db.create_all()
        try:
            yield application
        finally:
            db.session.remove()
            db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
