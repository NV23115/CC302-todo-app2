def test_home_page():
    from app import app
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code in [200, 302]  # fixed