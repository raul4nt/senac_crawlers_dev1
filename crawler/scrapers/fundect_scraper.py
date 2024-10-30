import requests
from bs4 import BeautifulSoup
import psycopg2

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres.akerwwnultjhmvdixfmm",
    "password": "senaccrawlerbr1234",
    "host": "aws-0-sa-east-1.pooler.supabase.com",
    "port": "6543",
}

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
                    
                    # Inserir no banco de dados
                    insert_into_database(edital_title, None, edital_link, None, None)
            else:
                print("Lista de editais não encontrada.")
        else:
            print("Seção 'Chamadas Abertas' não encontrada.")
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página Fundect: {e}")


def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        nome_banca = "Fundect"
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
                                       None))

        conn.commit()
        print("Dados inseridos com sucesso.")
    
    except Exception as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    
    finally:
        cursor.close()
        conn.close()

fundect_edital_titles_and_links()
