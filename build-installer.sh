#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
RELEASE_DIR="$PROJECT_DIR/release"
BUILD_DIR="$RELEASE_DIR/build"
APPDIR="$RELEASE_DIR/amarPlayer.AppDir"

INSTALLER_DIR="$PROJECT_DIR/installer"
INSTALLER_APPDIR="$RELEASE_DIR/installer.AppDir"

APPIMAGE_TOOL="$PROJECT_DIR/appimagetool-aarch64.AppImage"

echo
echo "=============================================="
echo " amarPlayer FINAL BUILD"
echo "=============================================="
echo

# ============================================================
# CHECK
# ============================================================

command -v python3 >/dev/null || {
    echo "ERROR: python3 tidak ditemukan."
    exit 1
}

command -v gst-inspect-1.0 >/dev/null || {
    echo "ERROR: GStreamer tidak ditemukan."
    exit 1
}

if [ ! -f "$PROJECT_DIR/amarPlayer.py" ]; then
    echo "ERROR: amarPlayer.py tidak ditemukan."
    exit 1
fi

if [ ! -f "$PROJECT_DIR/amarPlayer.png" ]; then
    echo "ERROR: amarPlayer.png tidak ditemukan."
    exit 1
fi

# ============================================================
# APPIMAGE TOOL
# ============================================================

if [ ! -f "$APPIMAGE_TOOL" ]; then

    echo "[1] Download appimagetool..."

    wget -O "$APPIMAGE_TOOL" \
        https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-aarch64.AppImage
fi

chmod +x "$APPIMAGE_TOOL"

# ============================================================
# CLEAN
# ============================================================

echo "[2] Membersihkan build lama..."

rm -rf "$RELEASE_DIR"
rm -rf "$INSTALLER_DIR"

mkdir -p "$RELEASE_DIR"
mkdir -p "$BUILD_DIR"
mkdir -p "$INSTALLER_DIR"

# appimagetool berada di project root dan tidak boleh terhapus
# karena RELEASE_DIR saja yang dihapus.

# ============================================================
# NUITKA
# ============================================================

echo "[3] Build amarPlayer dengan Nuitka..."

python3 -m nuitka \
    --mode=standalone \
    --enable-plugin=pyside6 \
    --follow-imports \
    --output-dir="$BUILD_DIR" \
    --output-filename=amarPlayer \
    --product-name="amarPlayer" \
    --file-description="Modern Music Player" \
    --company-name="Muammar" \
    "$PROJECT_DIR/amarPlayer.py"

NUITKA_DIR="$BUILD_DIR/amarPlayer.dist"

if [ ! -x "$NUITKA_DIR/amarPlayer" ]; then
    echo "ERROR: hasil Nuitka tidak ditemukan."
    exit 1
fi

# ============================================================
# APPDIR
# ============================================================

echo "[4] Membuat AppDir..."

mkdir -p "$APPDIR"

cp -a "$NUITKA_DIR/." "$APPDIR/"

# ============================================================
# GSTREAMER DIRECTORIES
# ============================================================

echo "[5] Mengambil GStreamer..."

mkdir -p \
    "$APPDIR/lib" \
    "$APPDIR/lib/gstreamer-1.0" \
    "$APPDIR/libexec/gstreamer-1.0"

# ============================================================
# FUNCTION COPY LIB
# ============================================================

copy_lib()
{
    local NAME="$1"

    local PATH_FOUND

    PATH_FOUND="$(ldconfig -p 2>/dev/null | \
        grep -m1 "lib${NAME}\.so" | \
        sed -E 's/.*=> //' || true)"

    if [ -n "$PATH_FOUND" ] && [ -f "$PATH_FOUND" ]; then

        echo "  LIB: $PATH_FOUND"

        cp -L \
            "$PATH_FOUND" \
            "$APPDIR/lib/"

    else

        echo "  WARNING: lib${NAME}.so tidak ditemukan."

    fi
}

# ============================================================
# CORE GSTREAMER
# ============================================================

copy_lib "gstreamer-1.0"
copy_lib "gstbase-1.0"
copy_lib "gstcontroller-1.0"
copy_lib "gstnet-1.0"
copy_lib "gstaudio-1.0"
copy_lib "gsttag-1.0"
copy_lib "gstpbutils-1.0"

