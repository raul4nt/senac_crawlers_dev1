import requests
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres.akerwwnultjhmvdixfmm",
    "password": "senaccrawlerbr1234",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "6543",
}

def get_fapesc_edital_titles_and_links():
    url = "https://fapesc.sc.gov.br/category/chamadas-abertas/"
    
    try:
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
            
            # Obtém a descrição do edital
            descricao = get_edital_descricao(edital_link)
            # Obtém a data de publicação do edital
            data_publicacao_str = get_edital_publication_date(edital_link)
            data_publicacao = convert_date_format(data_publicacao_str)
            # Obtém a data de vencimento do edital
            vencimento_str = get_vencimento(edital_link)
            vencimento = convert_date_format(vencimento_str)
            
            insert_into_database(edital_title, descricao, edital_link, data_publicacao, vencimento)
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página FAPESC: {e}")

def get_edital_descricao(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Tentar encontrar o primeiro parágrafo que parece ser a descrição
        descricao_element = soup.find("p")
        if descricao_element:
            return descricao_element.text.strip()
        
        return "Descrição não encontrada."
    
    except requests.RequestException as e:
        print(f"Erro ao acessar o edital: {e}")
        return "Erro ao acessar o edital."

def get_edital_publication_date(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontrar a tag <time> dentro do span apropriado
        date_element = soup.find('span', class_='elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date')
        if date_element:
            publication_date = date_element.find('time')
            if publication_date:
                return publication_date.text.strip()
        return "Data de publicação não encontrada."

    except requests.RequestException as e:
        print(f"Erro ao acessar o edital: {e}")
        return "Erro ao acessar o edital."

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

def convert_date_format(date_str):
    """Converte a data do formato DD/MM/YYYY para YYYY-MM-DD."""
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        print(f"Formato de data inválido: {date_str}")
        return None

def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        nome_banca = "FAPESC"
        valor = 0.0
        prazo_execucao = None
        valor_global = 0.0
        valor_estimado = 0.0
        valor_maximo = 0.0

        insert_query = """
            INSERT INTO edital (nome_banca, titulo, valor, descricao, link, 
            id_site, img_logo, vencimento, prazo_execucao, valor_global, 
            valor_estimado, valor_maximo, data_publicacao)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (nome_banca, titulo, valor, descricao, link,
                                       None, None, vencimento, prazo_execucao,
                                       valor_global, valor_estimado, valor_maximo, 
                                       data_publicacao))

        conn.commit()
        print("Dados inseridos com sucesso.")
    
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    
    finally:
        cursor.close()
        conn.close()

# Para obter e armazenar os títulos, links, descrições, data de publicação e vencimento
get_fapesc_edital_titles_and_links()



# 
