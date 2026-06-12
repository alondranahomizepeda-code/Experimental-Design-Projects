import os
import sys

# Agregamos las carpetas al sistema para poder importar los módulos
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIRECTORIO_BASE, "Tratamiento de imagen"))
sys.path.append(os.path.join(DIRECTORIO_BASE, "Lectura OCR"))

from recorte_imagen import detectar_y_recortar_documento, redimensionar_imagen
from extractor_de_texto import extraer_texto
from dotenv import load_dotenv

import argparse
import cv2

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def principal():
    # Configurar la lectura del parámetro desde la terminal
    analizador_argumentos = argparse.ArgumentParser(description="Lector OCR para imágenes")
    analizador_argumentos.add_argument("ruta_imagen", help="Ruta de la imagen a procesar. Ejemplo: IMG/ejemplo.jpg")
    argumentos = analizador_argumentos.parse_args()
    
    ruta_imagen = argumentos.ruta_imagen
    
    if not os.path.exists(ruta_imagen):
        print(f"Error: No se encontró la imagen en {ruta_imagen}")
        print("Por favor, verifica que la ruta esté bien escrita o que el archivo exista.")
        return

    print(f"--- Procesando imagen: {ruta_imagen} ---")
    
    try:
        # Paso 1: Escáner Inteligente (Detectar ticket y recortar)
        print("1. Buscando el documento en la imagen...")
        imagen_escaneada = detectar_y_recortar_documento(ruta_imagen)
        
        # Redimensionar para tamaño óptimo de OCR
        imagen_escaneada = redimensionar_imagen(imagen_escaneada)
        
        # Guardar la imagen recortada para verificación visual
        ruta_depuracion = os.path.join("Resultados", "scanned_debug.jpg")
        cv2.imwrite(ruta_depuracion, imagen_escaneada)
        print(f"   (Imagen escaneada guardada en {ruta_depuracion} para que puedas verla)")

        # Paso 2: Lectura y estructuración con IA (Azure OpenAI)
        print("2. Extrayendo y estructurando texto con Azure OpenAI...")
        # Nota: GPT-4o Vision lee MEJOR las imágenes a color originales que las binarizadas.
        texto_estructurado = extraer_texto(imagen_escaneada)
        
        print("\n--- Resultados Finales (Estructura IA) ---")
        print(texto_estructurado)
        
        # Paso 3: Guardar el JSON en la carpeta correspondiente
        nombre_carpeta_origen = os.path.basename(os.path.dirname(ruta_imagen))
        
        # Si la imagen estaba suelta o directamente en IMG, la metemos a una carpeta "General"
        if not nombre_carpeta_origen or nombre_carpeta_origen.upper() == "IMG":
            nombre_carpeta_origen = "General"
            
        nombre_archivo_origen = os.path.splitext(os.path.basename(ruta_imagen))[0]
        
        # Crear la ruta: Resultados/18.96/
        carpeta_destino = os.path.join("Resultados", nombre_carpeta_origen)
        os.makedirs(carpeta_destino, exist_ok=True)
        
        # Crear el nombre del archivo: resultado_ticket1_1.json
        ruta_json_salida = os.path.join(carpeta_destino, f"resultado_{nombre_archivo_origen}.json")
        
        # Escribir el archivo
        with open(ruta_json_salida, 'w', encoding='utf-8') as archivo_json:
            archivo_json.write(texto_estructurado)
            
        print(f"\n[ÉXITO] El JSON se ha guardado correctamente en: {ruta_json_salida}")
            
    except Exception as e:
        print(f"Ocurrió un error procesando la imagen: {e}")

if __name__ == "__main__":
    principal()
