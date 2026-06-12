import os
import json
import pandas as pd

ruta_resultados = "Resultados"
datos_extraidos = []

for carpeta in os.listdir(ruta_resultados):
    ruta_carpeta = os.path.join(ruta_resultados, carpeta)
    if os.path.isdir(ruta_carpeta):
        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith('.json'):
                ruta_archivo = os.path.join(ruta_carpeta, archivo)
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    try:
                        # Intentamos leer el JSON
                        contenido = json.load(f)
                        calidad = contenido.get("Calidad_Luz", None) 
                        datos_extraidos.append({
                            "Tratamiento": float(carpeta),
                            "Archivo_Ticket": archivo,
                            "Calidad_Luz": calidad
                        })
                    except json.JSONDecodeError:
                        # Si el archivo está roto, la terminal te avisa pero NO se detiene
                        print(f"⚠️ Omitiendo archivo malformado por la IA: {archivo} (en Lux: {carpeta})")

df = pd.DataFrame(datos_extraidos)
df.to_csv("datos_experimento.csv", index=False)

print("\n========================================")
print(" ¡EXTRACCIÓN TERMINADA! ")
print(f" Tickets procesados exitosamente: {len(df)}")
print(" Archivo 'datos_experimento.csv' creado.")
print("========================================\n")