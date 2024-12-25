from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')  #Abre navegador em segundo plano
driver = webdriver.Chrome(options=chrome_options)  

# Acesse o Mercado Livre
driver.get("https://www.mercadolivre.com.br")

# Pedir ao usuário o termo de busca
termo_busca = input("Digite o que você quer pesquisar: ").strip()

# Localizar o campo de busca e inserir o termo
busca = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[@class="nav-search-input"]'))
)
busca.clear()  # Limpa o campo de busca
busca.send_keys(termo_busca)  # Digita o termo fornecido pelo usuário
busca.send_keys(Keys.RETURN)  # Pressiona Enter para buscar

# Aguarde os resultados carregarem dinamicamente
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//li[contains(@class, "ui-search-layout__item")]'))
)

# Coletar os produtos listados
produtos = driver.find_elements(By.XPATH, '//li[contains(@class, "ui-search-layout__item")]')

# Criar um arquivo CSV para salvar os resultados
with open('mercado_livre_precos.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Título", "Preço", "Link"])

    for produto in produtos:
        try:
            # Usando os XPath fornecidos
            titulo = produto.find_element(By.XPATH, './/h2[@class="poly-box poly-component__title"]').text
            preco = produto.find_element(By.XPATH, './/span[@class="andes-money-amount__fraction"]').text
            link = produto.find_element(By.XPATH, './/a').get_attribute('href')

            # Escrever no arquivo CSV
            writer.writerow([titulo, preco, link])
        except Exception as e:
            print(f"Erro ao coletar dados de um produto: {e}")

# Finalizar o WebDriver
driver.quit()

print("Arquivo CSV criado com sucesso!")
