import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Receive the main page link, and return the amount of pages
options = webdriver.ChromeOptions()
options.add_argument("--blink-settings=imagesEnabled=false") # Disable images
options.add_argument("--disable-features=CSSStyleSheet") # Disable CSS styles
options.add_argument('--headless') # Run in headless mode (without a graphical user interface)
options.add_argument("--disable-logging")  # Disable logging for DevTools
driver = webdriver.Chrome(options=options)

def get_max_page(url):

    url = url.format(1)

    driver.get(url)

    # Page numbers are <a> with class="pagination-link"
    pages = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".pagination-link ")))

    highest_page = -1
    
    if pages:
        # Iterate through the found elements
        for new_page in pages:
            # Convert the element text to a numeric value
            new_page = int(new_page.text)
            # Check if the current value is higher than the highest value found so far
            if new_page > highest_page:
                highest_page = new_page
    
    if highest_page < 0:
        highest_page = 999

    driver.quit()

    return highest_page

def loading_bar(current_value, max_value, length=50):
    progress = (current_value / max_value)
    max_value = max(current_value, max_value)
    progress = min (progress, 1) # Cap progress at 100% if current value exceeds it
    arrow = '|' * int(round(progress * length))
    spaces = ' ' * (length - len(arrow))
    sys.stdout.write(f'\r[{arrow}{spaces}] {int(progress * 100):4}%  - {current_value:5} /{max_value} items')
    sys.stdout.flush()