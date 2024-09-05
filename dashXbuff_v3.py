from selenium import webdriver
import re
import pandas as pd
import locale
import requests
from bs4 import BeautifulSoup
import buff_price_scraper
import usd_rate_api

'''
Biblioteca/Arquivo auxiliar buff_price_scraper -

def get_skin_price(product_name, driver):
    Recebe o nome do produto no formato padrao da steam, e o driver aberto
    Monta o link a partir das condicoes desse nome,
    Retorna informacao de dash_price e qnt. de ofertas do item no BUFF163 (Global/Chines)

def get_price_from_page(product_link, driver):
    Recebe o link do produto,  e o driver aberto
    Entra na pagina do produto no site csgoskins.gg, onde é possivel coletar o dash_price do item no BUFF163.com sem precisar de API ou login
    Busca o dash_price do BUFF163 dentre diversos outros sites que o csgoskins.gg mostra
    Retorna preço e quantidade de ofertas do item



Biblioteca/Arquivo auxiliar usd_rate_api -

def usd_rate_api():
    Utiliza a ExchangeRatesAPI para retornar o preco do dolar USD (USDxBRL)
'''


# Definindo o local para o idioma e região como 'pt_BR'
locale.setlocale(locale.LC_ALL, 'pt_BR')

usd_rate = usd_rate_api.usd2brl()

# Ignora/Não mostra os erros no prompt. Exemplo: ...ERROR:device_event_log_impl...
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# Inicializando contador de item
cont_item = 0

skin_name = []
skin_dash_price = []
skin_buff_price = []
skin_buff_offers = []
skin_diff = []

#skin_dash_disc=[]
'''
Parei de pegar os descontos na dash pois muitas vezes nao estavam 100% corretos devido a um delay com os precos da steam.
Com isso passei a usar a biblioteca beatiful soup para realizar o scraping da dash, já que nao seria necessario carregar o javascript do site.
'''

df = pd.DataFrame(columns=['Name', 'Dash price', 'Buff price', 'Price diff', 'Buff offers'])

# Define as opções de exibição do pandas
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


# Define o número de páginas a serem percorridas e preco max. e min.
num_pages = 100
p_min = 10
p_max = 200

# Define a URL base para a página principal
# R$p_min até R$p_max, e 120 itens por página
#url_base = "https://dashskins.com.br/?search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_stattrak=&is_souvenir=&is_instant=&sort_by=&sort_dir=&limit=120&page={}&price_max="+ str(p_max) +"&price_min="+ str(p_min)

# Define a URL base para a página de ofertas
# R$p_min até R$p_max, e 120 itens por página
url_base = "https://dashskins.com.br/deals?min=&max=&search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_stattrak=&is_souvenir=&is_instant=&limit=120&page={}&price_max="+ str(p_max) +"&price_min="+ str(p_min)

# Cria um dicionário vazio para armazenar os produtos já visitados.
products = {}

# Cria uma lista vazia para armazenar os dicionários de produtos
products_list = [] 