# ============================================================
# GLIB
# ============================================================

copy_lib "glib-2.0"
copy_lib "gobject-2.0"
copy_lib "gmodule-2.0"

# ============================================================
# AUDIO DEPENDENCIES
# ============================================================

copy_lib "orc-0.4"
copy_lib "mpg123"

# ============================================================
# GSTREAMER PLUGINS
# ============================================================

echo
echo "Mengambil plugin GStreamer..."

GST_PLUGIN_SYSTEM="$(pkg-config --variable=pluginsdir gstreamer-1.0 2>/dev/null || true)"

if [ -z "$GST_PLUGIN_SYSTEM" ]; then

    GST_PLUGIN_SYSTEM="/usr/lib64/gstreamer-1.0"

fi

echo "Plugin system:"
echo "  $GST_PLUGIN_SYSTEM"

if [ ! -d "$GST_PLUGIN_SYSTEM" ]; then

    echo "ERROR: directory plugin GStreamer tidak ditemukan."
    exit 1

fi

PLUGINS=(
    libgstcoreelements.so
    libgstplayback.so
    libgstequalizer.so
    libgstaudioconvert.so
    libgstaudioresample.so
    libgstvolume.so
    libgstaudioparsers.so
    libgstflac.so
    libgstmpg123.so
    libgstid3demux.so
    libgstisomp4.so
    libgstogg.so
    libgstopus.so
    libgstvorbis.so
    libgsttypefindfunctions.so
    libgstautodetect.so
    libgstpulseaudio.so
    libgstpipewire.so
)

for plugin in "${PLUGINS[@]}"; do

    if [ -f "$GST_PLUGIN_SYSTEM/$plugin" ]; then

        echo "  PLUGIN: $plugin"

        cp -L \
            "$GST_PLUGIN_SYSTEM/$plugin" \
            "$APPDIR/lib/gstreamer-1.0/"

    else

        echo "  SKIP: $plugin"

    fi

done

# ============================================================
# GST PLUGIN SCANNER
# ============================================================

echo
echo "Mencari gst-plugin-scanner..."

SCANNER="$(find /usr -type f \
    -path '*/gstreamer-1.0/gst-plugin-scanner' \
    2>/dev/null | head -1 || true)"

if [ -z "$SCANNER" ]; then

    echo "ERROR: gst-plugin-scanner tidak ditemukan."
    exit 1

fi

echo "  $SCANNER"

cp -L \
    "$SCANNER" \
    "$APPDIR/libexec/gstreamer-1.0/gst-plugin-scanner"

chmod +x \
    "$APPDIR/libexec/gstreamer-1.0/gst-plugin-scanner"

# ============================================================
# RESOLVE DEPENDENCIES
# ============================================================

echo
echo "Menyalin dependency library GStreamer..."

for file in \
    "$APPDIR/lib/"*.so* \
    "$APPDIR/lib/gstreamer-1.0/"*.so
do

    [ -f "$file" ] || continue

    while read -r dependency; do

        [ -f "$dependency" ] || continue

        basename_dependency="$(basename "$dependency")"

        case "$basename_dependency" in

            libc.so*)
                continue
                ;;

            libm.so*)
                continue
                ;;

            libpthread.so*)
                continue
                ;;

            librt.so*)
                continue
                ;;

            libdl.so*)
                continue
                ;;

            libgcc_s.so*)
                continue
                ;;

            libstdc++.so*)
                continue
                ;;

            libsystemd.so*)
                ;;

            libwayland*)
                ;;

            libX11*)
                ;;

            libxcb*)
                ;;

            libpulse*)
                ;;

            libpipewire*)
                ;;

        esac

        if [ ! -e "$APPDIR/lib/$basename_dependency" ]; then

            cp -L \
                "$dependency" \
                "$APPDIR/lib/" \
                2>/dev/null || true

        fi

    done < <(
        ldd "$file" 2>/dev/null |
        awk '/=> \// {print $3} /^\// {print $1}' |
        sort -u
    )

done

# ============================================================
# ICON
# ============================================================

echo
echo "[6] Menyiapkan icon..."

