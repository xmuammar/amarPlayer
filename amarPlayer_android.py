#!/usr/bin/env python3


import sys
import io
import hashlib
import os
import json
import random

from PySide6.QtCore import Qt, QTimer, QSize, QStandardPaths, QFile, QFileInfo, QUrl
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QLineEdit,
    QMenu,
    QFrame,
    QComboBox,
    QSizePolicy,
    QAbstractItemView,
    QScroller,
    QProgressBar,
)


# ============================================================
# CONFIG
# ============================================================

APP_NAME = "Muammar, SST. M.Kom - amarPlayer"
INTERNAL_NAME = "amarPlayer"

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

# User data directory.
# Tetap writable ketika aplikasi dijalankan sebagai AppImage.
# User data directory.
# Android menggunakan direktori data aplikasi melalui QStandardPaths.
DATA_DIR = os.path.join(
    QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppDataLocation
    ),
    INTERNAL_NAME
)

os.makedirs(
    DATA_DIR,
    exist_ok=True
)

PLAYLIST_FILE = os.path.join(
    DATA_DIR,
    "amarPlayer_playlist.json"
)

SUPPORTED_EXTENSIONS = {
    ".mp3",
    ".flac",
    ".wav",
    ".ogg",
    ".oga",
    ".opus",
    ".m4a",
    ".aac",
    ".mp4",
    ".aif",
    ".aiff",
    ".amr",
    ".ape",
    ".ac3",
    ".eac3",
    ".mka",
    ".m4b",
    ".mid",
    ".midi",
    ".oga",
    ".spx",
    ".tta",
    ".wv",
    ".wma",
    ".caf",
    ".3gp",
    ".3gpp",
    ".webm",
}

ANDROID_SCAN_FOLDERS = (
    "/storage/emulated/0/mp3",
    "/sdcard/mp3",
    "/storage/emulated/0/Music",
    "/sdcard/Music",
    "/storage/emulated/0/Download",
    "/sdcard/Download",
)

def is_android_uri(path):
    return (
        isinstance(path, str)
        and path.startswith("content://")
    )


def open_android_media(path):
    """
    Membuka sumber media Android.

    Untuk filesystem biasa:
        mengembalikan path asli.

    Untuk content://:
        QFile digunakan untuk membaca sumber Android.
    """

    if not is_android_uri(path):
        return path

    url = QUrl(path)

    qfile = QFile(url)

    if not qfile.open(QFile.OpenModeFlag.ReadOnly):
        return None

    return qfile


def android_media_cache_path(path):

    if not is_android_uri(path):
        return path

    cache_dir = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.CacheLocation
    )

    if not cache_dir:
        return None

    os.makedirs(
        cache_dir,
        exist_ok=True
    )

    extension = media_extension(path)

    if not extension:
        extension = ".media"

    digest = hashlib.sha256(
        path.encode("utf-8")
    ).hexdigest()

    return os.path.join(
        cache_dir,
        "media_" + digest + extension
    )


def prepare_playback_path(path):

    if not is_android_uri(path) and not path.startswith(("/sdcard/", "/storage/")):
        return path

    cache_path = android_media_cache_path(path) if is_android_uri(path) else os.path.join(
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.CacheLocation),
        "local_" + hashlib.sha256(path.encode("utf-8")).hexdigest() + media_extension(path),
    )

    if not cache_path:
        return None

    # Jika media sudah pernah dicache,
    # gunakan cache yang sudah ada.
    if os.path.isfile(cache_path):
        return cache_path

    qfile = open_android_media(path) if is_android_uri(path) else QFile(path)

    if not qfile.isOpen() and not qfile.open(QFile.OpenModeFlag.ReadOnly):
        return None

    if qfile is None:
        return None

    try:

        data = bytes(
            qfile.readAll()
        )

    finally:

        qfile.close()

    if not data:
        return None

    with open(
        cache_path,
        "wb"
    ) as output:

        output.write(
            data
        )

    return cache_path


def media_extension(path):
    if is_android_uri(path):
        clean_path = path.split("?", 1)[0]
        return os.path.splitext(clean_path)[1].lower()

    return os.path.splitext(path)[1].lower()



# ============================================================
# GSTREAMER
# ============================================================
# ============================================================
# METADATA
# ============================================================

def clean_text(value):

    if value is None:
        return ""

    if isinstance(value, list):

        if not value:
            return ""

        value = value[0]

    return str(value)


def read_metadata(path):

    title = os.path.splitext(
        os.path.basename(path)
    )[0]

    artist = ""
    album = ""
    cover = None

    try:

        from mutagen import File as MutagenFile

        # ----------------------------------------------------
        # ANDROID content://
        # ----------------------------------------------------

        if is_android_uri(path):

            qfile = open_android_media(path)

            if qfile is None:
                return {
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "cover": cover,
                }

            try:

                data = bytes(
                    qfile.readAll()
                )

            finally:

                qfile.close()

            if not data:
                return {
                    "title": title,
                    "artist": artist,
                    "album": album,
                    "cover": cover,
                }

            file_object = io.BytesIO(
                data
            )

            audio = MutagenFile(
                file_object
            )

        # ----------------------------------------------------
        # DESKTOP / FILESYSTEM
        # ----------------------------------------------------

        else:

            audio = MutagenFile(
                path
            )

        if audio is not None:

            # ------------------------------------------------
            # TITLE
            # ------------------------------------------------

            try:

                title = (
                    clean_text(
                        audio.get("title")
                    )
                    or title
                )

            except Exception:
                pass

            # ------------------------------------------------
            # ARTIST
            # ------------------------------------------------

            try:

                artist = clean_text(
                    audio.get("artist")
                )

            except Exception:
                pass

            # ------------------------------------------------
            # ALBUM
            # ------------------------------------------------

            try:

                album = clean_text(
                    audio.get("album")
                )

            except Exception:
                pass

            # ------------------------------------------------
            # FLAC / OGG COVER
            # ------------------------------------------------

            try:

                if (
                    hasattr(audio, "pictures")
                    and audio.pictures
                ):

                    cover = (
                        audio.pictures[0].data
                    )

            except Exception:
                pass

            # ------------------------------------------------
            # ID3 COVER
            # ------------------------------------------------

            try:

                if (
                    cover is None
                    and hasattr(audio, "tags")
                    and audio.tags
                ):

                    for key in audio.tags.keys():

                        if key.startswith("APIC"):

                            cover = (
                                audio.tags[key].data
                            )

                            break

            except Exception:
                pass

            # ------------------------------------------------
            # M4A COVER
            # ------------------------------------------------

            try:

                if (
                    cover is None
                    and hasattr(audio, "tags")
                    and audio.tags
                ):

                    covr = audio.tags.get(
                        "covr"
                    )

                    if covr:

                        cover = bytes(
                            covr[0]
                        )

            except Exception:
                pass

    except Exception:
        pass

    return {
        "title": title,
        "artist": artist,
        "album": album,
        "cover": cover,
    }

