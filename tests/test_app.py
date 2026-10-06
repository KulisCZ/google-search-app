from app import app
from fastapi.testclient import TestClient
from unittest.mock import patch

client = TestClient(app)
fake_response = {
    "organic": [
        {
            "title": "Test result 1",
            "link": "https://example.com",
            "snippet": "Test snippet 1"
        },
        {
            "title": "Test result 2",
            "link": "https://example.org",
            "snippet": "Test snippet 2"
        }
    ]
}
def test_search():
    with patch("app.requests.post") as mock_post:
        mock_post.return_value.json.return_value = fake_response
        response = client.get("/search?query=windows")
        assert response.status_code == 200
        assert response.json() == fake_response["organic"]
        assert len(response.json()) <= 10
        assert all("title" in item and "link" in item and "snippet" in item for item in response.json())
        
def test_search_error():
    with patch("app.requests.post") as mock_post:
        mock_post.return_value.json.side_effect = Exception("API error")

        response = client.get("/search?query=windows")

        assert response.status_code == 500