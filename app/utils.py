#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Funciones utilitarias para la aplicación
"""

import os
import datetime

def obtener_metadatos(ruta):
    """Obtiene metadatos de un archivo o carpeta (tamaño y fecha de modificación)."""
    if not os.path.exists(ruta):
        return None
    return (os.path.getsize(ruta) if os.path.isfile(ruta) else 0, os.path.getmtime(ruta))

def convertir_tamano(bytes):
    """Convierte el tamaño de bytes a MB, GB o TB según corresponda."""
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unidad}"
        bytes /= 1024

def comparar_origen_destino(origen, destino, elementos_seleccionados=None):
    """Compara carpetas entre origen y destino y devuelve las que son nuevas o diferentes."""
    elementos_a_copiar = []

    for elemento in elementos_seleccionados:
        ruta_origen = os.path.join(origen, elemento)
        ruta_destino = os.path.join(destino, elemento)

        # Verificar si es una carpeta
        if os.path.isdir(ruta_origen):
            if not os.path.exists(ruta_destino):
                elementos_a_copiar.append((elemento, '[CARPETA]', 0))
            else:
                # Para carpetas, comparamos el contenido total
                tamano_origen = calcular_tamano_carpeta(ruta_origen)
                tamano_destino = calcular_tamano_carpeta(ruta_destino)
                
                if tamano_origen != tamano_destino:
                    elementos_a_copiar.append((elemento, '[CARPETA]', tamano_origen))
                    
    return elementos_a_copiar

def calcular_tamano_carpeta(ruta):
    """Calcula el tamaño total de una carpeta incluyendo todos sus archivos."""
    tamano_total = 0
    for dirpath, dirnames, filenames in os.walk(ruta):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                tamano_total += os.path.getsize(fp)
            except OSError:
                pass  # Ignorar archivos a los que no se puede acceder
    return tamano_total

def obtener_arbol_con_tamanos_nivel_2(base_path):
    """Genera un árbol de archivos con el tamaño total de cada carpeta hasta el nivel 2."""
    arbol = {}
    for root, dirs, files in os.walk(base_path):
        # Calcular el nivel de la carpeta
        nivel = root[len(base_path):].count(os.sep)
        if nivel > 2:  # Solo tomar hasta el nivel 2
            continue
        try:
            total_size = sum(os.path.getsize(os.path.join(root, f)) for f in files if os.path.exists(os.path.join(root, f)))
            arbol[root] = total_size
        except Exception as e:
            print(f"Error al calcular tamaño de {root}: {e}")
            arbol[root] = 0
    return arbol