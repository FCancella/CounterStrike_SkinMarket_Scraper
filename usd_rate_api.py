import requests
import json

def usd2brl():
    # Codigo da ExchangeRatesAPI foi copiado diretamente do site da API

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
    
    return usd_rate
    pass
