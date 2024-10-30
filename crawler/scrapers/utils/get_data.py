import psycopg2

# Configurações de conexão com o banco de dados
DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres.akerwwnultjhmvdixfmm',
    'password': 'senaccrawlerbr1234',
    'host': 'aws-0-sa-east-1.pooler.supabase.com',
    'port': '6543',
}

def get_connection():
    """Estabelece e retorna uma conexão com o banco de dados PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)

def get_edital_data():
    """Recupera e exibe todos os dados da tabela edital no banco de dados PostgreSQL."""
    try:
        # Conectar ao banco de dados
        conn = get_connection()
        cursor = conn.cursor()

        # Comando SQL para selecionar todos os dados da tabela edital
        select_query = "SELECT * FROM edital;"
        cursor.execute(select_query)

        # Recuperar todos os registros
        registros = cursor.fetchall()

        # Verifica se há registros
        if not registros:
            print("Nenhum edital encontrado.")
            return

        # Imprimir os dados
        for registro in registros:
            id, nome_banca, titulo, valor, descricao, link, id_site, img_logo, vencimento, prazo_execucao, valor_global, valor_estimado, valor_maximo, data_publicacao = registro
            print(f"ID: {id}, Nome da Banca: {nome_banca}, Título: {titulo}, Valor: {valor}, "
                  f"Descrição: {descricao}, Link: {link}, ID do Site: {id_site}, "
                  f"Logo: {img_logo}, Vencimento: {vencimento}, Prazo de Execução: {prazo_execucao}, "
                  f"Valor Global: {valor_global}, Valor Estimado: {valor_estimado}, "
                  f"Valor Máximo: {valor_maximo}, Data de Publicação: {data_publicacao}")

    except Exception as e:
        print(f"Erro ao recuperar dados do banco de dados: {e}")

    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        conn.close()

# Chamar a função para obter e exibir os dados da tabela edital
if __name__ == "__main__":
    get_edital_data()
