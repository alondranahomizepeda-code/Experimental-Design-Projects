import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("datos_experimento.csv")
df['Media_Grupo'] = df.groupby('Tratamiento')['Calidad_Luz'].transform('mean')
df['Residuo'] = df['Calidad_Luz'] - df['Media_Grupo']

grupos = [df['Calidad_Luz'][df['Tratamiento'] == nivel].dropna() for nivel in df['Tratamiento'].unique()]

stat_levene, p_levene = stats.levene(*grupos)
print(f"Prueba Levene - W: {stat_levene:.4f}, p: {p_levene:.6f}")

stat_shapiro, p_shapiro = stats.shapiro(df['Residuo'].dropna())
print(f"Prueba Shapiro - W: {stat_shapiro:.4f}, p: {p_shapiro:.6f}")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.regplot(x='Tratamiento', y='Calidad_Luz', data=df, ax=axes[0], scatter_kws={'alpha':0.6, 'color':'#2ca02c'}, line_kws={'color':'red'})
axes[0].set_title('A. Tendencia de Calidad de Luz vs Tratamiento')
axes[0].set_xlabel('Tratamiento (Lux)')
axes[0].set_ylabel('Calidad de Luz (%)')

sns.scatterplot(x='Media_Grupo', y='Residuo', data=df, ax=axes[1], alpha=0.7, color='#1f77b4', s=60)
axes[1].axhline(0, color='red', linestyle='--')
axes[1].set_title('B. Residuos vs Valores Predichos')
axes[1].set_xlabel('Valor Predicho')
axes[1].set_ylabel('Residuos')

stats.probplot(df['Residuo'].dropna(), dist="norm", plot=axes[2])
axes[2].set_title('C. Gráfico Q-Q de Normalidad')

plt.tight_layout()
plt.savefig('graficas_validacion.png', dpi=300)
print("¡Las 3 gráficas se han generado con éxito!")