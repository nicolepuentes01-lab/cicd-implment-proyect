def test_app_init(app):
    """Test that app is created with correct test configuration."""
    assert app.config["TESTING"] is True
    assert "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"].lower()


def test_health_endpoint(client):
    """Test health check endpoint returns ok status."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_404_handler(client):
    """Test that 404 is returned for non-existent routes."""
    r = client.get("/no-existe")
    assert r.status_code == 404
