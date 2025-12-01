def test_health_json_format(client):
    """Test that health endpoint returns proper JSON format."""
    resp = client.get("/health")
    assert resp.status_code == 200
    json_data = resp.get_json()
    assert json_data is not None
    assert "status" in json_data
    assert json_data["status"] == "ok"
