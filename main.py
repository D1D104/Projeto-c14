import requests

def main():
    response = requests.get("https://api.github.com")
    if response.status_code == 200:
        print("Conexão bem-sucedida com a API do GitHub!")
        print(response.json()["current_user_url"])
    else:
        print("Erro ao acessar a API.")

if __name__ == "__main__":
    main()