mkdir -p \
    "$APPDIR/usr/share/applications" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps"

cp \
    "$PROJECT_DIR/amarPlayer.png" \
    "$APPDIR/amarPlayer.png"

cp \
    "$PROJECT_DIR/amarPlayer.png" \
    "$APPDIR/.DirIcon"

cp \
    "$PROJECT_DIR/amarPlayer.png" \
    "$APPDIR/usr/share/icons/hicolor/256x256/apps/amarPlayer.png"

# ============================================================
# DESKTOP
# ============================================================

cat > "$APPDIR/amarPlayer.desktop" <<'DESKTOP'
[Desktop Entry]
Name=amarPlayer
Comment=Modern Music Player
Exec=amarPlayer %U
Icon=amarPlayer
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Player;
StartupWMClass=amarPlayer
MimeType=audio/mpeg;audio/flac;audio/x-wav;audio/ogg;audio/x-vorbis+ogg;audio/opus;audio/mp4;audio/aac;audio/x-m4a;
DESKTOP

cp \
    "$APPDIR/amarPlayer.desktop" \
    "$APPDIR/usr/share/applications/amarPlayer.desktop"

# ============================================================
# APPRUN
# ============================================================

cat > "$APPDIR/AppRun" <<'APPRUN'
#!/usr/bin/env bash

HERE="$(cd "$(dirname "$0")" && pwd)"

export LD_LIBRARY_PATH="$HERE/lib:$HERE:${LD_LIBRARY_PATH:-}"

export GST_PLUGIN_PATH="$HERE/lib/gstreamer-1.0"

export GST_PLUGIN_SYSTEM_PATH=""

export GST_PLUGIN_SCANNER="$HERE/libexec/gstreamer-1.0/gst-plugin-scanner"

export GST_REGISTRY="$HERE/gst-registry.bin"

exec "$HERE/amarPlayer" "$@"
APPRUN

chmod +x \
    "$APPDIR/AppRun"

chmod +x \
    "$APPDIR/amarPlayer"

# ============================================================
# TEST PORTABLE GSTREAMER
# ============================================================

echo
echo "[7] Test GStreamer portable..."

export LD_LIBRARY_PATH="$APPDIR/lib:$APPDIR:${LD_LIBRARY_PATH:-}"
export GST_PLUGIN_PATH="$APPDIR/lib/gstreamer-1.0"
export GST_PLUGIN_SYSTEM_PATH=""
export GST_PLUGIN_SCANNER="$APPDIR/libexec/gstreamer-1.0/gst-plugin-scanner"
export GST_REGISTRY="$APPDIR/gst-registry-test.bin"

"$APPDIR/amarPlayer" \
    --version \
    >/dev/null 2>&1 || true

echo
echo "Test playbin..."

if gst-inspect-1.0 \
    playbin \
    >/dev/null 2>&1
then

    echo "  playbin OK"

else

    echo "ERROR: playbin tidak tersedia."
    echo
    echo "Plugin yang tersedia:"
    GST_PLUGIN_PATH="$APPDIR/lib/gstreamer-1.0" \
    GST_PLUGIN_SYSTEM_PATH="" \
    GST_PLUGIN_SCANNER="$APPDIR/libexec/gstreamer-1.0/gst-plugin-scanner" \
    gst-inspect-1.0 playbin || true

    exit 1

fi

rm -f \
    "$APPDIR/gst-registry-test.bin"

unset LD_LIBRARY_PATH
unset GST_PLUGIN_PATH
unset GST_PLUGIN_SYSTEM_PATH
unset GST_PLUGIN_SCANNER
unset GST_REGISTRY

# ============================================================
# BUILD AMARPLAYER APPIMAGE
# ============================================================

echo
echo "[8] Membuat amarPlayer AppImage..."

rm -f \
    "$RELEASE_DIR/amarPlayer-Linux-aarch64.AppImage"

ARCH=aarch64 \
    "$APPIMAGE_TOOL" \
    "$APPDIR" \
    "$RELEASE_DIR/amarPlayer-Linux-aarch64.AppImage"

chmod +x \
    "$RELEASE_DIR/amarPlayer-Linux-aarch64.AppImage"

