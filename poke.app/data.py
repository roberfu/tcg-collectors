from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import math
import re
from collections import OrderedDict

driver = webdriver.Chrome()

url = "https://pokemoncard.io/top/"

driver.get(url)

time.sleep(5)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

card_list = soup.find('div', id='cardList')

resultados = OrderedDict()

if card_list:
    for card in card_list.find_all('div', recursive=False):
        card_name = card.find(class_='card-name-grid')
        badge = card.find(class_='badge custom-badge mt-1')
        if card_name and badge:

            name = re.sub(r'\([^)]*\)', '', card_name.text.strip()).strip()
            badge_text = badge.text.strip()
            
            name = re.sub(r'\([^)]*\)', '', name)
            name = re.sub(r'[^\w\s-]', '', name) 
            name = re.sub(r'\s+', ' ', name)

            avg_value = float(badge_text.split('Avg.')[-1].strip())
            
            if name in resultados:
                if avg_value > resultados[name]:
                    resultados[name] = math.ceil(avg_value)
            else:
                resultados[name] = math.ceil(avg_value)

driver.quit()

df = pd.DataFrame.from_dict(resultados, orient='index').reset_index()
df.columns = ['Name', 'Value']

print(df)

df.to_csv('poke.data.csv', index=False, header=False)