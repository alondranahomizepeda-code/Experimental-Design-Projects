# Lector OCR Inteligente y Análisis Estadístico

Un sistema avanzado para procesar fotografías de tickets de compra y extraer su información utilizando **Azure OpenAI (GPT-4o)** y **OpenCV**. Además, incluye un módulo completo de análisis estadístico para evaluar el rendimiento y la confianza de las lecturas.

## 📋 Requisitos Previos

1. **Python 3**: Asegúrate de tener Python instalado.
2. **Credenciales de Azure OpenAI**: Necesitas un archivo `.env` en la raíz del proyecto con tus credenciales:
   ```env
   AZURE_OPENAI_ENDPOINT=tu_endpoint
   AZURE_OPENAI_API_KEY=tu_api_key
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-02-01
   ```

## 🛠️ Instalación y Configuración

El proyecto ya cuenta con una estructura limpia y un único entorno virtual que contiene todas las dependencias necesarias.

1. **Activar el entorno virtual:**
   ```powershell
   # Abre la terminal en la carpeta principal del proyecto (LectorOCR) y ejecuta:
   .\venv\Scripts\activate
   ```
2. **Instalar dependencias (si es tu primera vez en otra computadora):**
   ```powershell
   pip install -r requirements.txt
   ```

## 🚀 Uso del Sistema OCR

Para procesar una imagen y extraer el texto estructurado en formato JSON, ejecuta el archivo principal indicando la ruta de la imagen fotográfica:

```powershell
python main.py IMG\121.2\ticket2_1.jpeg
```
*Los resultados (el JSON final) se guardarán automáticamente en la carpeta `Resultados/` conservando la misma estructura de la imagen original.*

## 📊 Módulo de Análisis Estadístico (Diseño de Experimentos)

El sistema incluye scripts específicos para analizar el nivel de "Confianza de Lectura" y validar mediante el diseño de experimentos si existen diferencias significativas entre distintas calidades o tratamientos de las imágenes.

Para usar esta parte del programa, ejecuta los scripts en el siguiente orden:

1. **Extraer y recopilar datos:**
   ```powershell
   python extraer_datos.py
   ```
   *Recorre todos los archivos JSON de los resultados, extrae los niveles de confianza de lectura detectados por la IA y genera un archivo consolidado llamado `datos_experimento.csv`.*

2. **Validar Supuestos Estadísticos:**
   ```powershell
   python validacion_supuestos.py
   ```
   *Genera las gráficas de normalidad y homocedasticidad (`graficas_validacion.png`) para asegurar matemáticamente que la prueba ANOVA que se aplicará después sea válida.*

3. **Prueba de Hipótesis y ANOVA:**
   ```powershell
   python analisis_anova.py
   ```
   *Realiza la prueba estadística (ANOVA de un factor) para determinar si el factor/tratamiento de la imagen afecta la precisión del OCR, indicando si se rechaza o no la hipótesis nula, y genera una gráfica visual (`grafica_resultados.png`).*

---
📄 *Para más detalles técnicos sobre el funcionamiento interno de la Inteligencia Artificial y OpenCV, consulta el archivo [DOCUMENTACION.md](DOCUMENTACION.md).*
