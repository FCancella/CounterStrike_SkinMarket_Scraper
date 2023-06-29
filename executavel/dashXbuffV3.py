

"""

História:
Este código foi desenvolvido com o objetivo de identificar as melhores oportunidades de negociação de skins no mercado de CS:GO,
aproveitando a diferença de preços entre a plataforma brasileira Dash Skins e o mercado global representado pelo serviço Buff.163.

No mercado nacional de skins de CS:GO, embora seja significativo, a oferta de produtos e os preços baixos são limitados quando
comparados ao mercado global. Atualmente, a Dash Skins é o único site brasileiro que permite aos usuários anunciar seus itens por
qualquer preço desejado, oferecendo um ambiente de "livre mercado". Por outro lado, o Buff.163 é reconhecido como o maior mercado
global de skins, especialmente aquecido no mercado chinês. No entanto, o Buff aceita apenas pagamentos nacionais chineses,
impossibilitando transações diretas de usuários estrangeiros.

Diante desse cenário, surgiu a ideia de adquirir skins na Dash Skins e vendê-las no Buff para aproveitar as vantagens oferecidas por
um mercado global. Durante essa operação, notei que alguns itens na Dash Skins estavam com preços mais baixos em relação ao Buff.
A fimde explorar esse "spread", e identificar as melhores ofertas, comeceio desenvolvimento deste código em conjunto com o ChatGPT.

A escolha de utilizar o ChatGPT para desenvolver este projeto teve dois propósitos: avaliar sua eficiência na colaboração com um ser
humano e testar a viabilidade de programar utilizando bibliotecas com aa quais eu não possuía conhecimento prévio.

Com base em conhecimentos em HTML, CSS e Python, consegui criar toda a lógica necessária para realizar o web scraping dos dados,
evitando erros e bloqueios durante o processo. O ChatGPT desempenhou um papel fundamental no projeto, uma vez que sem ele qualquer
um seria incapaz de aprender o suficiente de BeautifulSoup e selenium a fim realizar este projeto. Em vários momentos, a IA foi capaz
de fornecer soluções para problemas encontrados, como a necessidade de suporte para JavaScript, que foi resolvida com a transição para
o Selenium.

Com todos os aspectos discutidos e as dúvidas esclarecidas, foi possível programar em conjunto com o ChatGPT um modelo extremamente
útil para a finalidade deste projeto.


Lógica e Especificações:
Para coletar os dados dos produtos na Dash Skins, utilizei a biblioteca BeautifulSoup. Através da análise do HTML da página, é possível
extrair informações como nome e preço dos itens anunciados.

Em seguida, procuro o preço desses mesmos produtos no Buff.163, e como a plataforma não permite acesso direto a usuários não logados,
contornei essa restrição utilizando o site csgoskins.gg, que fornece informações sobre preços de itens anunciados no Buff.

Com todos os dados coletados, aplico filtros com base em parâmetros como o valor do spread e número de ofertas, armazenando as informações
em um DataFrame e exibindo-as no terminal.

Uso e Contribuições:
    1. Clone o repositório e instale as dependências necessárias.
    2. Execute o código alterando os parametros, se necessario.
        Preco Min./Max. de busca (linhas 122, 123)
        Numero de paginas (linha 134)
        Filtros das ofertas (linhas 308)
    3. Analise os resultados exibidos no terminal, que mostrarão as melhores oportunidades de negociação encontradas (Compra e Venda). 


Aprimoramentos, sugestões e contribuições são bem-vindos!


"""



from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd
import locale
import requests
import json
from bs4 import BeautifulSoup

# Codigo da ExchangeRatesAPI foi copiado diretamente do site da API
# Definindo o local para o idioma e região como 'pt_BR'
locale.setlocale(locale.LC_ALL, 'pt_BR')

# Usando ExchangeRatesAPI para obter a conversão Real/Dólar com requests e json
url = "https://api.apilayer.com/exchangerates_data/convert?to=brl&from=usd&amount=1"

payload = {}
headers = {
  "apikey": "hctbuPG2ZZKWLzOldnP6khjGqDXgiY4k"
}

# Fazendo uma solicitação GET à API para obter a taxa de câmbio
response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:
    # Converte a string JSON em um objeto Python
    data = json.loads(response.text)
    
    # Atribui o valor de "result" a "usd_rate"
    usd_rate = data["result"]
    
    # Imprime o valor de "usd_rate"
    print("USD-BRL:", usd_rate)
else:
    print("Erro ao obter a taxa de câmbio")

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




# Solicitando o preço mínimo do usuário
p_min = input("Enter the minimum price: ")

# Verificando se o input é um número
try:
    p_min = float(p_min)
except ValueError:
    print("Invalid input. The minimum price will be set to 10.")
    p_min = 10

# Solicitando o preço máximo do usuário
p_max = input("Enter the maximum price: ")

# Verificando se o input é um número
try:
    p_max = float(p_max)
except ValueError:
    print("Invalid input. The maximum price will be set to 200.")
    p_max = 200

# Exibindo os valores finais
print("\nMinimum price:", p_min)
print("Maximum price:", p_max)




