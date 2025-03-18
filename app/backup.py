#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Módulo para operaciones de copia y respaldo
"""

import os
import subprocess

def copiar_archivo_manual(origen, destino):
    """Copia un archivo de forma manual con verificación"""
    # Asegurar que el directorio destino existe
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    
    # Copiar el archivo
    with open(origen, 'rb') as fsrc:
        contenido = fsrc.read()
        with open(destino, 'wb') as fdst:
            fdst.write(contenido)
    
    # Verificar que el tamaño coincide
    if os.path.getsize(origen) != os.path.getsize(destino):
        raise Exception(f"Error de verificación en la copia de {origen}")

def copiar_con_robocopy(origen, destino, elementos_seleccionados, opciones_adicionales=""):
    """
    Copia archivos usando robocopy.
    
    Args:
        origen: Ruta de origen
        destino: Ruta de destino
        elementos_seleccionados: Lista de elementos a copiar
        opciones_adicionales: Opciones adicionales para robocopy
        
    Returns:
        Tupla de (exito, codigo_salida, log, error_msg)
    """
    try:
        # Crear archivo de inclusión para los elementos seleccionados
        archivo_inclusion = "elementos_seleccionados.txt"
        with open(archivo_inclusion, "w", encoding="utf-8") as f:
            for elemento in elementos_seleccionados:
                # Para robocopy, usar formato con barras invertidas
                elemento_formateado = elemento.replace("/", "\\")
                f.write(f"{elemento_formateado}\n")
        
        # Opciones base
        opciones = f"/E {opciones_adicionales}"
        
        # Comando Robocopy
        comando = f'robocopy "{origen}" "{destino}" {opciones} /XA:SH /XD "$RECYCLE.BIN" "System Volume Information" /IF @{archivo_inclusion}'
        
        # Ejecutar Robocopy
        proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
        
        # Capturar la salida en logs
        output_log = []
        
        for linea in proceso.stdout:
            output_log.append(linea.strip())
        
        # Esperar a que termine el proceso y obtener el código de salida
        codigo_salida = proceso.wait()
        
        # Verificar si hubo errores graves según el código de salida de robocopy
        # Los códigos de robocopy son diferentes: 0=sin cambios, 1=ok, >7=errores
        if codigo_salida >= 8:
            error_output = "\n".join(output_log[-10:]) if output_log else "Error desconocido"
            return (False, codigo_salida, output_log, f"Error en robocopy (código {codigo_salida}): {error_output}")
        
        # Robocopy se ejecutó correctamente
        return (True, codigo_salida, output_log, None)
    
    except Exception as e:
        return (False, -1, [], str(e))

def copiar_archivos_manualmente(origen, destino, elementos_seleccionados, callback_progreso=None):
    """
    Realiza la copia de archivos manualmente sin usar robocopy
    
    Args:
        origen: Ruta de origen
        destino: Ruta de destino
        elementos_seleccionados: Lista de elementos a copiar
        callback_progreso: Función para reportar progreso (recibe índice, total, ruta)
        
    Returns:
        Lista de elementos copiados en formato (ruta, tipo, tamaño)
    """
    elementos_copiados = []
    total_elementos = len(elementos_seleccionados)
    
    for idx, ruta in enumerate(elementos_seleccionados):
        ruta_origen_completa = os.path.join(origen, ruta)
        ruta_destino_completa = os.path.join(destino, ruta)
        
        # Reportar progreso si se proporciona callback
        if callback_progreso:
            callback_progreso(idx, total_elementos, ruta)
        
        try:
            if os.path.isdir(ruta_origen_completa):
                # Es un directorio
                if not os.path.exists(ruta_destino_completa):
                    os.makedirs(ruta_destino_completa, exist_ok=True)
                elementos_copiados.append((ruta, '[CARPETA]', 0))
            elif os.path.isfile(ruta_origen_completa):
                # Es un archivo
                tamano = os.path.getsize(ruta_origen_completa)
                copiar_archivo_manual(ruta_origen_completa, ruta_destino_completa)
                elementos_copiados.append((ruta, '[ARCHIVO]', tamano))
        except Exception as e:
            print(f"Error al copiar {ruta}: {e}")
    
    return elementos_copiados