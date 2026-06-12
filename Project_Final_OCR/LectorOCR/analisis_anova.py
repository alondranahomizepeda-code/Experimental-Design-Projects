import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("datos_experimento.csv")
grupos = [df['Calidad_Luz'][df['Tratamiento'] == nivel].dropna() for nivel in df['Tratamiento'].unique()]

f_stat, p_valor = stats.f_oneway(*grupos)

print("\n========================================")
print(" RESULTADOS DEL ANOVA DE UN FACTOR")
print("========================================")
print(f"Estadístico F : {f_stat:.4f}")
print(f"Valor p       : {p_valor:.6f}")
print("========================================\n")

plt.figure(figsize=(10, 6))
sns.boxplot(x='Tratamiento', y='Calidad_Luz', data=df, palette='Set2')
plt.title('Efecto de la Iluminación en la Calidad de Luz (OCR)')
plt.xlabel('Tratamiento (Niveles de Iluminación en Lux)')
plt.ylabel('Calidad de Luz Detectada (%)')
plt.grid(True, linestyle='--', alpha=0.7)

plt.savefig('grafica_resultados.png', dpi=300)
print("¡Gráfica guardada como 'grafica_resultados.png'!")