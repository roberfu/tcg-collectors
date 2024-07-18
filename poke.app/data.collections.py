import pandas as pd

df = pd.read_csv('poke.data.csv')

df_valor_1 = df[df['Value'] == 1]
df_valor_superior_1 = df[df['Value'] > 1]

df_valor_1.to_csv('poke.collecion.csv', index=False, header=False)

df_valor_superior_1.to_csv('poke.collection.ps.csv', index=False, header=False)