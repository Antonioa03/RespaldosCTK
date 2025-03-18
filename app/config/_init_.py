#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyRespaldos - Subpaquete de configuración
"""

# Valores predeterminados de configuración
DEFAULT_CONFIG = {
    'email': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
    },
    'backup': {
        'use_multithreading': True,
        'verify_copy': True,
        'send_email': False
    },
    'ui': {
        'theme': 'system',
        'color_theme': 'blue'
    }
}