#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Ventana principal de la aplicación
"""

import os
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import tkinter as tk

from app.utils import comparar_origen_destino, convertir_tamano
from app.ui.directory_item import DirectorioItem
from app.backup import copiar_con_robocopy, copiar_archivos_manualmente, copiar_archivo_manual
from app.reporte import generar_reporte_html
from app.email_sender import probar_conexion_smtp, enviar_informe_por_correo

class PyRespaldosApp(ctk.CTk):
    """Aplicación principal de PyRespaldos con CustomTkinter"""
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("PyRespaldos")
        self.geometry("900x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Variables de la aplicación
        self.ruta_origen = ""
        self.ruta_destino = ""
        self.elementos_mostrados = {}  # Para mantener referencia a los elementos mostrados
        
        # Sección superior - Selección de rutas
        self.crear_seccion_rutas()
        
        # Sección media - Opciones
        self.crear_seccion_opciones()
        
        # Sección de selección de archivos y carpetas
        self.crear_seccion_seleccion()
        
        # Sección inferior - Botones de acción
        self.crear_seccion_acciones()
        
        # Estado de copia y progreso
        self.crear_seccion_estado()

    def crear_seccion_rutas(self):
        """Crea la sección para seleccionar rutas de origen y destino"""
        frame_rutas = ctk.CTkFrame(self)
        frame_rutas.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_rutas.grid_columnconfigure(1, weight=1)
        
        # Origen
        ctk.CTkLabel(frame_rutas, text="Origen:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_origen = ctk.CTkEntry(frame_rutas)
        self.entry_origen.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_rutas, text="Examinar", command=self.seleccionar_origen).grid(row=0, column=2, padx=10, pady=10)
        
        # Destino
        ctk.CTkLabel(frame_rutas, text="Destino:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_destino = ctk.CTkEntry(frame_rutas)
        self.entry_destino.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_rutas, text="Examinar", command=self.seleccionar_destino).grid(row=1, column=2, padx=10, pady=10)

    def crear_seccion_opciones(self):
        """Crea la sección de opciones adicionales"""
        frame_opciones = ctk.CTkFrame(self)
        frame_opciones.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.var_multihilo = ctk.BooleanVar(value=True)
        self.var_verificar = ctk.BooleanVar(value=True)
        self.var_enviar_correo = ctk.BooleanVar(value=False)
        
        # Primera fila de opciones
        ctk.CTkCheckBox(frame_opciones, text="Usar múltiples hilos (más rápido)", variable=self.var_multihilo).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(frame_opciones, text="Verificar archivos copiados", variable=self.var_verificar).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        ctk.CTkCheckBox(frame_opciones, text="Enviar informe por correo", variable=self.var_enviar_correo, command=self.toggle_email_options).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        # Segunda fila para opciones de correo
        self.frame_email = ctk.CTkFrame(frame_opciones)
        self.frame_email.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.frame_email.grid_columnconfigure(1, weight=1)
        self.frame_email.grid_remove()  # Oculto por defecto
        
        # Campos de correo electrónico
        ctk.CTkLabel(self.frame_email, text="Correo:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(self.frame_email)
        self.entry_email.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.frame_email, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_password = ctk.CTkEntry(self.frame_email, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.frame_email, text="Destinatario:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_destinatario = ctk.CTkEntry(self.frame_email)
        self.entry_destinatario.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Servidor SMTP
        ctk.CTkLabel(self.frame_email, text="Servidor SMTP:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_smtp = ctk.CTkEntry(self.frame_email)
        self.entry_smtp.insert(0, "smtp.gmail.com")
        self.entry_smtp.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        ctk.CTkLabel(self.frame_email, text="Puerto:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_puerto = ctk.CTkEntry(self.frame_email)
        self.entry_puerto.insert(0, "587")
        self.entry_puerto.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        
        # Botón para probar configuración de correo
        ctk.CTkButton(self.frame_email, text="Probar conexión", command=self.probar_conexion_email).grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Botón de analizar
        frame_botones = ctk.CTkFrame(frame_opciones)
        frame_botones.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        frame_botones.grid_columnconfigure(0, weight=1)
        
        ctk.CTkButton(frame_botones, text="Analizar", command=self.analizar_directorios).pack(padx=10, pady=5, fill="x")

    def crear_seccion_seleccion(self):
        """Crea la sección para seleccionar archivos y carpetas"""
        frame_titulo = ctk.CTkFrame(self)
        frame_titulo.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="ew")
        
        ctk.CTkLabel(frame_titulo, text="Selecciona los archivos y carpetas a copiar:").pack(side="left", padx=10, pady=5)
        self.label_total = ctk.CTkLabel(frame_titulo, text="")
        self.label_total.pack(side="right", padx=10, pady=5)
        
        # Frame con scroll para la lista de archivos
        self.frame_contenedor = ctk.CTkScrollableFrame(self)
        self.frame_contenedor.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_contenedor.grid_columnconfigure(0, weight=1)

    def crear_seccion_acciones(self):
        """Crea la sección para los botones de acción"""
        frame_acciones = ctk.CTkFrame(self)
        frame_acciones.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        
        frame_acciones.grid_columnconfigure(0, weight=1)
        frame_acciones.grid_columnconfigure(1, weight=1)
        frame_acciones.grid_columnconfigure(2, weight=1)
        
        ctk.CTkButton(frame_acciones, text="Seleccionar Todo", command=self.seleccionar_todo).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(frame_acciones, text="Deseleccionar Todo", command=self.deseleccionar_todo).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.btn_copiar = ctk.CTkButton(frame_acciones, text="Iniciar Copia", command=self.iniciar_copia, state="disabled")
        self.btn_copiar.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

    def crear_seccion_estado(self):
        """Crea la sección para mostrar el estado y progreso de la copia"""
        frame_estado = ctk.CTkFrame(self)
        frame_estado.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
        frame_estado.grid_columnconfigure(0, weight=1)
        
        self.label_estado = ctk.CTkLabel(frame_estado, text="Esperando selección de archivos...")
        self.label_estado.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.barra_progreso = ctk.CTkProgressBar(frame_estado)
        self.barra_progreso.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.barra_progreso.set(0)

    def toggle_email_options(self):
        """Muestra u oculta las opciones de correo según el estado del checkbox"""
        if self.var_enviar_correo.get():
            self.frame_email.grid()
        else:
            self.frame_email.grid_remove()
            
    def probar_conexion_email(self):
        """Prueba la conexión al servidor SMTP con las credenciales proporcionadas"""
        correo = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        servidor = self.entry_smtp.get().strip()
        puerto = self.entry_puerto.get().strip()
        
        if not correo or not password or not servidor or not puerto:
            messagebox.showerror("Error", "Por favor completa todos los campos de configuración de correo")
            return
        
        self.label_estado.configure(text="Probando conexión al servidor SMTP...")
        self.update_idletasks()
        
        exito, mensaje = probar_conexion_smtp(correo, password, servidor, puerto)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.label_estado.configure(text="Conexión SMTP probada con éxito")
        else:
            messagebox.showerror("Error", mensaje)
            self.label_estado.configure(text="Error al conectar con el servidor SMTP")

    def seleccionar_origen(self):
        """Abre un diálogo para seleccionar la carpeta de origen"""
        directorio = filedialog.askdirectory(title="Selecciona la carpeta de origen")
        if directorio:
            self.ruta_origen = directorio
            self.entry_origen.delete(0, tk.END)
            self.entry_origen.insert(0, directorio)
            self.actualizar_estado()

    def seleccionar_destino(self):
        """Abre un diálogo para seleccionar la carpeta de destino"""
        directorio = filedialog.askdirectory(title="Selecciona la carpeta de destino")
        if directorio:
            self.ruta_destino = directorio
            self.entry_destino.delete(0, tk.END)
            self.entry_destino.insert(0, directorio)
            self.actualizar_estado()

    def analizar_directorios(self):
        """Analiza los directorios y muestra los elementos para seleccionar"""
        self.ruta_origen = self.entry_origen.get().strip()
        self.ruta_destino = self.entry_destino.get().strip()
        
        if not self.ruta_origen or not os.path.exists(self.ruta_origen):
            messagebox.showerror("Error", "La ruta de origen no es válida")
            return
            
        if not self.ruta_destino or not os.path.exists(self.ruta_destino):
            messagebox.showerror("Error", "La ruta de destino no es válida")
            return
            
        # Limpiar elementos previos
        for widget in self.frame_contenedor.winfo_children():
            widget.destroy()
        self.elementos_mostrados = {}
        
        # Mostrar mensaje de carga
        self.label_estado.configure(text="Analizando directorios... Por favor espera.")
        self.update_idletasks()
        
        # Iniciar análisis en un hilo separado
        threading.Thread(target=self._analizar_en_hilo, daemon=True).start()

    def _analizar_en_hilo(self):
        """Realiza el análisis de directorios en un hilo separado"""
        try:
            # Analizar la estructura del directorio de origen
            estructura = []
            tamano_total = 0
            
            # Primero todas las carpetas
            for root, dirs, files in os.walk(self.ruta_origen):
                ruta_relativa = os.path.relpath(root, self.ruta_origen)
                if ruta_relativa != ".":  # No mostrar la carpeta raíz
                    nivel = ruta_relativa.count(os.sep)
                    estructura.append((ruta_relativa, True, 0, nivel))
            
            # Luego todos los archivos
            for root, dirs, files in os.walk(self.ruta_origen):
                ruta_relativa = os.path.relpath(root, self.ruta_origen)
                for file in files:
                    try:
                        ruta_archivo = os.path.join(root, file)
                        tamano = os.path.getsize(ruta_archivo) if os.path.exists(ruta_archivo) else 0
                        nivel = ruta_relativa.count(os.sep) + 1
                        estructura.append((os.path.join(ruta_relativa, file), False, tamano, nivel))
                        tamano_total += tamano
                    except Exception as e:
                        print(f"Error al obtener tamaño de {ruta_archivo}: {e}")
            
            # Actualizar la interfaz en el hilo principal
            self.after(0, lambda: self._mostrar_estructura(estructura, tamano_total))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error al analizar los directorios: {e}"))
            self.after(0, lambda: self.label_estado.configure(text="Error al analizar los directorios."))

    def _mostrar_estructura(self, estructura, tamano_total):
        """Muestra la estructura de archivos y carpetas en la interfaz"""
        for ruta, es_dir, tamano, nivel in estructura:
            item = DirectorioItem(self.frame_contenedor, ruta, es_dir, tamano, nivel, height=30)
            item.pack(fill="x", padx=5, pady=2)
            self.elementos_mostrados[ruta] = item
        
        # Actualizar información de tamaño total
        self.label_total.configure(text=f"Tamaño total: {convertir_tamano(tamano_total)}")
        
        # Habilitar botón de copia
        self.btn_copiar.configure(state="normal")
        
        # Actualizar estado
        self.label_estado.configure(text=f"Se encontraron {len(estructura)} elementos. Selecciona los que deseas copiar.")

    def seleccionar_todo(self):
        """Selecciona todos los elementos de la lista"""
        for item in self.elementos_mostrados.values():
            item.var_seleccionado.set(True)

    def deseleccionar_todo(self):
        """Deselecciona todos los elementos de la lista"""
        for item in self.elementos_mostrados.values():
            item.var_seleccionado.set(False)

    def obtener_elementos_seleccionados(self):
        """Obtiene la lista de elementos seleccionados"""
        seleccionados = []
        for ruta, item in self.elementos_mostrados.items():
            if item.get_estado():
                seleccionados.append(ruta)
        return seleccionados

    def iniciar_copia(self):
        """Inicia el proceso de copia con los elementos seleccionados"""
        elementos_seleccionados = self.obtener_elementos_seleccionados()
        
        if not elementos_seleccionados:
            messagebox.showwarning("Advertencia", "No has seleccionado ningún elemento para copiar")
            return
            
        # Previsualizar elementos a copiar
        elementos_a_copiar = comparar_origen_destino(self.ruta_origen, self.ruta_destino, elementos_seleccionados)
        
        if not elementos_a_copiar:
            messagebox.showinfo("Información", "No hay elementos nuevos o modificados que necesiten ser copiados")
            return
            
        # Mostrar confirmación con resumen
        texto_confirmacion = "Se copiarán los siguientes elementos:\n\n"
        texto_confirmacion += f"Total: {len(elementos_a_copiar)} elementos\n"
        
        archivos = [e for e in elementos_a_copiar if e[1] == '[ARCHIVO]']
        carpetas = [e for e in elementos_a_copiar if e[1] == '[CARPETA]']
        
        texto_confirmacion += f"Archivos: {len(archivos)}\n"
        texto_confirmacion += f"Carpetas: {len(carpetas)}\n\n"
        
        # Calcular tamaño total a copiar
        tamano_total = sum(tamano for _, _, tamano in elementos_a_copiar)
        texto_confirmacion += f"Tamaño total: {convertir_tamano(tamano_total)}\n\n"
        texto_confirmacion += "¿Deseas continuar?"
        
        confirmar = messagebox.askyesno("Confirmar copia", texto_confirmacion)
        if not confirmar:
            return
            
        # Desactivar botones mientras se realiza la copia
        self.btn_copiar.configure(state="disabled")
        
        # Iniciar la copia en un hilo separado
        threading.Thread(target=self._copiar_en_hilo, args=(elementos_seleccionados, elementos_a_copiar), daemon=True).start()

    def _copiar_en_hilo(self, elementos_seleccionados, elementos_a_copiar):
        """Realiza la copia en un hilo separado"""
        try:
            # Actualizar estado
            self.after(0, lambda: self.label_estado.configure(text="Iniciando copia..."))
            self.after(0, lambda: self.barra_progreso.set(0.05))
            
            # Variable para controlar si se usará robocopy o copia manual
            usar_robocopy = True
            elementos_copiados = []
            
            if usar_robocopy:
                try:
                    # Preparar opciones para robocopy
                    opciones_adicionales = ""
                    
                    if self.var_multihilo.get():
                        opciones_adicionales += "/MT:8"  # Multihilo
                        
                    if self.var_verificar.get():
                        opciones_adicionales += " /V"  # Verificar
                    
                    self.after(0, lambda: self.label_estado.configure(text="Ejecutando copia con Robocopy..."))
                    self.after(0, lambda: self.barra_progreso.set(0.1))
                    
                    # Ejecutar robocopy
                    exito, codigo_salida, output_log, error_msg = copiar_con_robocopy(
                        self.ruta_origen, self.ruta_destino, elementos_seleccionados, opciones_adicionales
                    )
                    
                    # Actualizar progreso basado en la salida
                    for i, linea in enumerate(output_log):
                        if i % 10 == 0:  # Actualizar cada 10 líneas para no sobrecargar la UI
                            progreso = min(0.1 + (i / len(output_log) * 0.8), 0.9)
                            self.after(0, lambda p=progreso: self.barra_progreso.set(p))
                            self.after(0, lambda l=linea: self.label_estado.configure(text=f"Copiando: {l[:60]}..."))
                    
                    if not exito:
                        raise Exception(error_msg)
                    
                    # Robocopy se ejecutó correctamente
                    elementos_copiados = elementos_a_copiar
                
                except Exception as e:
                    # Si falla robocopy, lo registramos y procedemos a copia manual
                    print(f"Error con robocopy: {e}")
                    usar_robocopy = False
            
            # Si no usamos robocopy o falló, hacemos copia manual
            if not usar_robocopy:
                self.after(0, lambda: self.label_estado.configure(text="Realizando copia manual de archivos..."))
                
                # Función de callback para actualizar progreso
                def actualizar_progreso(idx, total, ruta):
                    progreso = 0.1 + (idx / total * 0.8)
                    self.after(0, lambda p=progreso: self.barra_progreso.set(p))
                    self.after(0, lambda r=ruta: self.label_estado.configure(text=f"Copiando: {r[:60]}..."))
                
                # Copiar manualmente
                elementos_copiados = copiar_archivos_manualmente(
                    self.ruta_origen, self.ruta_destino, elementos_seleccionados, actualizar_progreso
                )
            
            # Generar informe
            self.after(0, lambda: self.label_estado.configure(text="Generando informe..."))
            self.after(0, lambda: self.barra_progreso.set(0.95))
            
            informe = generar_reporte_html(self.ruta_origen, self.ruta_destino, elementos_copiados)
            
            # Completado
            self.after(0, lambda: self.barra_progreso.set(0.98))
            
            # Enviar informe por correo si está habilitado
            if self.var_enviar_correo.get():
                self.after(0, lambda: self.label_estado.configure(text="Enviando informe por correo..."))
                
                correo = self.entry_email.get().strip()
                password = self.entry_password.get().strip()
                destinatario = self.entry_destinatario.get().strip()
                servidor = self.entry_smtp.get().strip()
                puerto = self.entry_puerto.get().strip()
                
                exito, mensaje = enviar_informe_por_correo(
                    informe, correo, password, destinatario, servidor, puerto, 
                    self.ruta_origen, self.ruta_destino
                )
                
                if exito:
                    self.after(0, lambda: self.label_estado.configure(text=f"Copia completada. Informe enviado por correo y guardado en: {informe}"))
                    mensaje_final = f"Copia finalizada con éxito.\nSe ha generado un informe: {informe}\nEl informe ha sido enviado por correo."
                else:
                    self.after(0, lambda: self.label_estado.configure(text=f"Copia completada. Informe guardado en: {informe}. Error al enviar por correo."))
                    mensaje_final = f"Copia finalizada con éxito.\nSe ha generado un informe: {informe}\nNo se pudo enviar el informe por correo: {mensaje}"
            else:
                self.after(0, lambda: self.label_estado.configure(text=f"Copia completada. Informe guardado en: {informe}"))
                mensaje_final = f"Copia finalizada con éxito.\nSe ha generado un informe: {informe}"
            
            self.after(0, lambda: self.barra_progreso.set(1.0))
            self.after(0, lambda: self.btn_copiar.configure(state="normal"))
            self.after(0, lambda: messagebox.showinfo("Operación completada", mensaje_final))
            
            # Intentar abrir el informe
            try:
                os.startfile(informe)
            except Exception as e:
                print(f"No se pudo abrir el informe: {e}")
                
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Error durante la copia: {e}"))
            self.after(0, lambda: self.label_estado.configure(text=f"Error: {str(e)}"))
            self.after(0, lambda: self.btn_copiar.configure(state="normal"))
            
    def actualizar_estado(self):
        """Actualiza el estado de la aplicación según las rutas seleccionadas"""
        if self.ruta_origen and self.ruta_destino:
            self.label_estado.configure(text="Pulsa 'Analizar' para ver los archivos disponibles")
        elif self.ruta_origen:
            self.label_estado.configure(text="Selecciona una carpeta de destino")
        else:
            self.label_estado.configure(text="Selecciona una carpeta de origen")