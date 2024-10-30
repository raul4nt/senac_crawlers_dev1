import requests
from bs4 import BeautifulSoup

def get_vencimento(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Tentar encontrar a tag <p> que contém a data de vencimento
        vencimento_element = soup.find("p", class_="has-vivid-cyan-blue-color")
        
        if vencimento_element:
            # Pega o texto da tag <p>
            texto = vencimento_element.text.strip()
            # Extrai as datas do texto
            datas = [data.strip() for data in texto.split(" ") if "/" in data]
            if len(datas) >= 2:
                # Retorna a última data
                return datas[-1]
        
        return "Vencimento não encontrado."
    
    except requests.RequestException as e:
        print(f"Erro ao acessar o edital: {e}")
        return "Erro ao acessar o edital."

# Testar a função com o link do edital específico
edital_link = "https://fapesc.sc.gov.br/edital-de-chamada-publica-fapesc-no-56-2024-fapesc-iai-step-fellowship-program-mdic/"
vencimento = get_vencimento(edital_link)
print(f"Data de vencimento do edital:\n{vencimento}")
