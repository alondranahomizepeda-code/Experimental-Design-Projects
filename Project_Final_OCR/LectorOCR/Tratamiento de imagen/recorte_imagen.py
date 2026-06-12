import cv2
import numpy as np

def ordenar_puntos(puntos):
    # Ordenar puntos: superior-izquierdo, superior-derecho, inferior-derecho, inferior-izquierdo
    rectangulo = np.zeros((4, 2), dtype="float32")
    suma = puntos.sum(axis=1)
    rectangulo[0] = puntos[np.argmin(suma)]
    rectangulo[2] = puntos[np.argmax(suma)]
    diferencia = np.diff(puntos, axis=1)
    rectangulo[1] = puntos[np.argmin(diferencia)]
    rectangulo[3] = puntos[np.argmax(diferencia)]
    return rectangulo

def transformacion_cuatro_puntos(imagen, puntos):
    rectangulo = ordenar_puntos(puntos)
    (sup_izq, sup_der, inf_der, inf_izq) = rectangulo

    # Calcular anchura máxima
    anchura_A = np.sqrt(((inf_der[0] - inf_izq[0]) ** 2) + ((inf_der[1] - inf_izq[1]) ** 2))
    anchura_B = np.sqrt(((sup_der[0] - sup_izq[0]) ** 2) + ((sup_der[1] - sup_izq[1]) ** 2))
    anchura_maxima = max(int(anchura_A), int(anchura_B))

    # Calcular altura máxima
    altura_A = np.sqrt(((sup_der[0] - inf_der[0]) ** 2) + ((sup_der[1] - inf_der[1]) ** 2))
    altura_B = np.sqrt(((sup_izq[0] - inf_izq[0]) ** 2) + ((sup_izq[1] - inf_izq[1]) ** 2))
    altura_maxima = max(int(altura_A), int(altura_B))

    # Construir vista plana ("pájaro")
    destino = np.array([
        [0, 0],
        [anchura_maxima - 1, 0],
        [anchura_maxima - 1, altura_maxima - 1],
        [0, altura_maxima - 1]], dtype="float32")

    matriz = cv2.getPerspectiveTransform(rectangulo, destino)
    recorte = cv2.warpPerspective(imagen, matriz, (anchura_maxima, altura_maxima))
    return recorte

def detectar_y_recortar_documento(ruta_imagen):
    # 1. Cargar imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise ValueError(f"No se pudo cargar la imagen: {ruta_imagen}")
        
    original = imagen.copy()
    proporcion = imagen.shape[0] / 500.0 # Operar en una imagen pequeña mejora la detección
    
    anchura = int(imagen.shape[1] * (500.0 / imagen.shape[0]))
    redimensionada = cv2.resize(imagen, (anchura, 500), interpolation=cv2.INTER_AREA)

    # 2. Detección de bordes
    grises = cv2.cvtColor(redimensionada, cv2.COLOR_BGR2GRAY)
    grises = cv2.GaussianBlur(grises, (5, 5), 0)
    bordes = cv2.Canny(grises, 75, 200)

    # 3. Buscar contornos
    contornos, _ = cv2.findContours(bordes.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:5]
    contorno_documento = None
    
    # Calcular el 70% del área de la imagen redimensionada
    area_redimensionada = redimensionada.shape[0] * redimensionada.shape[1]
    area_minima = 0.70 * area_redimensionada
    
    for c in contornos:
        # Si el área del contorno es menor al 70%, lo ignoramos
        if cv2.contourArea(c) < area_minima:
            continue
            
        perimetro = cv2.arcLength(c, True)
        aproximacion = cv2.approxPolyDP(c, 0.02 * perimetro, True)
        # Si tiene 4 vértices, es el documento
        if len(aproximacion) == 4:
            contorno_documento = aproximacion
            break

    # 4. Aplicar transformación o mantener original
    if contorno_documento is not None:
        print("Documento detectado exitosamente (área > 70%). Aplicando recorte.")
        recorte_final = transformacion_cuatro_puntos(original, contorno_documento.reshape(4, 2) * proporcion)
    else:
        print("El contorno detectado es menor al 70% de la imagen. Manteniendo la imagen original completa.")
        recorte_final = original

    return recorte_final

def redimensionar_imagen(imagen):
    # Limpiamos los cambios anteriores y solo dejamos una protección básica:
    # Si la imagen por alguna razón supera los 3000px, la reducimos proporcionalmente.
    # De lo contrario (como en tu imagen de 787x1600), se quedará intacta.
    altura, anchura = imagen.shape[:2]
    dimension_maxima = 3000
    
    if altura > dimension_maxima or anchura > dimension_maxima:
        escala = dimension_maxima / max(altura, anchura)
        nueva_anchura = int(anchura * escala)
        nueva_altura = int(altura * escala)
        imagen = cv2.resize(imagen, (nueva_anchura, nueva_altura), interpolation=cv2.INTER_AREA)
        
    return imagen
