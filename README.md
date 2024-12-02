# Reproductor de Música PyQt6

Un reproductor de música moderno y elegante desarrollado con PyQt6 y Pygame, que ofrece una interfaz gráfica intuitiva y capacidades de reproducción de audio robustas.

![Icono de la Aplicación](src/icon/icon_aplicacion.png)

## Características

- 🎵 Reproducción de archivos de audio
- 🎨 Temas claro y oscuro
- 📋 Gestión de lista de reproducción
- 🎚️ Control de volumen
- 🖼️ Fondo personalizado
- 🎯 Interfaz moderna y semi-transparente
- 📱 Diseño responsive

## Requisitos del Sistema

- Windows 10 o superior
- Espacio en disco: ~100MB
- Memoria RAM: 256MB mínimo

## Tecnologías Utilizadas

- Python 3.8+
- PyQt6 - Framework de interfaz gráfica
- Pygame - Motor de audio
- Qt Stylesheet (QSS) - Estilos personalizados

## Dependencias

```
pygame==2.6.1
PyQt6==6.7.1
PyQt6-Qt6==6.7.3
PyQt6_sip==13.8.0
PySide6==6.8.0.2
PySide6_Addons==6.8.0.2
PySide6_Essentials==6.8.0.2
shiboken6==6.8.0.2
```

## Instalación para Desarrollo

1. Clonar el repositorio:
```bash
git clone [URL_del_repositorio]
cd [nombre_del_repositorio]
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r src/requirements.txt
```

## Uso

### Versión de Desarrollo
```bash
python src/main.py
```

### Versión Portable
1. Descargar la última versión desde la sección de releases
2. Descomprimir el archivo ZIP
3. Ejecutar `ReproductorMusica.exe`

## Estructura del Proyecto

```
src/
├── main.py              # Punto de entrada de la aplicación
├── music_player.py      # Clase principal del reproductor
├── requirements.txt     # Dependencias del proyecto
├── icon/               # Iconos de la aplicación
├── imagen/             # Imágenes y fondos
└── styles/             # Archivos de estilo QSS
    ├── styles_light.qss
    └── styles_dark.qss
```

## Características Principales

### Reproducción de Audio
- Play/Pause/Stop
- Control de volumen
- Navegación entre pistas

### Gestión de Playlist
- Agregar/Eliminar canciones
- Reproducción secuencial
- Visualización de la pista actual

### Temas
- Tema claro y oscuro
- Cambio dinámico de temas
- Persistencia del fondo de imagen

## Creación del Ejecutable

1. Instalar PyInstaller:
```bash
pip install pyinstaller
```

2. Generar el ejecutable:
```bash
pyinstaller ReproductorMusica.spec
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu función (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

[Gonzalo Ponce] - [gompatri@gmail.com]

Link del Proyecto: [https://github.com/Ponce1969/reproductor_qt.git]

## Agradecimientos

- PyQt6 por el framework de GUI
- Pygame por el motor de audio
- Todos los contribuidores que han ayudado a mejorar este proyecto
