import time
import re
import pandas as pd

# Modules
from tools.cny2brl import cny_brl_rate
from tools.buff_skins_id import load_id_dict
from tools.auxiliary import get_max_page, loading_bar

import requests
import sys
import concurrent.futures
from bs4 import BeautifulSoup

# Change the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Call the function to get the Yuan to Brazilian Real exchange rate
yuan_brl_rate = cny_brl_rate()
print("* CNY/BRL rate successfully updated!")

# Deals page (or Main ordenated by discount)
price_min = 500
price_max = 1500
base_url = f"https://dashskins.com.br/deals?min=&max=&search=&item_type=&rarity=&itemset=&exterior=&weapon=&has_sticker=&has_stattrak=&is_souvenir=&is_instant=&limit=120&page={'{}'}&price_min={price_min}&price_max={price_max}"

page_limit = 500

max_page = get_max_page(base_url)


if (page_limit > max_page):
    page_limit = max_page


# Define the Buff ID dictionary (skin_name: buff_id)
id_dict = load_id_dict()
'''
id_dict = {
'skin_1': id1,
'skin_2': id2,
'skin_3': id3,
}
'''
print("* Buff ID dictionary successfully loaded")

# Receive a skin's name and return its price and the number of offers on Buff
def get_skin_data(product_name):
    # Get the item's Buff ID by searching the dictionary.
    item_id = id_dict.get(product_name)

    buff_api_url = f"https://buff.163.com/api/market/goods/sell_order?game=csgo&page_num=1&goods_id={item_id}"

    while True:
        try:
            # Send a GET request to the API
            response = requests.get(buff_api_url)
            response.raise_for_status()  # Raise an exception for bad responses (non-2xx status codes)

            # Parse the JSON response
            data = response.json()

            # Extract the "items" list
            items_list = data.get("data", {}).get("items", [])

            if items_list:
                # If the list is not empty, extract the "price" value from the first item
                buff_price = items_list[0].get("price")
                buff_price = float(buff_price) * yuan_brl_rate
                buff_offers = data.get("data", {}).get("total_count", 0)
                break  # Exit the loop if successful
            else:
                #print(f"'{product_name}' price information not found in the response")
                buff_price = 0
                buff_offers = 0
                break

        except requests.RequestException as e:
            None
            #warning(f"An error occurred: {str(e)}\n{product_name} fetch failed...")

        # Sleep before retrying
        time.sleep(0.2)

    buff_price = round(buff_price, 2)

    return [buff_price, buff_offers]




# Dict to store checked skins and their prices (prevent scraping the same item multiple times)
products = {}
'''
products = {
'skin_1': price_1,
'skin_2': price_2,
'skin_3': price_3,
}
'''

item_counter = 0

print("\nScraping all DASHSKINS items")

# Iterate over each page of Dash Skins
for page_num in range(1, page_limit+1):

    url = base_url.format(page_num)

    # Make the HTTP request and get the content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <div> elements with the specified class
        div_tags = soup.find_all('div', class_='column is-2-fullhd is-3-widescreen is-4-desktop is-6-tablet is-12-mobile')

        if not div_tags:
            break

        # Loop through the found <div> elements and extract the desired information
        for div_tag in div_tags:

            item_counter+=1

            # Get the href attribute from the first <a> element
            a_tag = div_tag.find('a')
            if a_tag:
                href = a_tag.get('href')
                href_name = (href.split('/'))[2]
            
            name = href_name.replace("-", " ")
         
            # Get the text from the <span> element within the <div> with class "title ..."
            title_div = div_tag.find('div', class_='title is-size-6 has-text-white-bis has-text-centered')
            if title_div:
                span_text = (title_div.find_all('span'))[-1].text

            # Remove "." (thousands separator in the pt-BR format)
            # Replace "," with "." ("," represents decimal places in the pt-BR format)
            price = float(re.findall(r"\d+\.?\d*", (span_text.replace(".","")).replace(",", "."))[0]) # e.g.: R$1.234,56 -> 1234.56

            #print(f"{item_counter:4} | {name} - {price}")
            loading_bar(item_counter, (int(page_limit-0.5))*120)

            # Skip if item is a case key (not available on buff)
            if "case key" in name:
                continue
            
            # Check if the item qualifies for the items list
            if name in products and price >= products[name]:
                    # Skip this item as it's more expensive than the one already seen
                    continue
            
            # Add/Update the item on the dictionary of viewed items
            products[name] = price



print()


item_counter = 0

linha = []

total_items = len(products.keys())

print("\nScraping and analysing selected (+1000, no repeat) items")

# Define a function to process a single product
def process_product(product_name):
    global item_counter

    formated_product_name = product_name.replace(" ","")

    dash_price = products[product_name]

    # Get the price and offers for the product on the 'Buff163' platform
    [buff_price, buff_offers] = get_skin_data(formated_product_name)

    # Percentage difference between Buff163 and DashSkins (Dash + % = Buff)
    diff = int((buff_price / dash_price - 1) * 100)

    # Adjust dash's price if the spread is lower than -10%, indicating that it's an item for sale from 'Buff163' to 'Dashskins'.
    # Note1: -7% -> my selling fee on Dashskins.
    # Note2: -3% -> margin to sell even cheaper.
    # Note3: < -10% is being used because with [-10%, 0%], the calculation would turn the number into a positive percentage.
    if diff < -10:
        diff = int((buff_price / (dash_price*0.90) - 1) * 100)  
    elif  -10 <= diff and diff <= 0:
        diff = 0 # this item ain't relevant
    
    #print(f"{'R$'+str(dash_price):9} | BUFF {('R$' + str(buff_price)):^12} | {diff:3}% | {buff_offers:2} | \t{product_name}")
    item_counter+=1
    loading_bar(item_counter, total_items)

    # item_30d_sold_qnt > 1000 and
    if (buff_offers >= 91 and diff > 5 and \
        "sticker" not in product_name) or \
        (buff_offers >= 91 and diff < -8 and \
        "souvenir" not in product_name and \
        "sticker" not in product_name and \
        "pp bizon" not in product_name and \
        "p90" not in product_name and \
        "mag 7" not in product_name and \
        "tec 9" not in product_name and \
        "sg 553" not in product_name and \
        "xm1014" not in product_name):

        # Adiciona uma nova linha ao dataframe com as informações do produto
        linha.append([product_name, dash_price, buff_price, diff, buff_offers])


# Create a ThreadPoolExecutor with 2 concurrent threads ( More than 2 usually equals API errors)
with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
    # Use the executor to process products concurrently
    results = list(executor.map(process_product, products.keys()))

print("\n\nITEMS\n\n")

# Sort the list based on the "diff" field (4th element in each sublist)
sorted_linha = sorted(linha, key=lambda x: x[3], reverse=True)

# Create a DataFrame from the sorted list
df = pd.DataFrame(sorted_linha, columns=["Product Name", "Dash Price", "Buff Price", "Diff", "Buff Offers"])

# Save the DataFrame as a CSV file
df.to_csv("skins.csv", index=False)

# Print the DataFrame (optional)
print(df)