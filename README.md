# 📁 PyRespaldos

## 🌟 Respaldos selectivos con interfaz gráfica moderna

PyRespaldos es una aplicación para realizar respaldos selectivos de archivos y carpetas con una interfaz gráfica moderna y fácil de usar.

## ✨ Características

- 🖌️ Interfaz gráfica moderna con CustomTkinter
- 🔍 Selección visual de archivos y carpetas a respaldar
- 🚀 Respaldo usando Robocopy (en Windows) o método manual
- ✅ Verificación de archivos copiados
- 📊 Generación de informes detallados en HTML
- 📧 Envío de informes por correo electrónico
- 📈 Visualización de tamaños y estructura de carpetas

## 📋 Requisitos

- 🐍 Python 3.7 o superior
- 📦 Paquetes especificados en requirements.txt

## 🛠️ Instalación

1. 📥 Clonar o descargar este repositorio
2. 📦 Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. 🏃‍♂️ Ejecutar la aplicación:

```bash
python main.py
```

2. 📂 Seleccionar las carpetas de origen y destino
3. 🔍 Hacer clic en "Analizar" para ver la estructura de archivos
4. ✓ Seleccionar los archivos y carpetas que desea respaldar
5. ⚙️ Configurar opciones adicionales según sea necesario
6. 🚀 Hacer clic en "Iniciar Copia" para comenzar el respaldo

## ⚙️ Opciones de configuración

- 🧵 **Usar múltiples hilos**: Acelera el proceso de copia (solo funciona con Robocopy)
- 🔄 **Verificar archivos copiados**: Comprueba que los archivos se hayan copiado correctamente
- 📨 **Enviar informe por correo**: Envía el informe de respaldo por correo electrónico

## 📁 Estructura del proyecto

```
/pyrespaldos/
│
├── main.py                     # 🚀 Archivo principal para iniciar la aplicación
│
├── app/                        # 📦 Carpeta principal del módulo
│   ├── utils.py                # 🔧 Funciones utilitarias generales
│   ├── backup.py               # 💾 Funciones para realizar operaciones de copia
│   ├── reporte.py              # 📊 Funciones para generar informes
│   ├── email_sender.py         # 📧 Funciones para enviar correos
│   │
│   ├── ui/                     # 🖌️ Carpeta para componentes de la interfaz de usuario
│   │   ├── main_window.py      # 🪟 Clase para la ventana principal de la aplicación
│   │   └── directory_item.py   # 📂 Widget personalizado para mostrar directorios/archivos
│   │
│   └── config/                 # ⚙️ Carpeta para configuración
```

## 📝 Notas

- **🛠️ Robocopy**: La aplicación utiliza Robocopy en sistemas Windows para una copia más eficiente. En sistemas que no disponen de Robocopy, se utiliza un método de copia manual.
- **📧 Correo electrónico**: Para usar Gmail, es posible que necesite una "contraseña de aplicación" en lugar de su contraseña normal.

## 🔑 Funcionalidades principales

### 📋 Selección detallada
Selecciona exactamente qué archivos y carpetas quieres respaldar, sin necesidad de copiar todo.

### 📊 Informes detallados
Cada respaldo genera un informe HTML con estadísticas completas, incluyendo:
- Total de archivos y carpetas
- Tamaño del respaldo
- Comparación entre origen y destino

### 📧 Notificaciones por correo
Recibe informes de tus respaldos directamente en tu correo electrónico.

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar esta aplicación, no dudes en crear un pull request o abrir un issue.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.