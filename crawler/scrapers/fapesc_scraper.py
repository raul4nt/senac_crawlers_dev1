import requests
from bs4 import BeautifulSoup
from datetime import datetime

API_URL = "https://senac-crawlers.onrender.com/api/editais/"

def get_fapesc_edital_titles_and_links():
    url = "https://fapesc.sc.gov.br/category/chamadas-abertas/"
    
    try:
        print("Acessando a página de editais da FAPESC...")
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.find_all("h2", class_="entry-title")

        if not titles:
            print("Nenhum título encontrado na FAPESC.")
            return
        
        for title in titles:
            edital_title = title.text.strip()
            edital_link = title.find("a")["href"]

            print(f"Processando edital: {edital_title}")

            # Obtém a descrição e as datas em uma única chamada
            descricao, data_publicacao, vencimento = get_edital_details(edital_link)
            
            # Verifica se a descrição ou data_publicacao são None
            if descricao is None:
                print(f"Descrição não encontrada para o edital: {edital_title}")

            if data_publicacao is None:
                print(f"Data de publicação não encontrada para o edital: {edital_title}")

            if vencimento is None:
                print(f"Vencimento não encontrado para o edital: {edital_title}")

            # Insere os dados na API apenas se a descrição estiver presente
            if descricao:
                insert_into_api(edital_title, descricao, edital_link, data_publicacao, vencimento)
            else:
                print(f"Falha ao obter detalhes para o edital: {edital_title}")

    except requests.RequestException as e:
        print(f"Erro ao acessar a página FAPESC: {e}")


def get_edital_details(link):
    """Obtém a descrição, data de publicação e vencimento do edital."""
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Obtém a descrição
        descricao_element = soup.find("p")
        descricao = descricao_element.text.strip() if descricao_element else "Descrição não encontrada."

        # Obtém a data de publicação
        date_element = soup.find('span', class_='elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date')
        publication_date = date_element.find('time').text.strip() if date_element else "Data de publicação não encontrada."

        # Obtém a data de vencimento
        vencimento_element = soup.find("p", class_="has-vivid-cyan-blue-color")
        if vencimento_element:
            texto = vencimento_element.text.strip()
            datas = [data.strip() for data in texto.split(" ") if "/" in data]
            vencimento = datas[-1] if len(datas) >= 2 else "Vencimento não encontrado."
        else:
            vencimento = "Vencimento não encontrado."
        
        return descricao, convert_date_format(publication_date), convert_date_format(vencimento)

    except requests.RequestException as e:
        print(f"Erro ao acessar o edital: {e}")
        return None, None, None

def convert_date_format(date_str):
    """Converte a data do formato DD/MM/YYYY para YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        print(f"Formato de data inválido: {date_str}")
        return None

def insert_into_api(titulo, descricao, link, data_publicacao, vencimento):
    """Insere os dados do edital na API."""
    # Trunca o título se ele exceder 150 caracteres
    titulo_truncado = titulo[:150] if len(titulo) > 150 else titulo

    data = {
        "nome_banca": "FAPESC",
        "titulo": titulo_truncado,
        "valor": 0.0,  # Ajuste se houver um valor específico
        "descricao": descricao,
        "link": link if link.startswith('http') else f"https://fapesc.sc.gov.br{link}",
        "img_logo": None,  # Adicione o logo se necessário
        "vencimento": vencimento.isoformat() if vencimento else None,  # Converte para formato ISO se não for None
        "prazo_execucao": None,  # Ajuste conforme necessário
        "valor_global": 0.0,  # Ajuste se houver um valor específico
        "valor_estimado": 0.0,  # Ajuste se houver um valor específico
        "valor_maximo": 0.0,  # Ajuste se houver um valor específico
        "data_publicacao": data_publicacao.isoformat() if data_publicacao else None  # Converte para formato ISO se não for None
    }

    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        print("Dados inseridos na API com sucesso.")

    except requests.RequestException as e:
        print(f"Erro ao inserir dados na API: {e} - {response.text}")

# Para obter e armazenar os títulos, links, descrições, data de publicação e vencimento
get_fapesc_edital_titles_and_links()


# este está demorando muito, mas esta inserindo normal.
# coloquei uns prints de processando edital, acesso a pagina e etc pra mostrar que só está demorado mesmo
# corrigir msg duplicada: Formato de data inválido: Vencimento não encontrado.
# Vencimento não encontrado para o edital: Edital de Chamada Pública Fapesc nº 12/2