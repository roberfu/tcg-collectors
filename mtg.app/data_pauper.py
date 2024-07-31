import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import math

df = pd.DataFrame(columns=['Card', 'Played', 'Formato'])

urls = [
    ("https://www.mtggoldfish.com/format-staples/pauper/full/creatures", "Pauper"),
    ("https://www.mtggoldfish.com/format-staples/pauper/full/spells", "Pauper"),
    ("https://www.mtggoldfish.com/format-staples/pauper/full/lands", "Pauper")
]

for url, formato in urls:
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    segunda_columna = []
    ultima_columna = []

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) >= 2:
            segunda_columna.append(''.join(re.findall(r'\w+', cells[1].text.strip())))
            ultima_columna.append(math.ceil(float(cells[-1].text.strip())))

    df_temp = pd.DataFrame({'Card': segunda_columna, 'Played': ultima_columna, 'Formato': [formato] * len(segunda_columna)})

    for index, row in df_temp.iterrows():
        card = row['Card']
        played = row['Played']
        formato_temp = row['Formato']

        if card in df['Card'].values:
            if played > df.loc[df['Card'] == card, 'Played'].values[0]:
                df.loc[(df['Card'] == card), 'Played'] = played
        else:
            df = pd.concat([df, pd.DataFrame({'Card': [card], 'Played': [played], 'Formato': [formato_temp]})], ignore_index=True)

    print(f"Agregado {url}")

df.to_csv('mtg.data.pauper.csv', index=False)