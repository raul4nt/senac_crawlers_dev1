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

def rnp_edital_titles_links_and_descriptions():
    url = "https://www.rnp.br/inovacao/editais"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Localiza a seção "Editais abertos"
        editais_abertos_section = soup.find('h3', string="Editais abertos")
        
        if editais_abertos_section:
            # Move para o próximo elemento (que contém os editais)
            editais_list = editais_abertos_section.find_next('div')  # Ajuste conforme necessário

            if editais_list:
                # Busca os títulos e links dentro da seção encontrada
                titles = editais_list.find_all("strong")

                if not titles:
                    print("Nenhum título encontrado na seção de Editais Abertos.")
                    return
                
                for title in titles:
                    edital_title = title.text.strip()
                    # Encontrar o link relacionado à tag <strong>
                    edital_link = title.find_parent("a")["href"] if title.find_parent("a") else None
                    
                    # Se não conseguir encontrar o link direto, busca na seção que envolve a tag <strong>
                    if edital_link is None:
                        link_parent = title.find_parent('div')  # Ajuste conforme necessário
                        if link_parent:
                            edital_link_tag = link_parent.find('a')
                            if edital_link_tag:
                                edital_link = edital_link_tag['href']
                    
                    # Agora, vamos obter a descrição do edital
                    descricao = get_edital_description(editais_list, title)

                    # Exibindo o título, link e descrição no console
                    print(f"Título: {edital_title}, Link: {edital_link}, Descrição: {descricao}")
                    
                    # Inserir no banco de dados (ainda que as outras informações sejam None por enquanto)
                    insert_into_database(edital_title, descricao, edital_link, None, None)
            else:
                print("Seção de editais não encontrada após 'Editais abertos'.")
        else:
            print("Seção 'Editais abertos' não encontrada.")
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página RNP: {e}")

def get_edital_description(editais_list, title):
    """Obtém a descrição do edital da lista de editais, procurando após o título."""
    try:
        # Procurar o próximo <p> após o título para obter a descrição
        description_element = title.find_next('p')
        if description_element:
            return description_element.text.strip()
        
        return "Descrição não encontrada."
    
    except Exception as e:
        print(f"Erro ao obter a descrição: {e}")
        return "Erro ao acessar a descrição."

def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        nome_banca = "RNP"
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

# Chamada da função para obter títulos, links e descrições dos editais
rnp_edital_titles_links_and_descriptions()
