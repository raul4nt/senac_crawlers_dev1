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

def delete_all_editais():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        delete_query = "DELETE FROM edital;"
        cursor.execute(delete_query)

        conn.commit()
        print("Todos os editais foram deletados com sucesso.")
    
    except Exception as e:
        print(f"Erro ao deletar os editais do banco de dados: {e}")
    
    finally:
        cursor.close()
        conn.close()

delete_all_editais()