import pandas as pd
import re

data = pd.read_csv('mtg.data.csv')
collection = pd.read_csv('mtg.collection.csv')

collection['Name'] = collection['Name'].apply(lambda x: ''.join(re.findall(r'\w+', x)))

cartas_data = dict(zip(data['Card'], data['Played']))

comprar_df = pd.DataFrame(columns=['Card', 'Quantity'])
vender_df = pd.DataFrame(columns=['Card', 'Quantity'])

for index, row in collection.iterrows():
    card = row['Name']
    quantity = row['Quantity']

    if card in cartas_data:
        played = cartas_data[card]
        if quantity > played:
            vender_df = vender_df._append({'Card': card, 'Quantity': quantity - played}, ignore_index=True)
        elif quantity != played:
            comprar_df = comprar_df._append({'Card': card, 'Quantity': played - quantity}, ignore_index=True)
    else:
        vender_df = vender_df._append({'Card': card, 'Quantity': quantity }, ignore_index=True)

df_resultante = collection.sort_values('Name')
df_resultante.to_csv('mtg.collection.csv', index=False)

print("Cartas a comprar:")
if comprar_df.empty:
    print("[]")
else:
    print(comprar_df.to_string(index=False, header=False))
print("Cartas a vender:")
if vender_df.empty:
    print("[]")
else:
    print(vender_df.to_string(index=False, header=False))