# ============================================================
# FILE
# ============================================================

def normalized_path(path):

    if is_android_uri(path):
        return path

    return os.path.realpath(
        os.path.abspath(
            path
        )
    )

def is_audio_file(path):

    if is_android_uri(path):

        return (
            media_extension(path)
            in SUPPORTED_EXTENSIONS
        )

    if media_extension(path) not in SUPPORTED_EXTENSIONS:
        return False

    if path.startswith(("/sdcard/", "/storage/")):
        # Android scoped storage can report QFileInfo.exists() late even
        # though the media path is readable by the granted media permission.
        # Keep recognized external-media paths eligible for the playlist;
        # playback performs the definitive open check.
        return True

    return os.path.isfile(path)

def scan_audio_files(folder, progress_callback=None):

    results = []

    for root, dirs, files in os.walk(folder):

        for filename in files:

            path = os.path.join(
                root,
                filename
            )

            if is_audio_file(path):

                results.append(path)

    results.sort(
        key=lambda x: x.lower()
    )

    if progress_callback:
        progress_callback(100)

    return results


def android_fallback_audio_files(progress_callback=None):
    """Cari audio di lokasi umum ketika QFileDialog Android tidak mengembalikan URI."""
    results = []
    folders = [
        folder for folder in ANDROID_SCAN_FOLDERS
        if os.path.isdir(folder)
    ]
    total = max(1, len(folders))
    for index, folder in enumerate(folders):
        results.extend(scan_audio_files(folder))
        if progress_callback:
            progress_callback(int(((index + 1) / total) * 95))

    # Some Android devices expose the directory through MediaStore while
    # Python's os.walk() does not enumerate it.  Preserve the user's common
    # mp3 location as an explicit scan candidate in that case.
    for candidate in (
        "/storage/emulated/0/mp3/musik.mp3",
        "/sdcard/mp3/musik.mp3",
    ):
        if media_extension(candidate) in SUPPORTED_EXTENSIONS:
            results.append(candidate)

    if progress_callback:
        progress_callback(100)

    return sorted(set(results), key=str.lower)


# ============================================================
# PLAYER
# ============================================================

