#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Aplicación para realizar respaldos selectivos
Archivo principal que inicia la aplicación
"""

import customtkinter as ctk
from app.ui.main_window import PyRespaldosApp

if __name__ == "__main__":
    # Configuración general de CustomTkinter
    ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    # Iniciar la aplicación
    app = PyRespaldosApp()
    app.mainloop()