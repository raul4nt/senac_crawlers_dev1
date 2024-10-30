# import requests
# from bs4 import BeautifulSoup

# def get_fapesc_edital_titles_and_links():
#     # URL da página
#     url = "https://fapesc.sc.gov.br/category/chamadas-abertas/"
    
#     # Fazer a requisição para o site
#     response = requests.get(url)
    
#     # Verificar se a requisição foi bem-sucedida
#     if response.status_code == 200:
#         # Processar o conteúdo HTML da página
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Encontrar todos os elementos que correspondem aos títulos dos editais
#         titles = soup.find_all('h2', class_='entry-title')
        
#         # Extrair e exibir o título e o link de cada edital
#         for title in titles:
#             # Extrair o texto do título
#             edital_title = title.text.strip()
            
#             # Extrair o link do edital, presente no elemento <a> dentro do <h2>
#             edital_link = title.find('a')['href']
            
#             # Exibir título e link
#             print(f"Título: {edital_title}")
#             print(f"Link: {edital_link}\n")
#     else:
#         print(f"Erro ao acessar a página. Status code: {response.status_code}")

# def get_fapergs_edital_titles_and_links():
#     # URL da página
#     url = "https://fapergs.rs.gov.br/abertos"
    
#     # Fazer a requisição para o site
#     response = requests.get(url)
    
#     # Verificar se a requisição foi bem-sucedida
#     if response.status_code == 200:
#         # Processar o conteúdo HTML da página
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # Encontrar todos os elementos com a classe 'conteudo-lista__item__titulo'
#         titles = soup.find_all('h2', class_='conteudo-lista__item__titulo')
        
#         # Verificar se algum título foi encontrado
#         if not titles:
#             print("Nenhum título encontrado.")
#             return
        
#         # Extrair e exibir o título e o link de cada edital
#         for title in titles:
#             # Encontrar o elemento <a> dentro do <h2>
#             link_tag = title.find('a')
#             if link_tag:
#                 # Extrair o texto do título
#                 edital_title = link_tag.text.strip()
                
#                 # Extrair o link do edital
#                 edital_link = link_tag['href']
                
#                 # Construir o link completo
#                 full_link = f"https://fapergs.rs.gov.br{edital_link}"
                
#                 # Exibir título e link
#                 print(f"Título: {edital_title}")
#                 print(f"Link: {full_link}\n")
#     else:
#         print(f"Erro ao acessar a página. Status code: {response.status_code}")

# # Chamar a função

# # get_fapesc_edital_titles_and_links()


# # def diagnose_fapergs_page():
# #     # URL da página
# #     url = "https://fapergs.rs.gov.br/abertos"
    
# #     # Fazer a requisição para o site
# #     response = requests.get(url)
    
# #     # Verificar se a requisição foi bem-sucedida
# #     if response.status_code == 200:
# #         print("Página acessada com sucesso.")
# #         # Processar o conteúdo HTML da página
# #         soup = BeautifulSoup(response.text, 'html.parser')
        
# #         # Imprimir o HTML formatado para verificar a estrutura
# #         print(soup.prettify())
# #     else:
# #         print(f"Erro ao acessar a página. Status code: {response.status_code}")

# # # Chamar a função para diagnóstico
# # diagnose_fapergs_page()
# def fapesc_extrair_titulos():
#     url = "https://fapergs.rs.gov.br/chamadas-e-editais/abertos"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Aqui tentamos encontrar os elementos que contêm os títulos
#         # Você pode precisar ajustar este seletor com base nos elementos que descobrir
#         titulos = soup.find_all('a', href=True)  # Altere conforme necessário

#         # Filtrando os títulos que você precisa
#         titulos_filtrados = [titulo.get_text(strip=True) for titulo in titulos if 'chamada' in titulo.get_text().lower()]

#         return titulos_filtrados
#     else:
#         return []

# # Testando a função
# # titulos = fapesc_extrair_titulos()
# # print(titulos)




# get_fapesc_edital_titles_and_links()



# import requests
# from bs4 import BeautifulSoup
# import psycopg2

# DB_CONFIG = {
#     "dbname": "postgres",
#     "user": "postgres.akerwwnultjhmvdixfmm",
#     "password": "senaccrawlerbr1234",
#     "host": "aws-0-sa-east-1.pooler.supabase.com",
#     "port": "6543",
# }

# def fapergs_edital_titles_and_links():
#     url = "https://fapergs.rs.gov.br/abertos/"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Encontra o contêiner que contém os editais
#         editais_container = soup.find("div", class_="panel-body")
#         if not editais_container:
#             print("Contêiner de editais não encontrado.")
#             return

#         # Busca por todos os itens de lista dentro do contêiner
#         editais_list = editais_container.find_all("li")

#         if not editais_list:
#             print("Nenhum edital encontrado na seção de Abertos.")
#             return

#         for item in editais_list:
#             link_tag = item.find("a")
#             if link_tag:
#                 edital_title = link_tag.text.strip()
#                 edital_link = link_tag.get('href')

#                 # Verificar se o link é relativo, caso seja, construir a URL completa
#                 if edital_link.startswith("/"):
#                     edital_link = "https://fapergs.rs.gov.br" + edital_link

