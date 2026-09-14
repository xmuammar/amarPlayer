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
    QCheckBox,
)

from PySide6.QtCore import Qt


INSTALL_DIR = os.path.expanduser(
    "~/.local/opt/amarPlayer"
)

APP_DIR = os.path.expanduser(
    "~/.local/share/applications"
)

DATA_DIR = os.path.expanduser(
    "~/.local/share/amarPlayer"
)

DESKTOP = os.path.join(
    APP_DIR,
    "amarPlayer.desktop"
)

ICON = os.path.expanduser(
    "~/.local/share/icons/hicolor/256x256/apps/amarPlayer.png"
)


def uninstall(remove_data):

    if os.path.exists(DESKTOP):
        os.remove(DESKTOP)

    if os.path.exists(ICON):
        os.remove(ICON)

    if os.path.isdir(INSTALL_DIR):
        shutil.rmtree(
            INSTALL_DIR,
            ignore_errors=True
        )

    if remove_data and os.path.isdir(DATA_DIR):

        shutil.rmtree(
            DATA_DIR,
            ignore_errors=True
        )

    subprocess.run(
        [
            "update-desktop-database",
            APP_DIR
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False
    )


app = QApplication(sys.argv)

window = QWidget()

window.setWindowTitle(
    "Uninstall amarPlayer"
)

window.setFixedSize(
    450,
    280
)

layout = QVBoxLayout(
    window
)

title = QLabel(
    "Uninstall amarPlayer"
)

title.setAlignment(
    Qt.AlignCenter
)

title.setStyleSheet(
    "font-size:24px;font-weight:bold;"
)

layout.addWidget(title)

check = QCheckBox(
    "Hapus juga playlist dan data pengguna"
)

layout.addWidget(check)

button = QPushButton(
    "Uninstall"
)

def do_uninstall():

    answer = QMessageBox.question(
        window,
        "amarPlayer",
        "Yakin ingin menghapus amarPlayer?"
    )

    if answer != QMessageBox.Yes:
        return

    uninstall(
        check.isChecked()
    )

    QMessageBox.information(
        window,
        "amarPlayer",
        "amarPlayer berhasil dihapus."
    )

    window.close()


button.clicked.connect(
    do_uninstall
)

layout.addWidget(button)

window.show()

sys.exit(
    app.exec()
)
