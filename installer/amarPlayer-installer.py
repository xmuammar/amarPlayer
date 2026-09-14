#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)

from PySide6.QtCore import Qt


INSTALL_DIR = os.path.expanduser(
    "~/.local/opt/amarPlayer"
)

APP_DIR = os.path.expanduser(
    "~/.local/share/applications"
)

ICON_DIR = os.path.expanduser(
    "~/.local/share/icons/hicolor/256x256/apps"
)

APPIMAGE = os.path.join(
    INSTALL_DIR,
    "amarPlayer-Linux-aarch64.AppImage"
)

DESKTOP = os.path.join(
    APP_DIR,
    "amarPlayer.desktop"
)

ICON = os.path.join(
    ICON_DIR,
    "amarPlayer.png"
)

MIME_TYPES = [
    "audio/mpeg",
    "audio/flac",
    "audio/x-wav",
    "audio/ogg",
    "audio/x-vorbis+ogg",
    "audio/opus",
    "audio/mp4",
    "audio/aac",
    "audio/x-m4a",
]


def run(cmd):

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )


def install():

    here = os.path.dirname(
        os.path.abspath(__file__)
    )

    source = os.path.join(
        here,
        "amarPlayer-Linux-aarch64.AppImage"
    )

    icon_source = os.path.join(
        here,
        "amarPlayer.png"
    )

    if not os.path.isfile(source):

        QMessageBox.critical(
            None,
            "amarPlayer",
            "Payload amarPlayer tidak ditemukan."
        )

        return

    os.makedirs(
        INSTALL_DIR,
        exist_ok=True
    )

    os.makedirs(
        APP_DIR,
        exist_ok=True
    )

    os.makedirs(
        ICON_DIR,
        exist_ok=True
    )

    shutil.copy2(
        source,
        APPIMAGE
    )

    os.chmod(
        APPIMAGE,
        0o755
    )

    if os.path.isfile(icon_source):

        shutil.copy2(
            icon_source,
            ICON
        )

    with open(
        DESKTOP,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"""[Desktop Entry]
Name=amarPlayer
Comment=Modern Music Player
Exec={APPIMAGE} %U
Icon=amarPlayer
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Player;
StartupWMClass=amarPlayer
MimeType=audio/mpeg;audio/flac;audio/x-wav;audio/ogg;audio/x-vorbis+ogg;audio/opus;audio/mp4;audio/aac;audio/x-m4a;
"""
        )

    os.chmod(
        DESKTOP,
        0o755
    )

    for mime in MIME_TYPES:

        run(
            [
                "xdg-mime",
                "default",
                "amarPlayer.desktop",
                mime
            ]
        )

    run(
        [
            "update-desktop-database",
            APP_DIR
        ]
    )

    QMessageBox.information(
        None,
        "amarPlayer",
        "amarPlayer berhasil di-install."
    )


app = QApplication(sys.argv)

window = QWidget()

window.setWindowTitle(
    "amarPlayer Installer"
)

window.setFixedSize(
    450,
    250
)

layout = QVBoxLayout(
    window
)

title = QLabel(
    "amarPlayer"
)

title.setAlignment(
    Qt.AlignCenter
)

title.setStyleSheet(
    "font-size:28px;font-weight:bold;"
)

layout.addWidget(title)

info = QLabel(
    "Install amarPlayer dan hubungkan "
    "file audio dengan aplikasi."
)

info.setAlignment(
    Qt.AlignCenter
)

info.setWordWrap(True)

layout.addWidget(info)

button = QPushButton(
    "Install amarPlayer"
)

button.clicked.connect(
    install
)

layout.addWidget(
    button
)

window.show()

sys.exit(
    app.exec()
)
