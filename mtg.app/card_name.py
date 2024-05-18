import pandas as pd

cards = [
    "Mutavault"
]

collection_df = pd.read_csv('mtg.collection.csv')
data_df  = pd.read_csv('mtg.data.csv')
comprar_df = pd.DataFrame(columns=['Card', 'Quantity', 'Formato'])

for card in cards:
    if card in data_df['Card'].values:
        played = data_df.loc[data_df['Card'] == card, 'Played'].values[0]
        formato = data_df.loc[data_df['Card'] == card, 'Formato'].values[0]
        if card in collection_df['Card'].values:
            quantity = collection_df.loc[collection_df['Card'] == card, 'Quantity'].values[0] 
            if played > quantity:
                comprar_df = comprar_df._append({'Card': card, 'Quantity': played - quantity, 'Formato': formato}, ignore_index=True)
        else:
            comprar_df = comprar_df._append({'Card': card, 'Quantity': played, 'Formato': formato}, ignore_index=True)


print("Cartas a comprar:")
if comprar_df.empty:
    print("[]")
else:
    print(comprar_df.to_string(index=False, header=False))