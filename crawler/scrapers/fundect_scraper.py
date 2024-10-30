import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fundect_edital_titles_and_links():
    url = "https://www.fundect.ms.gov.br/category/chamadas-abertas/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Localiza a seção "Chamadas Abertas"
        editais_abertos_section = soup.find('h1', class_="green")
        
        if editais_abertos_section:
            # Move para a lista de editais que seguem a seção
            editais_list = editais_abertos_section.find_next('div', class_='card-body')
            
            if editais_list:
                # Busca os cartões de editais na seção
                cards = soup.find_all("div", class_="card")
                
                if not cards:
                    print("Nenhum edital encontrado na seção de Chamadas Abertas.")
                    return
                
                for card in cards:
                    # Encontrar o título do edital
                    edital_title = card.find('h5', class_='card-title').text.strip()
                    # Encontrar o link do edital
                    edital_link = card.find('a')['href'] if card.find('a') else None
                    
                    # Exibindo o título e link no console
                    print(f"Título: {edital_title}, Link: {edital_link}")

                    # Obtém a descrição e as datas do edital
                    descricao = "Descrição não disponível"  # Ajuste conforme necessário
                    vencimento = "2024-11-30"  # Exemplo; ajuste conforme necessário
                    data_publicacao = datetime.now().date()  # Data atual

                    # Envia para a API
                    insert_into_api(edital_title, descricao, edital_link, vencimento, data_publicacao)
            else:
                print("Lista de editais não encontrada.")
        else:
            print("Seção 'Chamadas Abertas' não encontrada.")
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página Fundect: {e}")

def insert_into_api(titulo, descricao, link, vencimento, data_publicacao):
    api_url = "https://senac-crawlers.onrender.com/api/editais/"
    data = {
        "nome_banca": "Fundect",
        "titulo": titulo,
        "valor": 0.0,  # Ajuste se houver um valor específico
        "descricao": descricao,
        "link": link if link.startswith('http') else f"https://www.fundect.ms.gov.br{link}",
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
        print(f"Erro ao inserir dados na API: {e} - {response.text if 'response' in locals() else ''}")

fundect_edital_titles_and_links()
