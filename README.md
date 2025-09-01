# Projeto Python com Pipenv

Este repositório demonstra como configurar um ambiente isolado com Pipenv, instalar dependências, executar um script Python e rodar um script de build simples.

---

## Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes do Python)
- Pipenv

---

## Instalação e Configuração

```bash
pip install pipenv
pipenv install --dev
pipenv shell
python main.py

```

## 📂 Estrutura dos testes

Os testes estão organizados em dois blocos principais:

### ✅ Casos Positivos

Simulam cenários onde a requisição é bem-sucedida (`status_code == 200`), usando **mocks** para controlar a resposta da API.

Cobrem:

- Retorno correto quando a chave `current_user_url` existe.
- Comportamento quando a chave está ausente.
- Múltiplas chamadas consecutivas.
- URLs personalizadas.
- Mensagem de sucesso não vazia.
- Formato da URL retornada.
- Diferentes valores de URL.
- Garantia de que a função não quebre e retorne sempre um dicionário.

### ❌ Casos Negativos

Simulam erros de rede, HTTP e dados inválidos, também usando **mocks** e exceções do `requests`.

Cobrem:

- `HTTPError` com diferentes códigos (404, 403, 500).
- `ConnectionError` (incluindo "reset by peer").
- `Timeout`.
- `RequestException` genérica.
- Resposta com JSON inválido (`ValueError`).
- Mensagens de erro claras e contendo detalhes relevantes.

---

## ▶️ Como executar os testes

pipenv run pytest -v

## Histórico de Bugs

### Bug: Chave incorreta no JSON da API do GitHub

**Data:** 01/09/2025  
**Descrição:** Durante uma refatoração, a função `fetch_github_data()` passou a buscar a chave `current_user` no JSON retornado pela API do GitHub, em vez de `current_user_url`.  
**Impacto:** Quebra de múltiplos testes de sucesso (`test_success_basic`, `test_success_status_code_200`, `test_success_custom_url`, etc.), pois a função retornava `"Chave não encontrada"` mesmo quando a resposta era válida.  
**Correção:** Alterar a linha:

```python
url = response.json().get("current_user", "Chave não encontrada")
```