echo
echo "amarPlayer AppImage berhasil dibuat."

# ============================================================
# GENERATE INSTALLER
# ============================================================

echo
echo "[9] Membuat installer..."

cp \
    "$RELEASE_DIR/amarPlayer-Linux-aarch64.AppImage" \
    "$INSTALLER_DIR/amarPlayer-Linux-aarch64.AppImage"

cp \
    "$PROJECT_DIR/amarPlayer.png" \
    "$INSTALLER_DIR/amarPlayer.png"

cat > "$INSTALLER_DIR/amarPlayer-installer.py" <<'PYTHON'
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
PYTHON

# ============================================================
# GENERATE UNINSTALLER
# ============================================================

echo "[10] Membuat uninstaller..."

cat > "$INSTALLER_DIR/amarPlayer-uninstaller.py" <<'PYTHON'
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
PYTHON

# ============================================================
# COMPILE INSTALLER
# ============================================================

echo
echo "[11] Compile installer..."

python3 -m nuitka \
    --mode=standalone \
    --enable-plugin=pyside6 \
    --follow-imports \
    --output-dir="$BUILD_DIR/installer" \
    --output-filename=amarPlayer-installer \
    "$INSTALLER_DIR/amarPlayer-installer.py"

echo
echo "[12] Compile uninstaller..."

python3 -m nuitka \
    --mode=standalone \
    --enable-plugin=pyside6 \
    --follow-imports \
    --output-dir="$BUILD_DIR/uninstaller" \
    --output-filename=amarPlayer-uninstaller \
    "$INSTALLER_DIR/amarPlayer-uninstaller.py"

# ============================================================
# INSTALLER APPDIR
# ============================================================

echo
echo "[13] Membuat installer AppDir..."

mkdir -p \
    "$INSTALLER_APPDIR/usr/bin" \
    "$INSTALLER_APPDIR/usr/share/applications" \
    "$INSTALLER_APPDIR/usr/share/icons/hicolor/256x256/apps" \
    "$INSTALLER_APPDIR/payload"

cp -a \
    "$BUILD_DIR/installer/amarPlayer-installer.dist/." \
    "$INSTALLER_APPDIR/usr/bin/"

cp -a \
    "$BUILD_DIR/uninstaller/amarPlayer-uninstaller.dist/." \
    "$INSTALLER_APPDIR/usr/bin/"

cp \
    "$INSTALLER_DIR/amarPlayer-Linux-aarch64.AppImage" \
    "$INSTALLER_APPDIR/payload/"

cp \
    "$INSTALLER_DIR/amarPlayer.png" \
    "$INSTALLER_APPDIR/amarPlayer.png"

cp \
    "$INSTALLER_DIR/amarPlayer.png" \
    "$INSTALLER_APPDIR/.DirIcon"

# ============================================================
# INSTALLER APPRUN
# ============================================================

cat > "$INSTALLER_APPDIR/AppRun" <<'APPRUN'
#!/usr/bin/env bash

HERE="$(cd "$(dirname "$0")" && pwd)"

export APPDIR="$HERE"

exec "$HERE/usr/bin/amarPlayer-installer" "$@"
APPRUN

chmod +x \
    "$INSTALLER_APPDIR/AppRun"

# ============================================================
# FINAL INSTALLER
# ============================================================

echo
echo "[14] Membuat installer AppImage..."

rm -f \
    "$INSTALLER_DIR/amarPlayer-installer-Linux-aarch64.AppImage"

ARCH=aarch64 \
    "$APPIMAGE_TOOL" \
    "$INSTALLER_APPDIR" \
    "$INSTALLER_DIR/amarPlayer-installer-Linux-aarch64.AppImage"

chmod +x \
    "$INSTALLER_DIR/amarPlayer-installer-Linux-aarch64.AppImage"

# ============================================================
# FINAL
# ============================================================

echo
echo "=============================================="
echo " BUILD SELESAI"
echo "=============================================="
echo
echo "Installer:"
echo
echo "  $INSTALLER_DIR/amarPlayer-installer-Linux-aarch64.AppImage"
echo
echo "Folder:"
echo
echo "  $INSTALLER_DIR"
echo
ls -lh "$INSTALLER_DIR"
echo
