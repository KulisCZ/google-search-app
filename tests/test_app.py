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
        assert all("title" in item and "link" in item and "snippet" in item for item in response.json())
        
def test_search_error():
    with patch("app.requests.post") as mock_post:
        mock_post.return_value.json.side_effect = Exception("API error")

        response = client.get("/search?query=windows")

        assert response.status_code == 500
        
def test_only_organic_results_are_returned():
    fake_response = {
        "organic": [
            {
                "title": "Organic result",
                "link": "https://example.com",
                "snippet": "Organic snippet"
            }
        ],
        "news": [
            {
                "title": "News result",
                "link": "https://news.example.com"
            }
        ],
        "peopleAlsoAsk": [
            {
                "question": "Some question?"
            }
        ]
    }

    with patch("app.requests.post") as mock_post:
        mock_post.return_value.json.return_value = fake_response

        response = client.get("/search?query=windows")

        assert response.status_code == 200
        assert response.json() == fake_response["organic"]
        
def test_search_uses_first_page():
    with patch("app.requests.post") as mock_post:
        mock_post.return_value.json.return_value = fake_response

        response = client.get("/search?query=windows")
        mock_post.assert_called_once_with(
            "https://google.serper.dev/search",
            headers=mock_post.call_args.kwargs["headers"],
            json={
                "q": "windows",
                "page": 1
            }
        )