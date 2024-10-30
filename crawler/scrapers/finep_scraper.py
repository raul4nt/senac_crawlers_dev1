import requests
from bs4 import BeautifulSoup
from datetime import datetime

def finep_edital_titles_and_links():
    base_url = "http://www.finep.gov.br/chamadas-publicas/chamadaspublicas"
    params = {
        "tema[0]": "5G e Wi-fi 6",
        "tema[1]": "Agritech",
        "tema[2]": "Biotecnologia",
        "tema[3]": "Fintech",
        "tema[4]": "Foodtech",
        "tema[5]": "Inteligência artificial (IA)",
        "tema[6]": "Internet das Coisas - IoT",
        "tema[7]": "Tecnologia Assistiva",
        "tema[8]": "Tecnologia Espacial",
        "tema[9]": "Tecnologia Social",
        "tema[10]": "TICs - Tecnologia de Informação e Comunicação",
        "situacao": "aberta",
        "boxchecked": "0",
        "filter_order": "ordering",
        "filter_order_Dir": "asc",
        "3348a20b7b3921308c4da261e3fc6d98": "1"
    }

    for page in range(1, 6):
        params["start"] = (page - 1) * 10
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            editais = soup.find_all('h3')
            if not editais:
                print(f"Nenhum edital encontrado na página {page}.")
                continue

            for edital in editais:
                link_tag = edital.find('a')
                if link_tag:
                    edital_title = link_tag.text.strip()
                    edital_link = link_tag['href']
                    print(f"Título: {edital_title}, Link: {edital_link}")

                    # Obtém a descrição e as datas do edital
                    descricao = "Descrição não disponível"  # Ajuste conforme necessário
                    vencimento = "2024-11-30"  # Exemplo; ajuste conforme necessário
                    data_publicacao = datetime.now().date()  # Data atual

                    # Envia para a API
                    insert_into_api(edital_title, descricao, edital_link, vencimento, data_publicacao)

        except requests.RequestException as e:
            print(f"Erro ao acessar a página FINEP: {e}")

def insert_into_api(titulo, descricao, link, vencimento, data_publicacao):
    api_url = "https://senac-crawlers.onrender.com/api/editais/"
    data = {
        "nome_banca": "FINEP",
        "titulo": titulo,
        "valor": 0.0,  # Ajuste se houver um valor específico
        "descricao": descricao,
        "link": link if link.startswith('http') else f"https://www.finep.gov.br{link}",
        "img_logo": None,  # Adicione o logo se necessário
        "vencimento": vencimento,
        "prazo_execucao": None,  # Ajuste conforme necessário
        "valor_global": 0.0,  # Ajuste se houver um valor específico
        "valor_estimado": 0.0,  # Ajuste se houver um valor específico
        "valor_maximo": 0.0,  # Ajuste se houver um valor específico
        "data_publicacao": data_publicacao.isoformat()  # Converte para formato ISO
    }

    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        print("Dados inseridos na API com sucesso.")

    except requests.RequestException as e:
        print(f"Erro ao inserir dados na API: {e} - {response.text}")

finep_edital_titles_and_links()
