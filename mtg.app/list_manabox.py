import re
import math
import pandas as pd

with open('mtg.list_manabox.txt', 'r', encoding='utf-8') as file:
    cartas = file.readlines()

cards = {}
comprar_df = pd.DataFrame(columns=['Card', 'Quantity'])
no_comprar_df = pd.DataFrame(columns=['Card'])

for carta in cartas:
    if not carta.startswith('Deck'):
        cantidad, nombre = carta.split(' ', 1)
        nombre_limpio = ''.join(re.findall(r'\w+', nombre))
        if nombre_limpio in cards:
            cards[nombre_limpio] += int(cantidad)
        else:
            cards[nombre_limpio] = int(cantidad)

collection_df = pd.read_csv('mtg.collection.csv')
data_df  = pd.read_csv('mtg.data.csv')

for card in cards:
    if card in data_df['Card'].values:
        played = data_df.loc[data_df['Card'] == card, 'Played'].values[0]
        formato = data_df.loc[data_df['Card'] == card, 'Formato'].values[0]
        if card in collection_df['Card'].values:
            quantity = collection_df.loc[collection_df['Card'] == card, 'Quantity'].values[0] 
            if played >= quantity:
                comprar_df = comprar_df._append({'Card': card, 'Quantity': played - quantity}, ignore_index=True)
        else:
            comprar_df = comprar_df._append({'Card': card, 'Quantity': played}, ignore_index=True)

print("Cartas a comprar:")
if comprar_df.empty:
    print("[]")
else:
    print(comprar_df.to_string(index=False, header=False))