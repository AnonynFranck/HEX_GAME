import pandas as pd
import matplotlib.pyplot as plt

data = [
    [1510940.9090909092, 47580.95238095238],
    [1271004.081632653, 153051.02040816325],
    [1880223.8095238095, 150380.0],
    [3550102.1739130435, 78024.44444444444],
    [1547660.8695652173, 45790.90909090909]
]

df = pd.DataFrame(data, columns=['Rojo (ns)', 'Azul (ns)'])

df_filtered = df[df['Azul (ns)'] > 0]

df_filtered['Rojo (ms)'] = df_filtered['Rojo (ns)'] / 1e6
df_filtered['Azul (ms)'] = df_filtered['Azul (ns)'] / 1e6

df_filtered = df_filtered.round({'Rojo (ms)': 3, 'Azul (ms)': 3})

table = df_filtered[['Rojo (ms)', 'Azul (ms)']].to_markdown(index=False)

print("Tabla de tiempos de ejecución:")
print(table)

plt.figure(figsize=(10, 6))
bar_width = 0.35
index = range(len(df_filtered))

plt.bar(index, df_filtered['Rojo (ms)'], bar_width, label='Rojo', color='red', alpha=0.7)
plt.bar([i + bar_width for i in index], df_filtered['Azul (ms)'], bar_width, label='Azul', color='blue', alpha=0.7)

plt.xlabel('Muestra')
plt.ylabel('Tiempo de ejecución (ms)')
plt.title('Comparación de tiempos de ejecución entre jugadores Rojo y Azul')
plt.legend()

plt.xticks([i + bar_width/2 for i in index], [f'Muestra {i+1}' for i in index])

for i, v in enumerate(df_filtered['Rojo (ms)']):
    plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')
for i, v in enumerate(df_filtered['Azul (ms)']):
    plt.text(i + bar_width, v, f'{v:.1f}', ha='center', va='bottom')

plt.tight_layout()
plt.show()