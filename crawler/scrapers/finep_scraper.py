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

    for page in range(1, 6):  # Altere o range conforme o número de páginas
        params["start"] = (page - 1) * 10  # Ajusta o parâmetro para a paginação
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Encontra os títulos e links dos editais
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
                    insert_into_database(edital_title, None, edital_link, None, None)

        except requests.RequestException as e:
            print(f"Erro ao acessar a página FINEP: {e}")

def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        nome_banca = "FINEP"
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

finep_edital_titles_and_links()


# CHECAR FILTROS. TAMBEM ACHO QUE NAO PEGOU TODOS OS SITES. OS FILTROS ACHO QUE ESTAO ERRADOS, PEGOU UM DE 2015 DO NADA. CORRIGIR, MAS ESTA NO CAMINHO CERTO.
# link para teste http://www.finep.gov.br/chamadas-publicas/chamadaspublicas?tema[0]=5G%20e%20Wi-fi%206&tema[1]=Agritech&tema[2]=Biotecnologia&tema[3]=Fintech&tema[4]=Foodtech&tema[5]=Intelig%C3%AAncia%20artificial%20(IA)&tema[6]=Internet%20das%20Coisas%20-%20IoT&tema[7]=Tecnologia%20Assitiva&tema[8]=Tecnologia%20Espacial&tema[9]=Tecnologia%20Social&tema[10]=TICs%20-%20Tecnologia%20de%20Informa%C3%A7%C3%A3o%20e%20Comunica%C3%A7%C3%A3o&situacao=aberta&boxchecked=0&filter_order=ordering&filter_order_Dir=asc&3348a20b7b3921308c4da261e3fc6d98=1&start=40