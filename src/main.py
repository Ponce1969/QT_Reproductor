import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import os
import ctypes
from music_player import MusicPlayer

def main():
    # Crear la aplicación
    app = QApplication(sys.argv)
    
    # Establecer el ID de la aplicación en Windows
    if os.name == 'nt':
        myappid = 'mycompany.musicplayer.qt6.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    # Establecer el icono para toda la aplicación
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon', 'icon_aplicacion.png')
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)
    
    # Crear y mostrar el reproductor
    player = MusicPlayer()
    player.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec())

if __name__ == '__main__':
    main()