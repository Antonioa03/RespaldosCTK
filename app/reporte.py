#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Módulo para generación de informes
"""

import os
import datetime
from app.utils import convertir_tamano, obtener_arbol_con_tamanos_nivel_2

def generar_reporte_html(origen, destino, archivos_copiados, tamaño_destino_antes=0, tamaño_destino_despues=0, tamaño_diferencia=0):
    """
    Genera un informe HTML con los archivos copiados y estadísticas de tamaño.
    
    Args:
        origen: Ruta de origen
        destino: Ruta de destino
        archivos_copiados: Lista de archivos copiados en formato (ruta, tipo, tamaño)
        tamaño_destino_antes: Tamaño del directorio destino antes de la copia
        tamaño_destino_despues: Tamaño del directorio destino después de la copia
        tamaño_diferencia: Diferencia de tamaño (después - antes)
    
    Returns:
        Ruta al archivo HTML generado
    """
    # Obtener información de la estructura del origen y destino
    arbol_origen = obtener_arbol_con_tamanos_nivel_2(origen)
    arbol_destino = obtener_arbol_con_tamanos_nivel_2(destino)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Obtener solo el nombre del directorio de origen (sin la ruta completa)
    nombre_carpeta_origen = os.path.basename(origen)
    
    # Calcular estadísticas del respaldo
    total_archivos = sum(1 for _, tipo, _ in archivos_copiados if tipo == '[ARCHIVO]')
    total_carpetas = sum(1 for _, tipo, _ in archivos_copiados if tipo == '[CARPETA]')
    total_tamano = sum(tamano for _, tipo, tamano in archivos_copiados if tipo == '[ARCHIVO]')

    html = f"""
    <html>
    <head>
        <title>Informe de Copia - {nombre_carpeta_origen}</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            h1, h2 {{ color: #333; }}
            .summary {{ 
                background-color: #e8f5e9; 
                border: 1px solid #a5d6a7; 
                padding: 15px; 
                border-radius: 5px;
                margin: 20px 0;
            }}
            .total {{ font-weight: bold; }}
            .comparison {{ 
                background-color: #e3f2fd; 
                border: 1px solid #90caf9; 
                padding: 15px; 
                border-radius: 5px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h1>Informe de Copia - {nombre_carpeta_origen} - {fecha}</h1>
        
        <div class="summary">
            <h2>Resumen del Respaldo</h2>
            <p><span class="total">Carpeta origen:</span> {origen}</p>
            <p><span class="total">Carpeta destino:</span> {destino}</p>
            <p><span class="total">Total de Archivos:</span> {total_archivos}</p>
            <p><span class="total">Total de Carpetas:</span> {total_carpetas}</p>
            <p><span class="total">Tamaño Total Copiado:</span> {convertir_tamano(total_tamano)}</p>
        </div>
        
        <div class="comparison">
            <h2>Comparación de Tamaño Antes y Después</h2>
            <p><span class="total">Tamaño del destino antes de la copia:</span> {convertir_tamano(tamaño_destino_antes)}</p>
            <p><span class="total">Tamaño del destino después de la copia:</span> {convertir_tamano(tamaño_destino_despues)}</p>
            <p><span class="total">Diferencia de tamaño:</span> {convertir_tamano(tamaño_diferencia)}</p>
        </div>
        
        <h2>Archivos Copiados</h2>
        <table border='1'>
            <tr><th>Tipo</th><th>Ruta</th><th>Tamaño</th></tr>
            {''.join(f'<tr><td>{tipo}</td><td>{ruta}</td><td>{convertir_tamano(tamano)}</td></tr>' for ruta, tipo, tamano in archivos_copiados)}
            <tr class="total">
                <td colspan="2">Total</td>
                <td>{convertir_tamano(total_tamano)}</td>
            </tr>
        </table>
        
        <h2>Árbol de Archivos en Origen</h2>
        <table border='1'>
            <tr><th>Carpeta</th><th>Tamaño</th></tr>
            {''.join(f'<tr><td>{carp}</td><td>{convertir_tamano(tamano)}</td></tr>' for carp, tamano in arbol_origen.items())}
        </table>
        
        <h2>Árbol de Archivos en Destino</h2>
        <table border='1'>
            <tr><th>Carpeta</th><th>Tamaño</th></tr>
            {''.join(f'<tr><td>{carp}</td><td>{convertir_tamano(tamano)}</td></tr>' for carp, tamano in arbol_destino.items())}
        </table>
    </body>
    </html>
    """
    # Generar nombre de archivo que incluya el directorio de origen
    nombre_fecha = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    nombre_informe = f"informe_copia_{nombre_carpeta_origen}_{nombre_fecha}.html"
    
    with open(nombre_informe, "w", encoding="utf-8") as f:
        f.write(html)
    return nombre_informe