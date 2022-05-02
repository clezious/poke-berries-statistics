from app.main import app, get_berries, get_berry_growth_time
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

client = TestClient(app)


@patch("app.main.get")
def test_get_berries(mock_get):
    mock_response = {
        "count": 3,
        "next": "https://pokeapi.co/api/v2/berry?offset=20&limit=20",
        "previous": None,
        "results": [
            {"name": "cheri", "url": "https://pokeapi.co/api/v2/berry/1/"},
            {"name": "chesto", "url": "https://pokeapi.co/api/v2/berry/2/"},
            {"name": "pecha", "url": "https://pokeapi.co/api/v2/berry/3/"},
        ],
    }
    mock_get.return_value = Mock(ok=True, status_code=200, json=lambda: mock_response)
    assert get_berries("test_url") == mock_response


@patch("app.main.get")
def test_get_berry_growth_time(mock_get):
    mock_growth_time = 10
    mock_response = {"growth_time": mock_growth_time}
    mock_get.return_value = Mock(ok=True, status_code=200, json=lambda: mock_response)
    assert get_berry_growth_time("test_url") == mock_growth_time


@patch("app.main.get_berry_growth_time")
@patch("app.main.get_berries")
def test_allBerryStats(mock_get_berries, mock_get_berry_growth_time):
    mock_get_berry_growth_time.return_value = 1
    mock_get_berries.return_value = {
        "next": None,
        "results": [
            {"name": "test", "url": "test"},
            {"name": "test2", "url": "test2"},
        ],
    }
    response = client.get("/allBerryStats")
    assert response.status_code == 200
    assert response.json() == {
        "berries_names": [
            "test",
            "test2",
        ],
        "min_growth_time": 1,
        "median_growth_time": 1.0,
        "max_growth_time": 1,
        "variance_growth_time": 0.0,
        "mean_growth_time": 1.0,
        "frequency_growth_time": {
            "1": 2,
        },
    }
