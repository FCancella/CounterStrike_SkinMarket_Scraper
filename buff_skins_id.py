import html
import re
import requests

def clear_item_name(name):
    # Decode HTML entities, replace single quotes, and remove non-alphanumeric characters
    cleared_name = re.sub(r'[^a-zA-Z0-9]', '', html.unescape(name.replace("'", ""))).lower().replace("27","") # Work around for "Case Key" and "Capsule Key", since buff doesn't sell it
    return cleared_name

def load_id_dict():
    # URL of the text file containing the ids
    url = "https://raw.githubusercontent.com/ModestSerhat/cs2-marketplace-ids/main/cs2_marketplaceids.json"

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (non-2xx status codes)

        # Parse the response content
        return parse_response(response.json()['items'])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading items id dictonary: {e}")

def parse_response(content):
    id_dict = {}
    for item in content:
        try:
            item_buff_id = content[item]['buff163_goods_id']
        except:
            None
        try:
            item_youpin_id = content[item]['youpin_id']
        except:
            item_youpin_id = None
        item_name = item
        cleaned_key = clear_item_name(item_name)
        id_dict[cleaned_key] = int(item_buff_id)

    return id_dict
