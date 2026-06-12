# Documentación Técnica: Lector OCR Inteligente para Tickets (Garis)

## 1. Descripción General del Proyecto
Este proyecto es un sistema automatizado diseñado para procesar fotografías de tickets de compra, extraer su información contable (tienda, productos, precios, totales) de manera inteligente, y guardar los resultados en un formato de datos estructurado (JSON). El sistema está optimizado para procesar datos de forma masiva y clasificar los resultados automáticamente replicando la estructura de carpetas de origen.

---

## 2. Herramientas y Tecnologías Utilizadas

* **Python:** Lenguaje de programación principal del proyecto.
* **OpenCV (`cv2`) y Numpy:** Librerías utilizadas para la visión por computadora clásica. Se encargan de "ver" la imagen, detectar dónde están los bordes del ticket, aplicar cálculos matemáticos y recortar el fondo sobrante de la foto.
* **Azure OpenAI (Modelo GPT-4o con Visión):** Es el "cerebro" del proyecto. Un modelo fundacional multimodal masivo capaz de leer y razonar sobre imágenes a todo color.
* **Base64:** Estándar de codificación utilizado para transformar la imagen fotográfica en una cadena de texto para poder enviarla de forma segura por internet a los servidores de Microsoft.
* **JSON:** Formato de texto ligero utilizado para estructurar los datos finales (nombre de la tienda, listas, números) para que puedan ser fácilmente leídos por bases de datos o sistemas contables.
* **Dotenv:** Herramienta de seguridad que permite cargar variables de entorno (como la Clave de API de Azure) desde un archivo `.env` para que no queden expuestas directamente en el código fuente.

---

## 3. Flujo de Ejecución (Paso a Paso)

El flujo de trabajo inicia cuando ejecutas el archivo principal (`main.py`) pasándole la ruta de una fotografía. Esto es lo que ocurre internamente:

### Paso 1: Recepción de la Imagen (`main.py`)
El script principal captura la ruta del archivo (ej. `IMG/18.96/ticket1.jpeg`), verifica que el archivo realmente exista y prepara el entorno.

### Paso 2: Escáner Inteligente (`recorte_imagen.py`)
Antes de enviarle la foto a la Inteligencia Artificial, el código optimiza la imagen mediante algoritmos de visión artificial:
1. **Detección de bordes:** Convierte temporalmente una copia de la imagen a blanco y negro y usa el algoritmo de `Canny` para buscar líneas rectas.
2. **Cálculo de contornos:** Busca formas geométricas de 4 lados (un rectángulo) que ocupen más del 70% de la foto. Si encuentra el ticket, calcula su perspectiva.
3. **Recorte (Warp Perspective):** Toma la imagen a color original y la "endereza" o recorta, eliminando el fondo (como la mesa donde estaba el ticket). Esto permite que la IA se enfoque 100% en el papel.
4. **Redimensión:** Si la foto tiene una calidad exageradamente alta (más de 3000 pixeles), la comprime proporcionalmente para evitar saturar la memoria y enviar un archivo demasiado pesado a internet.

### Paso 3: Comunicación y Extracción (`extractor_de_texto.py`)
La imagen recortada y a todo color es enviada al motor de extracción:
1. Toma la imagen y la encripta en código Base64.
2. Arma el **Prompt de Sistema**: Una instrucción estricta en lenguaje natural donde le dice a GPT-4o su rol (experto en contabilidad) y la estructura JSON exacta que debe devolver.
3. El motor llama a la API de Microsoft Azure OpenAI, pasándole tanto la instrucción como la imagen, y se queda esperando la respuesta.

### Paso 4: Autoevaluación de la IA
Durante la lectura en los servidores de Azure, GPT-4o analiza los píxeles de la imagen. Basado en las instrucciones que le dimos, extrae los productos y los precios. Además, hace un análisis de **Autoevaluación**: revisa qué tan borrosa estaba la foto, si hubo sombras que dificultaron la lectura, y se asigna una calificación de `Confianza_Lectura` de 0 a 100, justificando su calificación.

### Paso 5: Almacenamiento Estructurado (`main.py`)
1. El `extractor_de_texto.py` recibe el texto JSON puro de Azure y lo entrega al `main.py`.
2. El programa analiza la ruta original de la foto para saber a qué carpeta pertenecía (ej. `18.96`).
3. Crea un directorio espejo dentro de la carpeta global `Resultados/` (ej. `Resultados/18.96/`).
4. Genera un archivo con el prefijo `resultado_` (ej. `resultado_ticket1.json`) y guarda ahí todo el texto de forma permanente.

---

## 4. Ventajas de la Arquitectura Actual
* **Uso de imágenes a color:** A diferencia de los OCR tradicionales que requieren convertir el documento a blanco y negro absoluto (destruyendo el antialiasing y contexto visual), esta arquitectura le envía a GPT-4o la imagen natural, mejorando drásticamente la capacidad de la IA de leer textos muy pequeños, mal iluminados o borrosos.
* **Tolerancia a fallos:** Al tener una autoevaluación, un humano puede filtrar más adelante los JSON buscando aquellos que tengan una `Confianza_Lectura` menor a 80 y auditar únicamente esos tickets, ahorrando miles de horas de trabajo manual.
