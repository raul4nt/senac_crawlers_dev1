from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

API_URL = "https://senac-crawlers.onrender.com/api/editais/"  # Ajuste para o endpoint correto

def fapergs_edital_titles_and_links():
    # Configurações do Chrome para rodar em modo headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ativa o modo headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Inicia o driver do Chrome com as opções
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "https://fapergs.rs.gov.br/abertos/"
    
    try:
        driver.get(url)

        # Aguarda o carregamento da página e busca pelos títulos de editais
        wait = WebDriverWait(driver, 10)  # Aguardar até 10 segundos
        editais_list = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2.conteudo-lista__item__titulo a"))
        )

        if not editais_list:
            print("Nenhum edital encontrado na seção de Abertos.")
            return

        for link_tag in editais_list:
            edital_title = link_tag.text.strip()
            edital_link = link_tag.get_attribute('href')

            # Verifica se o link é relativo e constrói a URL completa, se necessário
            if edital_link.startswith("/"):
                edital_link = "https://fapergs.rs.gov.br" + edital_link

            print(f"Título: {edital_title}, Link: {edital_link}")

            # Inserir na API
            insert_into_api(edital_title, None, edital_link, None, None)

    except Exception as e:
        print(f"Erro ao acessar a página Fapergs: {e}")

    finally:
        driver.quit()

def insert_into_api(titulo, descricao, link, data_publicacao, vencimento):
    payload = {
        "nome_banca": "Fapergs",
        "titulo": titulo,
        "valor": 0.0,
        "descricao": descricao,
        "link": link,
        "img_logo": None,
        "vencimento": vencimento,
        "prazo_execucao": None,
        "valor_global": 0.0,
        "valor_estimado": 0.0,
        "valor_maximo": 0.0,
        "data_publicacao": None  # Ajuste se você tiver essa informação
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        print("Dados inseridos na API com sucesso.")
    except requests.RequestException as e:
        print(f"Erro ao inserir dados na API: {e}")

# Chamada da função para obter títulos e links dos editais
fapergs_edital_titles_and_links()



# O uso do Selenium neste site se faz necessário porque o conteúdo dos editais é carregado dinamicamente via 
# JavaScript após o carregamento inicial da página. 
# O BeautifulSoup, por outro lado, apenas analisa o HTML que é enviado inicialmente pelo servidor, e não 
# consegue acessar o conteúdo que é gerado por scripts em JavaScript. 
# Portanto, para acessar e extrair os editais que aparecem apenas após a execução de JavaScript, é 
# essencial utilizar o Selenium, que simula a interação com o navegador e permite que esses conteúdos sejam carregados e acessados.
