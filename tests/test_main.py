import pytest
from unittest.mock import patch, Mock
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import main


# -----------------------------
# Casos POSITIVOS
# -----------------------------
def test_success_basic():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "url_teste"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["status"] == "success"
    assert "Conexão bem-sucedida" in result["message"]
    assert result["url"] == "url_teste"


def test_success_missing_key():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["url"] == "Chave não encontrada"


def test_success_multiple_calls():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        results = [main.fetch_github_data() for _ in range(3)]

    assert all(r["status"] == "success" for r in results)


def test_success_status_code_200():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "teste200"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["url"] == "teste200"


def test_success_custom_url():
    url = "https://api.github.com/custom"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": url}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["url"] == url


def test_success_not_empty_message():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "url"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["message"] != ""


def test_success_with_different_key():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"another_key": "ignored"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["url"] == "Chave não encontrada"


def test_success_url_format():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "https://api.github.com/user"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert result["url"].startswith("https://")


def test_success_multiple_urls():
    urls = ["url1", "url2", "url3"]
    for u in urls:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"current_user_url": u}
        mock_response.raise_for_status.return_value = None

        with patch("requests.get", return_value=mock_response):
            result = main.fetch_github_data()
            assert result["url"] == u


def test_success_call_not_crash():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"current_user_url": "ok"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert isinstance(result, dict)


# -----------------------------
# Casos NEGATIVOS
# -----------------------------
def test_http_error():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Erro 404")

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert "Erro HTTP" in result["message"]


def test_connection_error():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError):
        result = main.fetch_github_data()

    assert "Erro de conexão" in result["message"]


def test_timeout_error():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = main.fetch_github_data()

    assert "Tempo de resposta" in result["message"]


def test_generic_request_exception():
    with patch("requests.get", side_effect=requests.exceptions.RequestException("falha")):
        result = main.fetch_github_data()

    assert "Erro inesperado" in result["message"]


def test_invalid_json():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("JSON inválido")

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert "não é JSON válido" in result["message"]
    

def test_unexpected_status_code():
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert "Erro HTTP" in result["message"]


def test_request_exception_text():
    with patch("requests.get", side_effect=requests.exceptions.RequestException("falhou feio")):
        result = main.fetch_github_data()

    assert "falhou feio" in result["message"]


def test_connection_reset():
    with patch("requests.get", side_effect=requests.exceptions.ConnectionError("reset by peer")):
        result = main.fetch_github_data()

    assert "reset by peer" in result["message"] or "Erro de conexão" in result["message"]


def test_timeout_message_clear():
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result = main.fetch_github_data()

    assert "excedido" in result["message"]


def test_http_error_contains_code():
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Forbidden")

    with patch("requests.get", return_value=mock_response):
        result = main.fetch_github_data()

    assert "403" in result["message"]