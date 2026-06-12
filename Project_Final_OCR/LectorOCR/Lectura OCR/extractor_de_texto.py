import os
import cv2
import json
import base64
from openai import AzureOpenAI

def extraer_texto(imagen_preprocesada):
    """
    Usa Azure OpenAI GPT-4o con Visión para extraer 
    y estructurar la información de un ticket de compra de Garis.
    """
    punto_conexion = os.getenv("AZURE_OPENAI_ENDPOINT")
    clave_api = os.getenv("AZURE_OPENAI_API_KEY")
    nombre_implementacion = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o")
    version_api = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not punto_conexion or not clave_api:
        raise ValueError("Faltan las credenciales de Azure en tu archivo .env.")

    cliente = AzureOpenAI(
        azure_endpoint=punto_conexion,
        api_key=clave_api,
        api_version=version_api
    )

    # Convertir la imagen de OpenCV (numpy array) a bytes (PNG)
    exito, bufer = cv2.imencode('.png', imagen_preprocesada)
    if not exito:
        raise ValueError("Error al codificar la imagen a PNG.")
    
    # Convertir a base64 para GPT-4o
    imagen_base64 = base64.b64encode(bufer).decode('utf-8')

    # Definir el prompt estructurado
    prompt_sistema = """
    Eres un asistente experto en contabilidad y OCR. Tu tarea es extraer la información de los tickets de la tienda "Garis".
    Existen tickets grandes y pequeños, pero para ambos debes extraer exactamente la misma información.
    
    Adicionalmente, debes autocalificar la calidad de tu lectura de la imagen en un rango de 0 a 100, mas la calidad de la luz igual en un rango de 0 a 100. Sé totalmente honesto: si la imagen está borrosa, cortada, oscura o hay datos que tuviste que adivinar, baja la calificación proporcionalmente y explica brevemente por qué en el campo "Notas_Confianza". Si se lee perfectamente, asigna 100.
    
    Extrae los siguientes datos y responde estrictamente en formato JSON válido, sin ningún texto adicional, sin bloques de código ```json, solo el JSON puro.
    Estructura requerida:
    {
        "Nombre_Tienda": "...",
        "Productos_Comprados": [
            {"Descripcion": "...", "Precio": "..."}
        ],
        "Total_a_Pagar": "...",
        "Monto_Pagado": "...",
        "Cambio": "...",
        "Confianza_Lectura": 100,
        "Calidad_Luz": 100,
        "Notas_Confianza": "..."    
    }
    
    Si algún dato no existe en el ticket o no es legible, pon "No detectado".
    Asegúrate de incluir todos los productos que logres identificar.
    """

    # Llamar al modelo de Azure OpenAI (Vision)
    respuesta = cliente.chat.completions.create(
        model=nombre_implementacion,
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Extrae la información de este ticket de Garis usando la estructura solicitada."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{imagen_base64}"
                        }
                    }
                ]
            }
        ],
        temperature=0.0
    )

    # Extraer el contenido del JSON
    texto_resultado = respuesta.choices[0].message.content.strip()
    
    # Limpiar el resultado por si el modelo incluye ```json
    if texto_resultado.startswith("```json"):
        texto_resultado = texto_resultado[7:]
    if texto_resultado.endswith("```"):
        texto_resultado = texto_resultado[:-3]
        
    try:
        # Validar y formatear el JSON
        json_parseado = json.loads(texto_resultado)
        return json.dumps(json_parseado, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        # En caso de que no haya devuelto un JSON válido, retornamos la respuesta cruda
        return texto_resultado