# Loop para percorrer as páginas
for i in range(1, num_pages+1):
    url = url_base.format(i)
    print('')
    print(f'|{"-"*46}| PAGINA {i :0>2} |{"-"*46}|\n')

    # Faz a requisição HTTP para obter o conteúdo HTML da página
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontra todos os elementos <div> com a classe especificada, que contêm informações dos produtos
    prod_divs = soup.find_all('div', {'class': 'column is-2-fullhd is-3-widescreen is-4-desktop is-6-tablet is-12-mobile'})

    # Verifica se não há mais produtos, ou seja, se não há mais elementos <div> encontrados
    if not prod_divs:
        print("\nFim das páginas\n")
        break

    # Loop para processar cada produto encontrado
    for prod_div in prod_divs:
        # Extrai o link do produto e o nome do produto
        product_link = prod_div.select_one('a')['href']
        product_name = product_link.split("/item/")[1].split('/')[0].replace('-', ' ')

        # Extrai o preço do produto
        price_span = prod_div.select_one('.title.is-size-6.has-text-white-bis.has-text-centered > span')
        price_text = price_span.text.strip() if price_span.text.strip().startswith('R$') else 'R$ XXXX'
        dash_price = float(re.findall(r"\d+\.?\d*", (price_text.replace(".","")).replace(",", "."))[0])

        # Verifica se o produto já foi visitado anteriormente
        if product_name in products:
            # Se o preço atual for menor, atualiza o preço no dicionário de produtos e na lista de produtos
            if dash_price < products[product_name]:
                products[product_name] = dash_price
                for product in products_list:
                    if product['Name'] == product_name:
                        product['Dash price'] = locale.currency(dash_price, grouping=True, symbol='')
                        break
            else:
                continue

        # Adiciona o produto ao dicionário de produtos com o preço atualizado
        products[product_name] = dash_price

        # Obtém o preço e a quantidade de ofertas do produto na plataforma "Buff163"
        [buff_price, buff_offers] = buff_price_scraper.get_skin_price(product_name, driver)

        # Formata os valores para serem adicionados na lista e impressos
        buff_price = round(buff_price * usd_rate, 2)
        dash_price_str = locale.currency(dash_price, grouping=True, symbol='')
        buff_price_str = locale.currency(buff_price, grouping=True, symbol='')

        # Calcula a diferença percentual entre o preço na plataforma "Buff163" e o preço na plataforma "Dashskins"
        # Dash + x% = Buff
        diff = int((buff_price / dash_price - 1) * 100)

        # Realiza um reajuste de preço (-7%) caso o spread seja menor que -8, indicando que é um item para venda da plataforma "Buff163" para a plataforma "Dashskins".
        # Obs1.: -7% é a minha taxa de venda na Dashskins
        # Obs2.: -8%, já que com [0%,7%] a conta transformaria o número em porcentagem positiva
        # if diff < -8:
        diff = int((buff_price / (dash_price*0.93) - 1) * 100)

        # Verifica se o produto atende aos critérios estabelecidos para ser incluído na lista de skins
        # if (diff >= 10 and buff_offers >= 100) or (diff >= 5 and buff_offers >= 300) or (diff >= -5 and buff_offers >= 600) or (diff <= -20 and buff_offers >= 900 and product_name.split()[0] != "sticker" and product_name.split()[0] != "music"):

        #     # Verifica se a diferença percentual é igual a -100 (buff price = 0) e quebra, caso contrário, adiciona a diferença percentual formatada na lista
        #     if diff == -100:
        #         break
        #     elif isinstance(diff, int):
        #         skin_diff.append(f"{diff:.0f}%")
        #     else:
        #         skin_diff.append("ERRO")
                
            # Adiciona as informações restantes do produto às listas correspondentes
        skin_name.append(product_name)
        skin_dash_price.append(dash_price_str)
        skin_buff_price.append(buff_price_str)
        skin_buff_offers.append(buff_offers)

        # Adiciona uma nova linha ao dataframe com as informações do produto
        new_row = pd.DataFrame({'Name': [product_name],
                                'Dash price': [dash_price_str],
                                'Buff price': [buff_price_str],
                                'Price diff': [diff],
                                'Buff offers': [buff_offers]})

        df = pd.concat([df, new_row], ignore_index=True)

        resultado_str = f"R$ {dash_price_str} \tBUFF ${(buff_price/usd_rate):.2f} (R${buff_price_str})\t {buff_offers}\t   {diff}%  \t {product_name}" 
        print(resultado_str)

        cont_item += 1


print('\nItens lidos:', cont_item)

# Imprimindo o DataFrame com todos os dados ordenado por 'diff'
df_sorted = df.sort_values(by=['Price diff'], ascending=False).reset_index(drop=True)
print(df_sorted)
