import requests

def fetch_github_data():
    """Faz a requisição à API do GitHub e retorna um dicionário com status e mensagem."""
    try:
        response = requests.get("https://api.github.com", timeout=5)
        response.raise_for_status()
        try:
            url = response.json().get("current_user_url", "Chave não encontrada")
        except ValueError:
            return {"status": "error", "message": "Erro inesperado: resposta não é JSON válido"}
        return {"status": "success", "message": "Conexão bem-sucedida", "url": url}
    except requests.exceptions.HTTPError as http_err:
        return {"status": "error", "message": f"Erro HTTP: {http_err}"}
    except requests.exceptions.ConnectionError:
        return {"status": "error", "message": "Erro de conexão. Verifique sua internet."}
    except requests.exceptions.Timeout:
        return {"status": "error", "message": "Tempo de resposta excedido."}
    except requests.exceptions.RequestException as err:
        return {"status": "error", "message": f"Erro inesperado: {err}"}

def main():
    result = fetch_github_data()
    if result["status"] == "success":
        print("✅", result["message"])
        print("🔗 URL do usuário atual:", result["url"])
    else:
        print("❌", result["message"])

if __name__ == "__main__":
    main()