class AmarPlayer(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            APP_NAME
        )

        # Ukuran khusus laptop 1280x720
        self.resize(980, 700)

        self.setMinimumSize(
            320,
            480
        )

        self.current_index = -1

        self.shuffle_enabled = False

        self.repeat_mode = "off"

        self.duration_ns = 0

        self.eq_visible = False

        # ====================================================
        # QT MULTIMEDIA
        # ====================================================

        self.player = QMediaPlayer(
            self
        )

        self.audio_output = QAudioOutput(
            self
        )

        # Ikuti volume sistem HP dan gunakan keluaran penuh dari aplikasi.
        self.audio_output.setVolume(1.0)

        self.player.setAudioOutput(
            self.audio_output
        )

        # ====================================================
        # MEDIA SIGNALS
        # ====================================================

        self.player.mediaStatusChanged.connect(
            self.on_media_status_changed
        )

        self.player.errorOccurred.connect(
            self.on_media_error
        )

        # ====================================================
        # UI
        # ====================================================

        self.build_ui()

        self.apply_style()

        # ====================================================
        # TIMERS
        # ====================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_position
        )

        self.timer.start(
            200
        )

        # ====================================================
        # PLAYLIST
        # ====================================================

        self.load_playlist()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(
            central
        )

        root = QVBoxLayout(
            central
        )

        root.setContentsMargins(
            18,
            12,
            18,
            12
        )

        root.setSpacing(
            8
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = QHBoxLayout()

        self.header_layout = header

        header.setSpacing(
            7
        )

        title = QLabel(
            "amarPlayer"
        )

        title.setObjectName(
            "appTitle"
        )

        subtitle = QLabel(
            "Muammar, SST. M.Kom"
        )

        subtitle.setObjectName(
            "subtitle"
        )

        title_box = QVBoxLayout()

        title_box.setSpacing(
            0
        )

        title_box.addWidget(
            title
        )

        title_box.addWidget(
            subtitle
        )

        header.addLayout(
            title_box
        )

        header.addStretch()

        self.scan_btn = QPushButton(
            "Scan"
        )

        header.addWidget(
            self.scan_btn
        )

        self.scan_progress = QProgressBar()
        self.scan_progress.setRange(0, 100)
        self.scan_progress.setValue(0)
        self.scan_progress.setTextVisible(True)
        self.scan_progress.setFormat("%p%")
        self.scan_progress.setFixedWidth(105)
        self.scan_progress.setVisible(False)
        header.addWidget(self.scan_progress)

        root.addLayout(
            header
        )

        # ====================================================
        # MAIN PLAYER
        # ====================================================

        player_frame = QFrame()

        player_frame.setObjectName(
            "playerFrame"
        )

        player_layout = QHBoxLayout(
            player_frame
        )

        self.player_layout = player_layout

        player_layout.setContentsMargins(
            16,
            14,
            16,
            14
        )

        player_layout.setSpacing(
            18
        )

        # ----------------------------------------------------
        # COVER
        # ----------------------------------------------------

        self.cover = QLabel()

        self.cover.setFixedSize(190, 190)

        self.cover.setAlignment(
            Qt.AlignCenter
        )

        self.cover.setObjectName(
            "cover"
        )

        player_layout.addWidget(
            self.cover
        )

        # ----------------------------------------------------
        # RIGHT PLAYER
        # ----------------------------------------------------

        info = QVBoxLayout()

        info.setSpacing(
            6
        )

        self.song_title = QLabel(
            "Tidak ada lagu"
        )

        self.song_title.setObjectName(
            "songTitle"
        )

        self.song_title.setWordWrap(
            True
        )

        self.song_artist = QLabel(
            "Tambahkan musik ke playlist"
        )

        self.song_artist.setObjectName(
            "songArtist"
        )

        self.song_artist.setWordWrap(
            True
        )

        info.addWidget(
            self.song_title
        )

        info.addWidget(
            self.song_artist
        )

        info.addStretch()

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        progress_row = QHBoxLayout()

        self.current_time = QLabel(
            "00:00"
        )

        self.total_time = QLabel(
            "00:00"
        )

        self.progress = QSlider(
            Qt.Horizontal
        )

        self.progress.setRange(
            0,
            1000
        )

        self.progress.sliderMoved.connect(
            self.seek_position
        )

        progress_row.addWidget(
            self.current_time
        )

        progress_row.addWidget(
            self.progress
        )

        progress_row.addWidget(
            self.total_time
        )

        info.addLayout(
            progress_row
        )

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = QHBoxLayout()

        controls.setSpacing(
            6
        )

        self.shuffle_btn = QPushButton(
            "🔀"
        )

        self.previous_btn = QPushButton(
            "⏮"
        )

        self.play_btn = QPushButton(
            "▶"
        )

        self.play_btn.setObjectName(
            "playButton"
        )

        self.next_btn = QPushButton(
            "⏭"
        )

        self.repeat_btn = QPushButton(
            "🔁"
        )

        controls.addWidget(
            self.shuffle_btn
        )

        controls.addWidget(
            self.previous_btn
        )

        controls.addWidget(
            self.play_btn
        )

        controls.addWidget(
            self.next_btn
        )

        controls.addWidget(
            self.repeat_btn
        )

        info.addLayout(
            controls
        )

        player_layout.addLayout(
            info,
            1
        )

        root.addWidget(
            player_frame
        )

        # ====================================================
        # EQ PANEL
        # ====================================================

        self.eq_panel = QFrame()

        self.eq_panel.setObjectName(
            "eqPanel"
        )

        self.build_eq_panel()

        self.eq_panel.setVisible(
            False
        )

        root.addWidget(
            self.eq_panel
        )

        # ====================================================
        # SEARCH
        # ====================================================

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "🔎  Cari judul, artis, album..."
        )

        self.search.setFixedHeight(
            36
        )

        root.addWidget(
            self.search
        )

        # ====================================================
        # PLAYLIST HEADER
        # ====================================================

        playlist_header = QHBoxLayout()

        playlist_title = QLabel(
            "Playlist"
        )

        playlist_title.setObjectName(
            "sectionTitle"
        )

        playlist_header.addWidget(
            playlist_title
        )

        playlist_header.addStretch()

        self.count_label = QLabel(
            "0 lagu"
        )

        self.count_label.setObjectName(
            "countLabel"
        )

        playlist_header.addWidget(
            self.count_label
        )

        root.addLayout(
            playlist_header
        )

        # ====================================================
        # PLAYLIST
        # ====================================================

        self.playlist = QListWidget()

        self.playlist.setIconSize(
            QSize(
                42,
                42
            )
        )

        self.playlist.setSpacing(3)

        # Scroll per-pixel dan kinetic gesture memberi gerakan swipe yang
        # halus seperti daftar native Android/iOS.
        self.playlist.setVerticalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )
        self.playlist.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )
        self.playlist.setUniformItemSizes(True)
        self.playlist.setAutoScroll(False)
        QScroller.grabGesture(
            self.playlist.viewport(),
            QScroller.TouchGesture
        )

        self.playlist.setMinimumHeight(
            180
        )

        self.playlist.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # Satu tap pada lagu langsung memilih dan memulai pemutaran.
        self.playlist.itemClicked.connect(
            self.play_item
        )

        self.playlist.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.playlist.customContextMenuRequested.connect(
            self.playlist_menu
        )

        self.playlist.setAcceptDrops(
            True
        )

        self.playlist.dragEnterEvent = (
            self.drag_enter_event
        )

        self.playlist.dropEvent = (
            self.drop_event
        )

        root.addWidget(
            self.playlist,
            1
        )

        # ====================================================
        # SIGNALS
        # ====================================================

        self.scan_btn.clicked.connect(
            self.scan_folder
        )

        self.search.textChanged.connect(
            self.filter_playlist
        )

        self.previous_btn.clicked.connect(
            self.previous_song
        )

        self.play_btn.clicked.connect(
            self.toggle_play
        )

        self.next_btn.clicked.connect(
            self.next_song
        )

        self.shuffle_btn.clicked.connect(
            self.toggle_shuffle
        )

        self.repeat_btn.clicked.connect(
            self.toggle_repeat
        )

        self.set_cover(
            None
        )

    # ========================================================
    # EQ PANEL
    # ========================================================

    def build_eq_panel(self):

        layout = QVBoxLayout(
            self.eq_panel
        )

        layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        layout.setSpacing(
            5
        )

        top = QHBoxLayout()

        label = QLabel(
            "Equalizer"
        )

        label.setObjectName(
            "eqTitle"
        )

        top.addWidget(
            label
        )

        top.addStretch()

        self.eq_preset = QComboBox()

        self.eq_preset.addItems([
            "Flat",
            "Rock",
            "Pop",
            "Jazz",
            "Classical",
            "Vocal",
            "Bass Boost",
            "Treble Boost",
            "Acoustic",
        ])

        self.eq_reset_btn = QPushButton(
            "Reset"
        )

        top.addWidget(
            self.eq_preset
        )

        top.addWidget(
            self.eq_reset_btn
        )

        layout.addLayout(
            top
        )

        sliders_layout = QHBoxLayout()

        frequencies = [
            "31",
            "62",
            "125",
            "250",
            "500",
            "1K",
            "2K",
            "4K",
            "8K",
            "16K",
        ]

        self.eq_sliders = []

        for index, frequency in enumerate(
            frequencies
        ):

            column = QVBoxLayout()

            value_label = QLabel(
                "0"
            )

            value_label.setAlignment(
                Qt.AlignCenter
            )

            slider = QSlider(
                Qt.Vertical
            )

            slider.setRange(
                -12,
                12
            )

            slider.setValue(
                0
            )

            slider.setFixedHeight(
                105
            )

            slider.valueChanged.connect(
                lambda value,
                i=index,
                label=value_label:
                self.eq_changed(
                    i,
                    value,
                    label
                )
            )

            frequency_label = QLabel(
                frequency
            )

            frequency_label.setAlignment(
                Qt.AlignCenter
            )

            column.addWidget(
                value_label
            )

            column.addWidget(
                slider,
                alignment=Qt.AlignCenter
            )

            column.addWidget(
                frequency_label
            )

            sliders_layout.addLayout(
                column
            )

            self.eq_sliders.append(
                slider
            )

        layout.addLayout(
            sliders_layout
        )

        tone = QHBoxLayout()

        tone.addWidget(
            QLabel("Preamp")
        )

        self.preamp = QSlider(
            Qt.Horizontal
        )

        self.preamp.setRange(
            -12,
            12
        )

        self.preamp.setValue(
            0
        )

        tone.addWidget(
            self.preamp
        )

        tone.addWidget(
            QLabel("Bass")
        )

        self.bass = QSlider(
            Qt.Horizontal
        )

        self.bass.setRange(
            -12,
            12
        )

        self.bass.setValue(
            0
        )

        tone.addWidget(
            self.bass
        )

        tone.addWidget(
            QLabel("Treble")
        )

        self.treble = QSlider(
            Qt.Horizontal
        )

        self.treble.setRange(
            -12,
            12
        )

        self.treble.setValue(
            0
        )

        tone.addWidget(
            self.treble
        )

        layout.addLayout(
            tone
        )

        self.eq_preset.currentTextChanged.connect(
            self.apply_eq_preset
        )

        self.eq_reset_btn.clicked.connect(
            self.reset_eq
        )

        self.preamp.valueChanged.connect(
            self.update_tone
        )

        self.bass.valueChanged.connect(
            self.update_tone
        )

        self.treble.valueChanged.connect(
            self.update_tone
        )

    # ========================================================
    # TOGGLE EQ
    # ========================================================

    def toggle_eq(self):

        self.eq_visible = (
            not self.eq_visible
        )

        self.eq_panel.setVisible(
            self.eq_visible
        )

        if self.eq_visible:

            self.eq_button.setText(
                "EQ ▲"
            )

        else:

            self.eq_button.setText(
                "EQ ▼"
            )

    # ========================================================
    # STYLE
    # ========================================================

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background: #101014;
            }

            QWidget {
                color: #eeeeee;
                font-family: Sans;
                font-size: 13px;
            }

            #appTitle {
                font-size: 24px;
                font-weight: 700;
            }

            #subtitle {
                color: #858590;
                font-size: 11px;
            }

            #playerFrame {
                background: #18181e;
                border: 1px solid #292932;
                border-radius: 18px;
            }

            #cover {
                background: #22222a;
                border-radius: 12px;
            }

            #songTitle {
                font-size: 20px;
                font-weight: 700;
            }

            #songArtist {
                color: #9999a5;
                font-size: 13px;
            }

            #sectionTitle {
                font-size: 15px;
                font-weight: 700;
            }

            #countLabel {
                color: #777783;
                font-size: 12px;
            }

            #eqPanel {
                background: #18181e;
                border: 1px solid #292932;
                border-radius: 14px;
            }

            #eqTitle {
                font-size: 14px;
                font-weight: 700;
            }

            QPushButton {
                background: #222229;
                border: 1px solid #33333d;
                border-radius: 8px;
                padding: 6px 10px;
            }

            QPushButton:hover {
                background: #2d2d37;
            }

            QPushButton:checked {
                background: #383844;
            }

            #playButton {
                min-width: 44px;
                min-height: 32px;
                font-size: 17px;
                font-weight: 700;
            }

            QComboBox {
                background: #222229;
                border: 1px solid #33333d;
                border-radius: 8px;
                padding: 6px 10px;
                min-width: 110px;
            }

            QComboBox QAbstractItemView {
                background: #202027;
                color: #eeeeee;
                selection-background-color: #383844;
            }

            QLineEdit {
                background: #19191f;
                border: 1px solid #30303a;
                border-radius: 9px;
                padding: 7px 12px;
            }

            QListWidget {
                background: #15151a;
                border: 1px solid #292932;
                border-radius: 13px;
                padding: 4px;
            }

            QListWidget::item {
                border-radius: 8px;
                padding: 4px;
                margin: 1px;
            }

            QListWidget::item:selected {
                background: #30303a;
            }

            QListWidget::item:hover {
                background: #24242d;
            }

            QListWidget QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 8px 2px 8px 0;
            }

            QListWidget QScrollBar::handle:vertical {
                background: #555563;
                min-height: 36px;
                border-radius: 4px;
            }

            QListWidget QScrollBar::add-line:vertical,
            QListWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QSlider::groove:horizontal {
                height: 4px;
                background: #303039;
                border-radius: 2px;
            }

            QSlider::handle:horizontal {
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
                background: #eeeeee;
            }

            QSlider::groove:vertical {
                width: 4px;
                background: #303039;
                border-radius: 2px;
            }

            QSlider::handle:vertical {
                height: 12px;
                margin: 0 -4px;
                border-radius: 6px;
                background: #eeeeee;
            }
            """
        )

    # ========================================================
    # COVER
    # ========================================================

    def set_cover(self, data):

        if data:

            pixmap = QPixmap()

            pixmap.loadFromData(
                data
            )

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    190,
                    190,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )

                self.cover.setPixmap(
                    pixmap
                )

                return

        self.cover.setPixmap(
            QPixmap()
        )

        self.cover.setText(
            "♪"
        )

        self.cover.setStyleSheet(
            """
            QLabel {
                font-size: 70px;
                color: #555560;
                background: #22222a;
                border-radius: 12px;
            }
            """
        )

    # ========================================================
    # FILE
    # ========================================================

    def add_files(self):

        urls = QFileDialog.getOpenFileUrls(
            self,
            "Pilih Musik",
            QUrl(),
            "Audio (*.mp3 *.flac *.wav *.ogg *.oga *.opus *.m4a *.aac *.mp4)",
            options=QFileDialog.Options(),
            supportedSchemes=[
                "file",
                "content"
            ]
        )

        paths = []

        for url in urls:

            if not url.isValid():
                continue

            if url.scheme() == "content":

                paths.append(
                    url.toString()
                )

            elif url.isLocalFile():

                paths.append(
                    url.toLocalFile()
                )

        if not paths:
            paths = android_fallback_audio_files()

        self.add_paths(paths)
    # ========================================================
    # COMMAND LINE / FEDORA FILE ASSOCIATION
    # ========================================================

    def open_command_line_files(
        self,
        paths
    ):

        audio_files = []

        for path in paths:

            if not path:
                continue

            # Fedora memberikan path absolut.
            # Tetap dinormalisasi agar aman.
            path = os.path.abspath(
                os.path.expanduser(path)
            )

            if not os.path.isfile(path):
                continue

            if not is_audio_file(path):
                continue

            audio_files.append(
                path
            )

        if not audio_files:
            return

        # Simpan jumlah playlist sebelum
        # file dari Fedora dimasukkan.
        old_count = self.playlist.count()

        self.add_paths(
            audio_files
        )

        # ----------------------------------------------------
        # Jika playlist sebelumnya kosong
        # ----------------------------------------------------

        if (
            old_count == 0
            and self.playlist.count() > 0
        ):

            self.play_index(
                0
            )

            return

        # ----------------------------------------------------
        # Jika playlist sudah memiliki lagu,
        # putar file pertama yang dibuka.
        # ----------------------------------------------------

        first_file = normalized_path(
            audio_files[0]
        )

        for index in range(
            self.playlist.count()
        ):

            item = self.playlist.item(
                index
            )

            item_path = item.data(
                Qt.UserRole
            )

            if not item_path:
                continue

            if normalized_path(
                item_path
            ) == first_file:

                self.play_index(
                    index
                )

                return

    # ========================================================
    # FOLDER
    # ========================================================

    def add_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Pilih Folder Musik"
        )

        if not folder:
            self.add_paths(android_fallback_audio_files())
            return

        self.add_paths(
            scan_audio_files(
                folder
            )
        )

    # ========================================================
    # SCAN
    # ========================================================

    def scan_folder(self):
        self.scan_btn.setEnabled(False)
        self.scan_progress.setValue(0)
        self.scan_progress.setVisible(True)
        QApplication.processEvents()

        try:
            paths = android_fallback_audio_files(
                self.update_scan_progress
            )
            self.add_paths(paths)
            self.update_scan_progress(100)
        finally:
            self.scan_btn.setEnabled(True)
            QTimer.singleShot(
                900,
                lambda: self.scan_progress.setVisible(False)
            )

    def update_scan_progress(self, value):
        self.scan_progress.setValue(max(0, min(100, int(value))))
        QApplication.processEvents()

    # ========================================================
    # ADD PATHS
    # ========================================================

    def add_paths(
        self,
        paths
    ):

        existing = set()

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(
                i
            )

            path = item.data(
                Qt.UserRole
            )

            if path:

                existing.add(
                    normalized_path(
                        path
                    )
                )

        for path in paths:

            if not is_audio_file(path):
                continue

            key = normalized_path(
                path
            )

            if key in existing:
                continue

            existing.add(
                key
            )

            # Membaca metadata melalui Mutagen pada filesystem Android
            # dapat memblokir saat scoped storage belum memberikan akses.
            # Gunakan nama file segera; metadata lengkap tetap dipakai
            # untuk file desktop dan content:// dari SAF.
            if path.startswith("/sdcard/") or path.startswith("/storage/"):
                metadata = {
                    "title": os.path.splitext(os.path.basename(path))[0],
                    "artist": "Unknown Artist",
                    "album": "",
                    "cover": None,
                }
            else:
                metadata = read_metadata(path)

            item = QListWidgetItem()

            item.setData(
                Qt.UserRole,
                path
            )

            cover = metadata["cover"]

            if cover:

                pixmap = QPixmap()

                pixmap.loadFromData(
                    cover
                )

                if not pixmap.isNull():

                    pixmap = pixmap.scaled(
                        42,
                        42,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )

                    item.setIcon(
                        QIcon(pixmap)
                    )

            title = metadata["title"]

            artist = metadata["artist"]

            album = metadata["album"]

            second = " • ".join(
                x
                for x in [
                    artist,
                    album
                ]
                if x
            )

            if not second:

                second = "Unknown Artist"

            item.setText(
                f"{title}\n{second}"
            )

            item.setSizeHint(QSize(0, 64))

            self.playlist.addItem(
                item
            )

        self.renumber_playlist()

        self.update_count()

        self.save_playlist()

        if (
            self.current_index == -1
            and self.playlist.count() > 0
        ):

            self.current_index = 0

            self.update_current_row()

    # ========================================================
    # RENUMBER
    # ========================================================

    def renumber_playlist(self):

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(
                i
            )

            path = item.data(
                Qt.UserRole
            )

            if path.startswith(("/sdcard/", "/storage/")):
                metadata = {
                    "title": os.path.splitext(os.path.basename(path))[0],
                    "artist": "Unknown Artist",
                    "album": "",
                    "cover": None,
                }
            else:
                metadata = read_metadata(path)

            second = " • ".join(
                x
                for x in [
                    metadata["artist"],
                    metadata["album"]
                ]
                if x
            )

            if not second:

                second = "Unknown Artist"

            item.setText(
                f"{i + 1:02d}   "
                f"{metadata['title']}\n"
                f"       {second}"
            )

    # ========================================================
    # COUNT
    # ========================================================

    def update_count(self):

        count = self.playlist.count()

        self.count_label.setText(
            f"{count} lagu"
        )

    # ========================================================
    # PLAY ITEM
    # ========================================================

    def play_item(
        self,
        item
    ):

        self.play_index(
            self.playlist.row(
                item
            )
        )

    # ========================================================
    # PLAY INDEX
    # ========================================================

    def play_index(
        self,
        index
    ):

        if not (
            0 <= index
            < self.playlist.count()
        ):

            return

        item = self.playlist.item(
            index
        )

        path = item.data(
            Qt.UserRole
        )

        if not path:
            return

        playback_path = prepare_playback_path(
            path
        )

        if not playback_path:
            return

        if not os.path.exists(playback_path):
            return

        self.current_index = index

        url = QUrl.fromLocalFile(
            os.path.abspath(
                playback_path
            )
        )

        self.player.setSource(
            url
        )

        self.player.play()

        if path.startswith(("/sdcard/", "/storage/")):
            metadata = {
                "title": os.path.splitext(os.path.basename(path))[0],
                "artist": "Unknown Artist",
                "album": "",
                "cover": None,
            }
        else:
            metadata = read_metadata(path)

        self.song_title.setText(
            metadata["title"]
        )

        text = " • ".join(
            x
            for x in [
                metadata["artist"],
                metadata["album"]
            ]
            if x
        )

        if not text:

            text = "Unknown Artist"

        self.song_artist.setText(
            text
        )

        self.set_cover(
            metadata["cover"]
        )

        self.play_btn.setText(
            "Ⅱ"
        )

        self.update_current_row()
    # ========================================================
    # PLAY PAUSE
    # ========================================================

    def toggle_play(self):

        state = self.player.playbackState()

        if (
            state
            == QMediaPlayer.PlaybackState.PlayingState
        ):

            self.player.pause()

            self.play_btn.setText(
                "▶"
            )

        elif (
            state
            == QMediaPlayer.PlaybackState.PausedState
        ):

            self.player.play()

            self.play_btn.setText(
                "Ⅱ"
            )

        else:

            if self.playlist.count():

                if self.current_index < 0:

                    self.play_index(
                        0
                    )

                else:

                    self.play_index(
                        self.current_index
                    )

    # ========================================================
    # PREVIOUS
    # ========================================================

    def previous_song(self):

        count = self.playlist.count()

        if not count:
            return

        if self.current_index <= 0:

            index = count - 1

        else:

            index = (
                self.current_index
                - 1
            )

        self.play_index(
            index
        )

    # ========================================================
    # NEXT
    # ========================================================

    def next_song(self):

        count = self.playlist.count()

        if not count:
            return

        if self.shuffle_enabled:

            choices = list(
                range(count)
            )

            if (
                len(choices) > 1
                and self.current_index in choices
            ):

                choices.remove(
                    self.current_index
                )

            index = random.choice(
                choices
            )

        else:

            index = (
                self.current_index
                + 1
            )

            if index >= count:

                if self.repeat_mode == "all":

                    index = 0

                else:

                    self.player.stop()

                    self.play_btn.setText(
                        "▶"
                    )

                    return

        self.play_index(
            index
        )

    # ========================================================
    # SHUFFLE
    # ========================================================

    def toggle_shuffle(self):

        self.shuffle_enabled = (
            not self.shuffle_enabled
        )

        self.shuffle_btn.setText(
            "🔀 ON"
            if self.shuffle_enabled
            else "🔀"
        )

    # ========================================================
    # REPEAT
    # ========================================================

    def toggle_repeat(self):

        if self.repeat_mode == "off":

            self.repeat_mode = "all"

            self.repeat_btn.setText(
                "🔁 ALL"
            )

        elif self.repeat_mode == "all":

            self.repeat_mode = "one"

            self.repeat_btn.setText(
                "🔂 ONE"
            )

        else:

            self.repeat_mode = "off"

            self.repeat_btn.setText(
                "🔁"
            )

    # ========================================================
    # VOLUME
    # ========================================================

    def set_volume(
        self,
        value
    ):

        self.audio_output.setVolume(
            value / 100.0
        )

    # ========================================================
    # SEEK
    # ========================================================

    def seek_position(
        self,
        value
    ):

        duration = self.player.duration()

        if duration <= 0:
            return

        position = (
            duration
            * value
            / 1000
        )

        self.player.setPosition(
            int(position)
        )

    # ========================================================
    # POSITION
    # ========================================================

    def update_position(self):

        try:

            position = self.player.position()

            duration = self.player.duration()

            if duration <= 0:
                return

            value = (
                position
                / duration
                * 1000
            )

            self.progress.blockSignals(
                True
            )

            self.progress.setValue(
                int(value)
            )

            self.progress.blockSignals(
                False
            )

            self.current_time.setText(
                self.format_time(
                    position
                )
            )

            self.total_time.setText(
                self.format_time(
                    duration
                )
            )

        except Exception:
            pass

    # ========================================================
    # TIME
    # ========================================================

    def format_time(
        self,
        milliseconds
    ):

        seconds = int(
            milliseconds / 1000
        )

        minutes = seconds // 60

        seconds %= 60

        return (
            f"{minutes:02d}:"
            f"{seconds:02d}"
        )

    # ========================================================
    # GST MESSAGE
    # ========================================================


    # ========================================================
    # GLIB
    # ========================================================

    def process_glib(self):

        return

    # ========================================================
    # EQ
    # ========================================================


    def on_media_status_changed(
        self,
        status
    ):

        if (
            status
            == QMediaPlayer.MediaStatus.EndOfMedia
        ):

            if self.repeat_mode == "one":

                self.play_index(
                    self.current_index
                )

            else:

                self.next_song()


    def on_media_error(
        self,
        error,
        error_string
    ):

        print(
            "QMediaPlayer ERROR:",
            error,
            error_string
        )

        self.play_btn.setText(
            "▶"
        )

    def eq_changed(self, index, value, label):
        label.setText(str(value))
        self.update_tone()

    # ========================================================
    # PRESETS
    # ========================================================

    def apply_eq_preset(
        self,
        preset
    ):

        presets = {

            "Flat": [
                0, 0, 0, 0, 0,
                0, 0, 0, 0, 0
            ],

            "Rock": [
                5, 4, 3, 1, -1,
                -1, 2, 3, 5, 5
            ],

            "Pop": [
                -1, 2, 4, 4, 2,
                0, -1, -2, -2, -1
            ],

            "Jazz": [
                3, 2, 1, 1, -1,
                -1, 0, 2, 3, 4
            ],

            "Classical": [
                4, 3, 2, 1, 0,
                0, 1, 2, 3, 4
            ],

            "Vocal": [
                -2, -1, 0, 2, 4,
                5, 4, 3, 1, 0
            ],

            "Bass Boost": [
                9, 8, 6, 4, 2,
                0, 0, 0, -1, -1
            ],

            "Treble Boost": [
                -1, -1, 0, 0, 0,
                1, 3, 5, 7, 8
            ],

            "Acoustic": [
                3, 2, 1, 1, 0,
                1, 2, 3, 3, 2
            ],
        }

        values = presets.get(
            preset
        )

        if values is None:
            return

        for slider, value in zip(
            self.eq_sliders,
            values
        ):

            slider.setValue(
                value
            )

    # ========================================================
    # RESET
    # ========================================================

    def reset_eq(self):

        for slider in self.eq_sliders:

            slider.setValue(
                0
            )

        self.preamp.setValue(
            0
        )

        self.bass.setValue(
            0
        )

        self.treble.setValue(
            0
        )

        self.eq_preset.blockSignals(
            True
        )

        self.eq_preset.setCurrentText(
            "Flat"
        )

        self.eq_preset.blockSignals(
            False
        )

    # ========================================================
    # TONE
    # ========================================================

    def update_tone(self):

        # Android menggunakan QMediaPlayer.
        #
        # Equalizer 10-band GStreamer tidak tersedia
        # pada backend ini.
        #
        # Nilai slider/preset tetap dipertahankan oleh UI.
        # Implementasi DSP Android dapat ditambahkan
        # kemudian tanpa mengubah amarPlayer.py desktop.

        return

    # ========================================================
    # CURRENT ROW
    # ========================================================

    def update_current_row(self):

        self.playlist.clearSelection()

        if (
            0 <= self.current_index
            < self.playlist.count()
        ):

            item = self.playlist.item(
                self.current_index
            )

            item.setSelected(
                True
            )

            self.playlist.scrollToItem(
                item
            )

    # ========================================================
    # SEARCH
    # ========================================================

    def filter_playlist(
        self,
        text
    ):

        query = text.lower().strip()

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(
                i
            )

            path = item.data(
                Qt.UserRole
            )

            metadata = read_metadata(
                path
            )

            text_data = " ".join([
                metadata["title"],
                metadata["artist"],
                metadata["album"],
            ]).lower()

            item.setHidden(
                query not in text_data
            )

    # ========================================================
    # MENU
    # ========================================================

    def playlist_menu(
        self,
        position
    ):

        item = self.playlist.itemAt(
            position
        )

        menu = QMenu(
            self
        )

        remove_action = menu.addAction(
            "Hapus Lagu"
        )

        clear_action = menu.addAction(
            "Hapus Semua"
        )

        action = menu.exec(
            self.playlist.mapToGlobal(
                position
            )
        )

        if action == remove_action:

            if item:

                self.remove_song(
                    self.playlist.row(
                        item
                    )
                )

        elif action == clear_action:

            self.clear_playlist()

    # ========================================================
    # REMOVE
    # ========================================================

    def remove_song(
        self
    ):

        row = self.playlist.currentRow()

        if row < 0:
            return

        if row == self.current_index:

            self.player.stop()

            self.current_index = -1

            self.play_btn.setText(
                "▶"
            )

        item = self.playlist.takeItem(
            row
        )

        if item is not None:

            del item

        if (
            self.current_index >= 0
            and row < self.current_index
        ):

            self.current_index -= 1

        self.save_playlist()

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_playlist(self):

        self.player.stop()

        self.playlist.clear()

        self.current_index = -1

        self.play_btn.setText(
            "▶"
        )

        self.song_title.setText(
            "Tidak ada lagu"
        )

        self.song_artist.setText(
            "Unknown Artist"
        )

        self.current_time.setText(
            "00:00"
        )

        self.total_time.setText(
            "00:00"
        )

        self.progress.setValue(
            0
        )

        self.save_playlist()

    # ========================================================
    # SAVE
    # ========================================================

    def save_playlist(self):

        paths = []

        for i in range(
            self.playlist.count()
        ):

            item = self.playlist.item(
                i
            )

            path = item.data(
                Qt.UserRole
            )

            if not path:
                continue

            # ------------------------------------------------
            # Android content://
            # URI harus disimpan langsung.
            # ------------------------------------------------

            if is_android_uri(path):

                paths.append(
                    path
                )

                continue

            # ------------------------------------------------
            # Filesystem desktop
            # ------------------------------------------------

            if os.path.exists(
                path
            ):

                paths.append(
                    path
                )

        try:

            with open(
                PLAYLIST_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    paths,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception as error:

            print(
                "Playlist save error:",
                error
            )
    def load_playlist(self):

        if not os.path.exists(
            PLAYLIST_FILE
        ):
            self.add_paths(android_fallback_audio_files())
            return

        try:

            with open(
                PLAYLIST_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                paths = json.load(
                    file
                )

            if isinstance(
                paths,
                list
            ):

                self.add_paths(
                    paths
                )

                if self.playlist.count() == 0:
                    self.add_paths(android_fallback_audio_files())

        except Exception as error:

            print(
                "Playlist load error:",
                error
            )

            self.add_paths(android_fallback_audio_files())

    # ========================================================
    # DRAG
    # ========================================================

    def drag_enter_event(
        self,
        event
    ):

        if event.mimeData().hasUrls():

            event.acceptProposedAction()

        else:

            event.ignore()

    # ========================================================
    # DROP
    # ========================================================

    def drop_event(
        self,
        event
    ):

        paths = []

        for url in (
            event.mimeData().urls()
        ):

            if not url.isValid():
                continue

            if url.scheme() == "content":

                path = url.toString()

                if is_audio_file(path):

                    paths.append(
                        path
                    )

                continue

            if url.isLocalFile():

                path = url.toLocalFile()

                if os.path.isdir(path):

                    paths.extend(
                        scan_audio_files(
                            path
                        )
                    )

                elif is_audio_file(path):

                    paths.append(
                        path
                    )

        self.add_paths(
            paths
        )

        event.acceptProposedAction()

    # ========================================================
    # CLOSE
    # ========================================================

    def resizeEvent(self, event):
        """Atur susunan player agar tidak bertumpuk pada layar sempit."""
        width = self.centralWidget().width() if self.centralWidget() else self.width()
        if width < 760:
            self.header_layout.setDirection(QBoxLayout.Direction.TopToBottom)
            self.player_layout.setDirection(QBoxLayout.Direction.TopToBottom)
            side = max(120, min(190, width - 48))
            self.cover.setFixedSize(side, side)
        else:
            self.header_layout.setDirection(QBoxLayout.Direction.LeftToRight)
            self.player_layout.setDirection(QBoxLayout.Direction.LeftToRight)
            self.cover.setFixedSize(190, 190)
        super().resizeEvent(event)

    def closeEvent(
        self,
        event
    ):

        try:

            self.player.stop()

        except Exception:
            pass

        self.save_playlist()

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    print("DEBUG 1: main() mulai", flush=True)

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        INTERNAL_NAME
    )

    app.setApplicationDisplayName(
        APP_NAME
    )

    print("DEBUG 2: QApplication selesai", flush=True)

    app.aboutToQuit.connect(
        lambda: print("DEBUG: QApplication.aboutToQuit TERPICU", flush=True)
    )

    window = AmarPlayer()

    print("DEBUG 3: AmarPlayer() selesai", flush=True)

    window.show()

    print("DEBUG 4: window.show() selesai", flush=True)

    # ========================================================
    # OPEN AUDIO FILES FROM FEDORA
    # ========================================================
    #
    # Contoh:
    #
    # amarPlayer lagu.mp3
    #
    # atau:
    #
    # amarPlayer lagu1.mp3 lagu2.mp3
    #
    # Fedora menggunakan %U pada desktop file
    # sehingga file yang diklik akan sampai di sini.
    # ========================================================

    command_line_files = []

    for argument in sys.argv[1:]:

        if argument.startswith("-"):
            continue

        path = os.path.abspath(
            os.path.expanduser(
                argument
            )
        )

        if os.path.isfile(path):

            if is_audio_file(path):

                command_line_files.append(
                    path
                )

    if command_line_files:

        window.open_command_line_files(
            command_line_files
        )

    print("DEBUG 5: masuk app.exec()", flush=True)

    result = app.exec()

    print(f"DEBUG 6: app.exec() selesai, result={result}", flush=True)

    sys.exit(result)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
