#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Módulo para envío de correos electrónicos
"""

import os
import re
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def probar_conexion_smtp(correo, password, servidor, puerto):
    """
    Prueba la conexión al servidor SMTP
    
    Args:
        correo: Dirección de correo
        password: Contraseña
        servidor: Servidor SMTP
        puerto: Puerto del servidor
        
    Returns:
        Tupla (exito, mensaje)
    """
    try:
        # Intentar conectar al servidor SMTP
        server = smtplib.SMTP(servidor, int(puerto))
        server.ehlo()
        server.starttls()
        server.login(correo, password)
        server.quit()
        
        return (True, "Conexión al servidor SMTP establecida correctamente")
    except Exception as e:
        return (False, f"No se pudo conectar al servidor SMTP: {str(e)}")

def enviar_informe_por_correo(ruta_informe, correo, password, destinatario, servidor, puerto, origen, destino):
    """
    Envía el informe por correo electrónico
    
    Args:
        ruta_informe: Ruta al archivo de informe HTML
        correo: Dirección de correo del remitente
        password: Contraseña
        destinatario: Correo del destinatario
        servidor: Servidor SMTP
        puerto: Puerto del servidor
        origen: Ruta de origen del respaldo
        destino: Ruta de destino del respaldo
        
    Returns:
        Tupla (exito, mensaje)
    """
    try:
        # Obtener estadísticas para el cuerpo del mensaje
        total_archivos = 0
        total_carpetas = 0
        total_tamano = "0 B"
        
        # Leer el archivo HTML para extraer estadísticas
        with open(ruta_informe, 'r', encoding='utf-8') as f:
            contenido = f.read()
            # Extraer estadísticas usando búsqueda de texto simple
            
            # Buscar totales en el HTML
            patron_archivos = r'Total de Archivos:</span>\s*(\d+)'
            patron_carpetas = r'Total de Carpetas:</span>\s*(\d+)'
            patron_tamano = r'Tamaño Total:</span>\s*([\d\.]+ [KMGT]?B)'
            
            match_archivos = re.search(patron_archivos, contenido)
            match_carpetas = re.search(patron_carpetas, contenido)
            match_tamano = re.search(patron_tamano, contenido)
            
            if match_archivos:
                total_archivos = match_archivos.group(1)
            if match_carpetas:
                total_carpetas = match_carpetas.group(1)
            if match_tamano:
                total_tamano = match_tamano.group(1)
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = correo
        msg['To'] = destinatario
        msg['Subject'] = f"Informe de Respaldo - {os.path.basename(origen)} - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Cuerpo del mensaje
        cuerpo = "Se adjunta el informe del respaldo realizado.\n\n"
        cuerpo += f"Origen: {origen}\n"
        cuerpo += f"Destino: {destino}\n"
        cuerpo += f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        cuerpo += f"Resumen del respaldo:\n"
        cuerpo += f"- Total de archivos: {total_archivos}\n"
        cuerpo += f"- Total de carpetas: {total_carpetas}\n"
        cuerpo += f"- Tamaño total: {total_tamano}\n"
        
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Adjuntar informe HTML
        with open(ruta_informe, "rb") as f:
            attachment = MIMEApplication(f.read())
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(ruta_informe))
            msg.attach(attachment)
        
        # Conectar y enviar
        server = smtplib.SMTP(servidor, int(puerto))
        server.ehlo()
        server.starttls()
        server.login(correo, password)
        server.send_message(msg)
        server.quit()
        
        return (True, "Correo enviado correctamente")
    except Exception as e:
        return (False, f"No se pudo enviar el informe por correo: {str(e)}")