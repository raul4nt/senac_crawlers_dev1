import requests
from bs4 import BeautifulSoup
from datetime import datetime

API_URL = "https://senac-crawlers.onrender.com/api/editais/"  # Ajuste para o endpoint correto

def rnp_edital_titles_links_and_descriptions():
    url = "https://www.rnp.br/inovacao/editais"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Localiza a seção "Editais abertos"
        editais_abertos_section = soup.find('h3', string="Editais abertos")
        
        if editais_abertos_section:
            editais_list = editais_abertos_section.find_next('div')  # Ajuste conforme necessário

            if editais_list:
                titles = editais_list.find_all("strong")

                if not titles:
                    print("Nenhum título encontrado na seção de Editais Abertos.")
                    return
                
                for title in titles:
                    edital_title = title.text.strip()
                    edital_link = title.find_parent("a")["href"] if title.find_parent("a") else None
                    
                    if edital_link is None:
                        link_parent = title.find_parent('div')
                        if link_parent:
                            edital_link_tag = link_parent.find('a')
                            if edital_link_tag:
                                edital_link = edital_link_tag['href']
                    
                    descricao = get_edital_description(editais_list, title)

                    # Exibindo o título, link e descrição no console
                    print(f"Título: {edital_title}, Link: {edital_link}, Descrição: {descricao}")
                    
                    # Inserir na API
                    insert_into_api(edital_title, descricao, edital_link, None, None)
            else:
                print("Seção de editais não encontrada após 'Editais abertos'.")
        else:
            print("Seção 'Editais abertos' não encontrada.")
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página RNP: {e}")

def get_edital_description(editais_list, title):
    try:
        description_element = title.find_next('p')
        if description_element:
            return description_element.text.strip()
        
        return "Descrição não encontrada."
    
    except Exception as e:
        print(f"Erro ao obter a descrição: {e}")
        return "Erro ao acessar a descrição."

def insert_into_api(titulo, descricao, link, data_publicacao, vencimento):
    payload = {
        "nome_banca": "RNP",
        "titulo": titulo,
        "valor": 0.0,
        "descricao": descricao,
        "link": link,
        "img_logo": None,
        "vencimento": vencimento,
        "prazo_execucao": None,
        "valor_global": 0.0,
        "valor_estimado": 0.0,
        "valor_maximo": 0.0,
        "data_publicacao": None  # Ajuste se você tiver essa informação
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        print("Dados inseridos na API com sucesso.")
    except requests.RequestException as e:
        print(f"Erro ao inserir dados na API: {e}")

# Chamada da função para obter títulos, links e descrições dos editais
rnp_edital_titles_links_and_descriptions()

# corrigir scraper