import sys
import pygame
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QSlider, QFileDialog,
                            QListWidget)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QIcon, QPixmap, QPalette, QBrush
import os
import ctypes
from mutagen.mp3 import MP3
from mutagen.wave import WAVE

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reproductor de Música")
        self.setGeometry(100, 100, 800, 600)
        
        # Establecer el directorio base para la música
        self.base_dir = os.path.join(os.path.dirname(__file__), 'music')
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        
        # Establecer el icono de la aplicación
        icon_path = os.path.join(os.path.dirname(__file__), 'icon', 'icon_aplicacion2.png')

        
        self.app_icon = QIcon(icon_path)
        self.setWindowIcon(self.app_icon)
        
        # Establecer imagen de fondo
        self.set_background_image()
        
        # Inicializar Pygame mixer
        pygame.mixer.init()
        
        # Variables de control
        self.is_playing = False
        self.current_position = 0
        self.song_length = 0
        self.last_position = 0
        
        # Lista de reproducción
        self.playlist = []
        self.current_track = 0
        
        # Control del tema
        self.is_dark_theme = False
        self.load_theme()
        
        # Timer para actualizar la posición
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_position)
        self.update_timer.start(1000)  # Actualizar cada segundo
        
        self.setup_ui()
        
        # Cargar la lista de reproducción guardada después de setup_ui
        self.load_playlist()

    def set_background_image(self):
        background_path = os.path.join(os.path.dirname(__file__), 'imagen', 'fondo_musical_qt.jpeg')
        palette = QPalette()
        background_pixmap = QPixmap(background_path)
        scaled_pixmap = background_pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)
    
    def load_theme(self):
        theme_file = 'styles_dark.qss' if self.is_dark_theme else 'styles_light.qss'
        style_path = os.path.join(os.path.dirname(__file__), 'styles', theme_file)
        if os.path.exists(style_path):
            with open(style_path, 'r') as file:
                self.setStyleSheet(file.read())
        # Restaurar el fondo después de aplicar el tema
        self.set_background_image()
    
    def get_audio_length(self, file_path):
        try:
            if file_path.lower().endswith('.mp3'):
                audio = MP3(file_path)
                return int(audio.info.length)
            elif file_path.lower().endswith('.wav'):
                audio = WAVE(file_path)
                return int(audio.info.length)
            return 0
        except Exception:
            return 0

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def setup_ui(self):
        # Habilitar arrastrar y soltar
        self.setAcceptDrops(True)
        
        central_widget = QWidget()
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Lista de reproducción
        self.track_list = QListWidget()
        self.track_list.doubleClicked.connect(self.play_selected_track)
        layout.addWidget(self.track_list)
        
        # Etiqueta para el nombre de la canción
        self.song_label = QLabel()
        self.song_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_song_label()  # Inicializar la etiqueta
        layout.addWidget(self.song_label)
        
        # Panel de progreso
        progress_widget = QWidget()
        progress_layout = QHBoxLayout(progress_widget)
        
        # Etiquetas de tiempo
        self.time_label = QLabel("00:00")
        self.duration_label = QLabel("00:00")
        
        # Barra de progreso
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setMinimum(0)
        self.progress_slider.sliderMoved.connect(self.set_position)
        self.progress_slider.sliderPressed.connect(self.on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)
        
        progress_layout.addWidget(self.time_label)
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addWidget(self.duration_label)
        layout.addWidget(progress_widget)
        
        # Panel de controles
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        
        # Botones de control
        self.prev_button = QPushButton("Anterior")
        self.prev_button.setObjectName("prev_button")
        self.prev_button.clicked.connect(self.previous_track)  # Conectar el botón
        
        self.play_button = QPushButton("Reproducir")
        self.play_button.setObjectName("play_button")
        self.play_button.clicked.connect(self.play_pause)
        
        self.next_button = QPushButton("Siguiente")
        self.next_button.setObjectName("next_button")
        self.next_button.clicked.connect(self.next_track)  # Conectar el botón
        
        self.stop_button = QPushButton("Detener")
        self.stop_button.setObjectName("stop_button")
        self.stop_button.clicked.connect(self.stop)
        
        # Control de volumen
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.valueChanged.connect(self.set_volume)
        
        # Agregar botones al layout
        controls_layout.addWidget(self.prev_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.next_button)
        controls_layout.addWidget(self.stop_button)
        controls_layout.addWidget(QLabel("Volumen:"))
        controls_layout.addWidget(self.volume_slider)
        
        layout.addWidget(controls_widget)
        
        # Botón para agregar canciones
        self.add_button = QPushButton("Agregar canciones")
        self.add_button.setObjectName("add_button")
        self.add_button.clicked.connect(self.add_files)
        layout.addWidget(self.add_button)
        
        # Botón para cambiar tema
        self.theme_button = QPushButton("Cambiar Tema")
        self.theme_button.setObjectName("theme_button")
        self.theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_button)
        
    def load_playlist(self):
        playlist_file = os.path.join(os.path.dirname(__file__), 'playlist.json')
        try:
            if os.path.exists(playlist_file):
                with open(playlist_file, 'r', encoding='utf-8') as file:
                    relative_paths = json.load(file)
                    # Convertir rutas relativas a absolutas y verificar que existan
                    for rel_path in relative_paths:
                        abs_path = self.get_absolute_path(rel_path)
                        if os.path.exists(abs_path):
                            self.playlist.append(abs_path)
                            self.track_list.addItem(os.path.basename(abs_path))
                if self.playlist:
                    self.song_label.setText("Lista de reproducción cargada")
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al cargar la lista de reproducción")

    def save_playlist(self):
        playlist_file = os.path.join(os.path.dirname(__file__), 'playlist.json')
        try:
            # Guardar rutas relativas
            relative_paths = [self.get_relative_path(path) for path in self.playlist]
            with open(playlist_file, 'w', encoding='utf-8') as file:
                json.dump(relative_paths, file, ensure_ascii=False, indent=2)
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al guardar la lista de reproducción")

    def closeEvent(self, event):
        # Guardar la lista de reproducción antes de cerrar
        self.save_playlist()
        event.accept()

    def add_files(self):
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleccionar archivos de música",
                "",
                "Archivos de música (*.mp3 *.wav *.ogg);;Todos los archivos (*.*)"
            )
            
            if files:
                for file in files:
                    # Copiar el archivo a la carpeta de música si está fuera de ella
                    if not file.startswith(self.base_dir):
                        filename = os.path.basename(file)
                        new_path = os.path.join(self.base_dir, filename)
                        # Si ya existe un archivo con ese nombre, agregar un número
                        counter = 1
                        while os.path.exists(new_path):
                            name, ext = os.path.splitext(filename)
                            new_path = os.path.join(self.base_dir, f"{name}_{counter}{ext}")
                            counter += 1
                        import shutil
                        shutil.copy2(file, new_path)
                        file = new_path
                    
                    self.playlist.append(file)
                    self.track_list.addItem(os.path.basename(file))
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al cargar los archivos de música")

    def get_relative_path(self, absolute_path):
        try:
            return os.path.relpath(absolute_path, self.base_dir)
        except ValueError:
            return absolute_path

    def get_absolute_path(self, relative_path):
        if os.path.isabs(relative_path):
            return relative_path
        return os.path.join(self.base_dir, relative_path)

    def play_pause(self):
        if not self.playlist:
            if hasattr(self, 'song_label'):
                self.song_label.setText("No hay canciones en la lista de reproducción")
            return
            
        try:
            if not self.is_playing:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                else:
                    pygame.mixer.music.load(self.playlist[self.current_track])
                    pygame.mixer.music.play(start=self.current_position)
                self.is_playing = True
                self.play_button.setText("Pausar")
            else:
                pygame.mixer.music.pause()
                self.is_playing = False
                self.play_button.setText("Reproducir")
            self.update_song_label()
        except pygame.error as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al reproducir/pausar la música")
            self.is_playing = False
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error inesperado en la reproducción")
            self.is_playing = False
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.current_position = 0
        self.progress_slider.setValue(0)
        self.time_label.setText("00:00")
        self.play_button.setText("Reproducir")
    
    def next_track(self):
        if not self.playlist:
            return
        
        self.current_track = (self.current_track + 1) % len(self.playlist)
        try:
            # Obtener la duración de la nueva canción
            self.song_length = self.get_audio_length(self.playlist[self.current_track])
            self.progress_slider.setMaximum(self.song_length)
            self.duration_label.setText(self.format_time(self.song_length))
            
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.current_position = 0
            self.is_playing = True
            self.play_button.setText("Pausar")
            self.update_song_label()
            # Seleccionar la canción en la lista visual
            self.track_list.setCurrentRow(self.current_track)
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al reproducir la siguiente canción")
            self.is_playing = False

    def previous_track(self):
        if not self.playlist:
            return
        
        self.current_track = (self.current_track - 1) % len(self.playlist)
        try:
            # Obtener la duración de la nueva canción
            self.song_length = self.get_audio_length(self.playlist[self.current_track])
            self.progress_slider.setMaximum(self.song_length)
            self.duration_label.setText(self.format_time(self.song_length))
            
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.current_position = 0
            self.is_playing = True
            self.play_button.setText("Pausar")
            self.update_song_label()
            # Seleccionar la canción en la lista visual
            self.track_list.setCurrentRow(self.current_track)
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al reproducir la canción anterior")
            self.is_playing = False

    def play_selected_track(self):
        if not self.playlist:
            if hasattr(self, 'song_label'):
                self.song_label.setText("No hay canciones en la lista de reproducción")
            return
        
        try:
            selected_row = self.track_list.currentRow()
            if selected_row >= 0:
                self.current_track = selected_row
            
            # Obtener la duración de la canción
            self.song_length = self.get_audio_length(self.playlist[self.current_track])
            self.progress_slider.setMaximum(self.song_length)
            self.duration_label.setText(self.format_time(self.song_length))
            
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
            self.current_position = 0
            self.is_playing = True
            self.play_button.setText("Pausar")
            self.update_song_label()
            # Seleccionar la canción en la lista visual
            self.track_list.setCurrentRow(self.current_track)
        except Exception as e:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Error al reproducir la canción")
            self.is_playing = False
    
    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100.0)
    
    def on_slider_pressed(self):
        self.last_position = self.progress_slider.value()

    def on_slider_released(self):
        if self.is_playing and self.playlist:
            try:
                # Guardar la nueva posición deseada
                new_position = self.progress_slider.value()
                
                # Recargar y reproducir desde la nueva posición
                pygame.mixer.music.load(self.playlist[self.current_track])
                pygame.mixer.music.play(start=new_position)
                
                # Actualizar la posición actual
                self.current_position = new_position
                self.time_label.setText(self.format_time(new_position))
            except Exception as e:
                # Si hay un error, volver a la posición anterior
                self.progress_slider.setValue(self.last_position)
                self.current_position = self.last_position

    def update_position(self):
        if self.is_playing and pygame.mixer.music.get_busy():
            self.current_position += 1
            self.progress_slider.setValue(self.current_position)
            self.time_label.setText(self.format_time(self.current_position))
        
        # Verificar si la canción ha terminado
        if self.is_playing and not pygame.mixer.music.get_busy():
            self.next_track()

    def set_position(self, position):
        if self.is_playing:
            # Actualizar etiqueta de tiempo mientras se arrastra
            self.time_label.setText(self.format_time(position))

    def update_song_label(self):
        if self.playlist and self.is_playing:
            current_song = os.path.basename(self.playlist[self.current_track])
            if hasattr(self, 'song_label'):
                self.song_label.setText(f"Reproduciendo: {current_song}")
        else:
            if hasattr(self, 'song_label'):
                self.song_label.setText("No hay canción reproduciendo")
    
    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        self.load_theme()  # Esto también restaurará el fondo
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_background_image()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            # Verificar si al menos un archivo es de música
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
                    event.accept()
                    return
        event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files_added = False
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp3', '.wav', '.ogg')):
                # Copiar el archivo a la carpeta de música si está fuera de ella
                if not file_path.startswith(self.base_dir):
                    filename = os.path.basename(file_path)
                    new_path = os.path.join(self.base_dir, filename)
                    # Si ya existe un archivo con ese nombre, agregar un número
                    counter = 1
                    while os.path.exists(new_path):
                        name, ext = os.path.splitext(filename)
                        new_path = os.path.join(self.base_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    import shutil
                    shutil.copy2(file_path, new_path)
                    file_path = new_path
                
                self.playlist.append(file_path)
                self.track_list.addItem(os.path.basename(file_path))
                files_added = True
        
        if files_added:
            if hasattr(self, 'song_label'):
                self.song_label.setText("Archivos agregados a la lista de reproducción")
        else:
            if hasattr(self, 'song_label'):
                self.song_label.setText("No se agregaron archivos. Solo se aceptan archivos MP3, WAV y OGG")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())