# Define a URL base para a página principal com os filtros de preço e quantidade de itens por página
# R$p_min até R$p_max, e 120 itens por página
#url_base = "https://dashskins.com.br/?search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_stattrak=&is_souvenir=&is_instant=&sort_by=&sort_dir=&limit=120&page={}&price_max="+ str(p_max) +"&price_min="+ str(p_min)

# Define a URL base para a página de ofertas com os filtros de preço e quantidade de itens por página
# R$p_min até R$p_max, e 120 itens por página
url_base = "https://dashskins.com.br/deals?min=&max=&search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_stattrak=&is_souvenir=&is_instant=&limit=120&page={}&price_max="+ str(p_max) +"&price_min="+ str(p_min)

# Define o número de páginas a serem percorridas
num_pages = 50



'''
Recebe o nome do produto no formato padrao da steam,
Monta o link a partir das condicoes desse nome,
Retorna informacao de dash_price e qnt. de ofertas do item no BUFF163 (Global/Chines)
'''
def get_skin_price(product_name):

    # Inicializa as variáveis de preço e ofertas
    price = 0
    offers = 0

    # Separa o nome e a condição do produto
    name_parts = product_name.split()

    # skins stattrack e souvenir
    if name_parts[0].lower() == 'stattrak' or name_parts[0].lower() == 'souvenir':
        # Adiciona 'souvenir'/'stattrak' antes das duas últimas palavras
        name_parts[-2:-1] = [f'{name_parts[0].lower()}-{name_parts[-2]}']
        # Remove 'souvenir'/'stattrak' do começo da lista
        name_parts.pop(0)
        name = '-'.join(name_parts[:-2]).lower()
        condition = '-'.join(name_parts[-2:]).lower()
    
    # skins normais
    elif name_parts[-1].lower() == 'new' or name_parts[-1].lower() == 'wear' or name_parts[-1].lower() == 'tested' or name_parts[-1].lower() == 'worn' or name_parts[-1].lower() == 'scarred':
        name = '-'.join(name_parts[:-2]).lower()
        condition = '-'.join(name_parts[-2:]).lower()

    # agentes, stickers, caixas, etc
    else:
        name = '-'.join(name_parts).lower()
        condition = ''

    # Cria o link com o nome e a condição do produto
    product_link = f"https://csgoskins.gg/items/{name}/{condition}"

    # Busca o preço na página do produto
    [price, offers] = get_price_from_page(product_link)

    return [price, offers]




'''
Recebe o link do produto,
Entra na pagina do produto no site csgoskins.gg, onde é possivel coletar o dash_price do item no BUFF163.com sem precisar de API ou login
Busca o dash_price do BUFF163 dentre diversos outros sites que o csgoskins.gg mostra
Retorna preço e quantidade de ofertas do item
'''
def get_price_from_page(product_link):
    # Navega para a URL desejada
    driver.get(product_link)

    price = 0
    offers = 0

    try:
        # Encontra todas as divs com a classe desejada
        prod_divs = driver.find_elements(By.CSS_SELECTOR, "div[class='bg-gray-800 rounded shadow-md relative flex items-center flex-wrap my-4 ']")

        # Verifica cada div encontrada e procura aquela que armazena o bloco com as infos. do produto no BUFF163
        for prod_div in prod_divs:

            # Verifica se a div contém um elemento <a> com a classe desejada
            prod_a = prod_div.find_element(By.CSS_SELECTOR, 'a.hover\\:underline')

            # Se encontrar a div com link do BUFF163, salva o preço e a quantidade de ofertas
            if 'BUFF163' in prod_div.text and prod_a.get_attribute('href') == 'https://csgoskins.gg/markets/buff163':
                # Encontra o span com o preço dentro da div
                price_span = prod_div.find_element(By.CSS_SELECTOR, 'span.font-bold.text-xl')

                # Pega o texto do span (o preço)
                price_text = price_span.text

                # Remove o símbolo de dólar e converte o preço para float
                price = float(price_text.replace('$', ''))


                # Encontra o span com o número de ofertas dentro da div
                offers_span = prod_div.find_element(By.CSS_SELECTOR, 'span[class=""]')

                # Pega o texto do span (a quantidade de ofertas)
                offers_text = offers_span.text

                # Converte a quantidade de ofertas para inteiro
                offers = int(offers_text)

                # Sai do loop ao encontrar as infos. desejadas
                break
    except:
        # Se nao, dash_price e offers = 0
        price = 0
        offers = 0

    return [price, offers]




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
        [buff_price, buff_offers] = get_skin_price(product_name)

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
        if diff < -8:
            diff = int((buff_price / (dash_price*0.93) - 1) * 100)

        # Verifica se o produto atende aos critérios estabelecidos para ser incluído na lista de skins
        if (diff >= 10 and buff_offers >= 100) or (diff >= 5 and buff_offers >= 300) or (diff >= -5 and buff_offers >= 600) or (diff <= -20 and buff_offers >= 900 and product_name.split()[0] != "sticker" and product_name.split()[0] != "music"):

            # Verifica se a diferença percentual é igual a -100 (buff price = 0) e quebra, caso contrário, adiciona a diferença percentual formatada na lista
            if diff == -100:
                break
            elif isinstance(diff, int):
                skin_diff.append(f"{diff:.0f}%")
            else:
                skin_diff.append("ERRO")
                
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

input("\n\nPress Enter to exit...")
