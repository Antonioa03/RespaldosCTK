#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Widget para mostrar directorios e ítems en la interfaz
"""

import os
import customtkinter as ctk
from app.utils import convertir_tamano

class DirectorioItem(ctk.CTkFrame):
    """Widget personalizado para representar un directorio o archivo en la lista de selección"""
    def __init__(self, master, ruta, es_dir, tamano, profundidad=0, **kwargs):
        super().__init__(master, **kwargs)
        self.ruta = ruta
        self.es_dir = es_dir
        self.tamano = tamano
        self.profundidad = profundidad
        self.nombre = os.path.basename(ruta) or ruta  # Si es raíz, usar la ruta completa
        
        # Configuración de la variable para el checkbox
        self.var_seleccionado = ctk.BooleanVar(value=True)
        
        # Crear elementos de la interfaz
        self.grid_columnconfigure(1, weight=1)  # Columna del nombre con peso 1
        
        # Padding según la profundidad para crear la estructura de árbol
        padding = 20 * self.profundidad
        
        # Checkbox para seleccionar/deseleccionar
        self.checkbox = ctk.CTkCheckBox(self, text="", variable=self.var_seleccionado,
                                         onvalue=True, offvalue=False)
        self.checkbox.grid(row=0, column=0, padx=(padding, 5), pady=2, sticky="w")
        
        # Icono y nombre
        icono = "📁" if es_dir else "📄"
        self.label_nombre = ctk.CTkLabel(self, text=f"{icono} {self.nombre}")
        self.label_nombre.grid(row=0, column=1, padx=5, pady=2, sticky="w")
        
        # Tamaño del archivo
        tamano_str = convertir_tamano(tamano) if not es_dir else ""
        self.label_tamano = ctk.CTkLabel(self, text=tamano_str, width=80)
        self.label_tamano.grid(row=0, column=2, padx=5, pady=2, sticky="e")

    def get_estado(self):
        """Devuelve el estado de selección del elemento"""
        return self.var_seleccionado.get()