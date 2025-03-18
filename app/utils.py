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
    """Compara archivos y carpetas entre origen y destino y devuelve los que son nuevos o diferentes."""
    elementos_a_copiar = []

    for root, dirs, files in os.walk(origen):
        ruta_relativa = os.path.relpath(root, origen)
        destino_actual = os.path.join(destino, ruta_relativa)

        # Verificar si esta carpeta está en la lista de seleccionados
        if elementos_seleccionados and ruta_relativa != "." and ruta_relativa not in elementos_seleccionados:
            # Verificar si alguna subcarpeta o archivo está seleccionado
            es_padre_de_seleccionado = False
            for elem in elementos_seleccionados:
                if elem.startswith(ruta_relativa + os.sep):
                    es_padre_de_seleccionado = True
                    break
            
            if not es_padre_de_seleccionado:
                continue  # Saltar esta carpeta si no está seleccionada

        if not os.path.exists(destino_actual):
            elementos_a_copiar.append((ruta_relativa, '[CARPETA]', 0))

        for file in files:
            archivo_relativo = os.path.join(ruta_relativa, file)
            if elementos_seleccionados and archivo_relativo not in elementos_seleccionados:
                continue  # Saltar este archivo si no está seleccionado
                
            ruta_origen = os.path.join(root, file)
            ruta_destino = os.path.join(destino_actual, file)

            meta_origen = obtener_metadatos(ruta_origen)
            meta_destino = obtener_metadatos(ruta_destino)

            if meta_destino is None or meta_origen != meta_destino:
                elementos_a_copiar.append((archivo_relativo, '[ARCHIVO]', meta_origen[0]))

    return elementos_a_copiar

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