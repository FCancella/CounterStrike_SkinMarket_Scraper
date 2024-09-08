import requests

def cny_brl_rate():
    # Define the API URL for exchange rates
    api_url = "https://open.er-api.com/v6/latest/CNY"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Raise an exception for bad responses
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Extract the exchange rate for BRL
        brl_rate = data.get("rates", {}).get("BRL")

        if brl_rate is not None:
            print("cny/brl =", brl_rate)
        else:
            # Exchange rate not found in the response
            print("Exchange rate not found in the API response")
            brl_rate = input("Enter the exchange rate from Chinese Yuan (CNY) to Brazilian Real (BRL) manually: ")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        brl_rate = input("Enter the exchange rate from Chinese Yuan (CNY) to Brazilian Real (BRL) manually: ")

    return brl_rate