import requests

def main():
    try:
        response = requests.get("https://api.github.com", timeout=5)
        response.raise_for_status()  # Lança exceção para códigos de erro HTTP
        print("✅ Conexão bem-sucedida com a API do GitHub!")
        print("🔗 URL do usuário atual:", response.json().get("current_user_url", "Chave não encontrada"))
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erro HTTP: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão. Verifique sua internet.")
    except requests.exceptions.Timeout:
        print("⏱️ Tempo de resposta excedido.")
    except requests.exceptions.RequestException as err:
        print(f"❌ Erro inesperado: {err}")

if __name__ == "__main__":
    main()