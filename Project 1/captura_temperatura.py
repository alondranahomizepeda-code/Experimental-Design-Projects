# =================================================================
# MATERIA: Diseño Experimental
# INTEGRANTES DEL EQUIPO:
# - Altamirano Reyes Diana Mayte
# - Laureano Martínez Fabiola
# - Zepeda Juárez Alondra Nahomi
# PROYECTO: Sistema de Adquisición de Temperatura (Práctica 1)
# PROFESOR: Dr. Javier Salas García
# =================================================================

import serial
import time
import csv
import numpy as np

# Configuraciones principales
PUERTO_COM = 'COM6'  # Modificar según el puerto asignado por Windows
VELOCIDAD = 9600
TOTAL_MUESTRAS = 10

def registrar_fase(nombre_etapa):
    print(f"\n[+] Preparando lectura para: {nombre_etapa}")
    registro_temporal = []
    
    try:
        # Establecemos conexión con el ESP32
        conexion = serial.Serial(PUERTO_COM, VELOCIDAD, timeout=2)
        time.sleep(2.5) # Tiempo de espera para sincronizar
        conexion.reset_input_buffer()
        
        print(f"Escuchando {PUERTO_COM} (1 muestra por segundo aprox.)...")
        
        while len(registro_temporal) < TOTAL_MUESTRAS:
            if conexion.in_waiting > 0:
                # Decodificación robusta para evitar errores de caracteres extraños
                lectura_cruda = conexion.readline().decode('utf-8', errors='ignore').strip()
                try:
                    valor_temp = float(lectura_cruda)
                    registro_temporal.append(valor_temp)
                    print(f" -> {nombre_etapa} | Dato {len(registro_temporal)}/{TOTAL_MUESTRAS}: {valor_temp} °C")
                except ValueError:
                    continue # Ignora líneas que no sean números
                    
        conexion.close() 
        
    except serial.SerialException:
        print(f"\n[!] Error crítico: No se puede acceder a {PUERTO_COM}.")
        print("Asegúrate de que el ESP32 esté conectado y el Monitor Serie de Arduino esté cerrado.")
        return None
        
    # Procesamiento estadístico (Rigor del Dr. Salas)
    promedio = np.mean(registro_temporal)
    var_muestral = np.var(registro_temporal, ddof=1) # ddof=1 para varianza muestral (n-1)
    
    print(f"\n>>> RESUMEN {nombre_etapa.upper()} <<<")
    print(f"Media: {promedio:.2f} °C | Varianza: {var_muestral:.4f}")
    
    return registro_temporal

if __name__ == '__main__':
    print("===============================================")
    print("   SISTEMA DE ADQUISICIÓN DE TEMPERATURA")
    print("        INGENIERÍA EN IA - UAEMEX")
    print("===============================================")
    
    # Ejecución de las 3 fases experimentales
    input("\n[ Acción ]: Coloca el termopar en AGUA FRÍA y presiona ENTER...")
    fase1_fria = registrar_fase("Agua Fría")
    
    if fase1_fria:
        input("\n[ Acción ]: Mueve el termopar a AGUA TIBIA y presiona ENTER...")
        fase2_tibia = registrar_fase("Agua Tibia")
        
    if fase1_fria and fase2_tibia:
        input("\n[ Acción ]: Mueve el termopar a AGUA CALIENTE y presiona ENTER...")
        fase3_caliente = registrar_fase("Agua Caliente")
    
    # Generación del archivo CSV unificado
    if fase1_fria and fase2_tibia and fase3_caliente:
        archivo_salida = "resultados_variacion_equipo.csv"
        
        with open(archivo_salida, mode='w', newline='', encoding='utf-8') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(['Muestra', 'Temp_Fria_C', 'Temp_Tibia_C', 'Temp_Caliente_C'])
            
            for idx in range(TOTAL_MUESTRAS):
                writer.writerow([idx + 1, fase1_fria[idx], fase2_tibia[idx], fase3_caliente[idx]])
                
        print(f"\n[ ÉXITO ] Archivo '{archivo_salida}' generado para el reporte.")
    else:
        print("\n[ ERROR ] No se completaron todas las fases. No se generó el CSV.")