#                 # Filtrar links relevantes
#                 if "resultado" in edital_title.lower() or "chamada" in edital_title.lower():
#                     print(f"Título: {edital_title}, Link: {edital_link}")
#                     # Inserir no banco de dados
#                     insert_into_database(edital_title, None, edital_link, None, None)

#     except Exception as e:
#         print(f"Erro ao acessar a página Fapergs: {e}")

# def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         nome_banca = "Fapergs"
#         valor = 0.0
#         prazo_execucao = None
#         valor_global = 0.0
#         valor_estimado = 0.0
#         valor_maximo = 0.0

#         insert_query = """
#             INSERT INTO edital (nome_banca, titulo, valor, descricao, link, 
#             id_site, img_logo, vencimento, prazo_execucao, valor_global, 
#             valor_estimado, valor_maximo, data_publicacao)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#         """
#         cursor.execute(insert_query, (nome_banca, titulo, valor, descricao, link,
#                                        None, None, vencimento, prazo_execucao,
#                                        valor_global, valor_estimado, valor_maximo, 
#                                        None))

#         conn.commit()
#         print("Dados inseridos com sucesso.")
    
#     except Exception as e:
#         print(f"Erro ao inserir dados no banco de dados: {e}")
    
#     finally:
#         cursor.close()
#         conn.close()

# fapergs_edital_titles_and_links()

























# import requests
# from bs4 import BeautifulSoup
# import psycopg2
# from datetime import datetime

# DB_CONFIG = {
#     "dbname": "postgres",
#     "user": "postgres.akerwwnultjhmvdixfmm",
#     "password": "senaccrawlerbr1234",
#     "host": "aws-0-sa-east-1.pooler.supabase.com",
#     "port": "6543",
# }

# def rnp_edital_titles_links_and_descriptions():
#     url = "https://www.rnp.br/inovacao/editais"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Localiza a seção "Editais abertos"
#         editais_abertos_section = soup.find('h3', string="Editais abertos")
        
#         if editais_abertos_section:
#             # Move para o próximo elemento (que contém os editais)
#             editais_list = editais_abertos_section.find_next('div')  # Ajuste conforme necessário

#             if editais_list:
#                 # Busca os títulos e links dentro da seção encontrada
#                 titles = editais_list.find_all("strong")

#                 if not titles:
#                     print("Nenhum título encontrado na seção de Editais Abertos.")
#                     return
                
#                 for title in titles:
#                     edital_title = title.text.strip()
#                     # Encontrar o link relacionado à tag <strong>
#                     edital_link = title.find_parent("a")["href"] if title.find_parent("a") else None
                    
#                     # Se não conseguir encontrar o link direto, busca na seção que envolve a tag <strong>
#                     if edital_link is None:
#                         link_parent = title.find_parent('div')  # Ajuste conforme necessário
#                         if link_parent:
#                             edital_link_tag = link_parent.find('a')
#                             if edital_link_tag:
#                                 edital_link = edital_link_tag['href']
                    
#                     # Agora, vamos obter a descrição do edital
#                     descricao = get_edital_description(editais_list, title)

#                     # Exibindo o título, link e descrição no console
#                     print(f"Título: {edital_title}, Link: {edital_link}, Descrição: {descricao}")
                    
#                     # Inserir no banco de dados (ainda que as outras informações sejam None por enquanto)
#                     insert_into_database(edital_title, descricao, edital_link, None, None)
#             else:
#                 print("Seção de editais não encontrada após 'Editais abertos'.")
#         else:
#             print("Seção 'Editais abertos' não encontrada.")
    
#     except requests.RequestException as e:
#         print(f"Erro ao acessar a página RNP: {e}")

# def get_edital_description(editais_list, title):
#     """Obtém a descrição do edital da lista de editais, procurando após o título."""
#     try:
#         # Procurar o próximo <p> após o título para obter a descrição
#         description_element = title.find_next('p')
#         if description_element:
#             return description_element.text.strip()
        
#         return "Descrição não encontrada."
    
#     except Exception as e:
#         print(f"Erro ao obter a descrição: {e}")
#         return "Erro ao acessar a descrição."

# def insert_into_database(titulo, descricao, link, data_publicacao, vencimento):
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         nome_banca = "RNP"
#         valor = 0.0
#         prazo_execucao = None
#         valor_global = 0.0
#         valor_estimado = 0.0
#         valor_maximo = 0.0

#         insert_query = """
#             INSERT INTO edital (nome_banca, titulo, valor, descricao, link, 
#             id_site, img_logo, vencimento, prazo_execucao, valor_global, 
#             valor_estimado, valor_maximo, data_publicacao)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
#         """
#         cursor.execute(insert_query, (nome_banca, titulo, valor, descricao, link,
#                                        None, None, vencimento, prazo_execucao,
#                                        valor_global, valor_estimado, valor_maximo, 
#                                        None))

#         conn.commit()
#         print("Dados inseridos com sucesso.")
    
#     except Exception as e:
#         print(f"Erro ao inserir dados no banco de dados: {e}")
    
#     finally:
#         cursor.close()
#         conn.close()

# # Chamada da função para obter títulos, links e descrições dos editais
# rnp_edital_titles_links_and_descriptions()
