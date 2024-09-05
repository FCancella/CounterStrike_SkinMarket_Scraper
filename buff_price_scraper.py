from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



'''
Recebe o nome do produto no formato padrao da steam, e o driver aberto
Monta o link a partir das condicoes desse nome,
Retorna informacao de dash_price e qnt. de ofertas do item no BUFF163 (Global/Chines)
'''
def get_skin_price(product_name, driver):

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
    [price, offers] = get_price_from_page(product_link, driver)

    return [price, offers]
    pass


'''
Recebe o link do produto, e o driver aberto
Entra na pagina do produto no site csgoskins.gg, onde é possivel coletar o dash_price do item no BUFF163.com sem precisar de API ou login
Busca o dash_price do BUFF163 dentre diversos outros sites que o csgoskins.gg mostra
Retorna preço e quantidade de ofertas do item
'''
def get_price_from_page(product_link, driver):
    wait = WebDriverWait(driver, 5)
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
                price_span = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span.font-bold.text-lg.sm\\:text-xl')))

                # Pega o texto do span (o preço)
                price_text = price_span.text
                

                # Remove o símbolo de dólar e converte o preço para float
                price = float(price_text.replace('$', ''))


                # Encontra o span com o número de ofertas dentro da div
                offers_span = wait.until(EC.visibility_of_element_located((By.XPATH, './/div[@class="w-full"][2]/span')))
                

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
    pass
