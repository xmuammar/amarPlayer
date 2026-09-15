Berikut **README.md lengkap yang sudah digabungkan**, termasuk bagian instalasi dependency dari source:

# amarPlayer

**amarPlayer** adalah aplikasi pemutar musik desktop yang dikembangkan oleh **Muammar, SST., M.Kom.** menggunakan Python, PySide6, GStreamer, Mutagen, dan Pillow.

amarPlayer dibuat sebagai pemutar musik desktop yang sederhana, modern, ringan, dan dapat dikembangkan untuk berbagai sistem operasi Linux serta Windows.

---

## ✨ Fitur

* Pemutar musik desktop berbasis PySide6
* GStreamer sebagai multimedia backend
* Playlist musik
* Penyimpanan playlist secara otomatis
* Pencarian musik
* Scan folder musik
* Drag and drop file musik
* Shuffle
* Repeat
* Kontrol volume
* Progress bar dan seek audio
* Informasi durasi audio
* Metadata musik menggunakan Mutagen
* Album art menggunakan Pillow
* Equalizer 10-band
* Membuka file musik melalui command line
* Mendukung berbagai format audio
* Antarmuka desktop yang sederhana dan responsif

---

## 🎵 Format Audio

amarPlayer mendukung berbagai format audio melalui GStreamer:

```text
.mp3
.flac
.wav
.ogg
.oga
.opus
.m4a
.aac
.mp4
```

Ketersediaan format tertentu bergantung pada plugin GStreamer yang tersedia pada sistem operasi pengguna.

---

## 🛠️ Teknologi

amarPlayer dikembangkan menggunakan:

* Python 3
* PySide6
* GStreamer
* PyGObject
* Mutagen
* Pillow

### Komponen utama

```text
Python
 ├── PySide6
 ├── PyGObject
 ├── Mutagen
 └── Pillow
        │
        ▼
    amarPlayer
        │
        ▼
    GStreamer
        │
        ▼
   Audio Output
```

---

## 📂 Struktur Project

```text
amarPlayer/
├── amarPlayer.py
├── amarPlayer.png
├── amarPlayer-debug.log
├── README.md
├── build-installer.sh
├── installer/
├── packaging/
│   ├── debian/
│   │   ├── control
│   │   ├── rules
│   │   ├── changelog
│   │   └── amarPlayer.desktop
│   │
│   └── fedora/
│       └── amarPlayer.spec
├── debian/
│   ├── control
│   ├── rules
│   ├── changelog
│   └── amarPlayer.desktop
├── release/
├── .github/
│   └── workflows/
│       └── build-rpm.yml
└── appimagetool-aarch64.AppImage
```

Direktori `debian/` pada root project digunakan oleh sistem Debian packaging ketika membangun paket `.deb`.

---

# 🐧 Linux

Linux merupakan salah satu target utama pengembangan amarPlayer.

Tujuan packaging adalah menyediakan amarPlayer untuk sebanyak mungkin distribusi Linux, baik melalui paket native maupun format universal.

## Status Packaging Linux

| Distribusi / Ekosistem | Format             | Status           |
| ---------------------- | ------------------ | ---------------- |
| Fedora x86_64          | RPM                | ✅ Berhasil       |
| Fedora aarch64         | RPM                | ✅ Berhasil       |
| Fedora COPR            | RPM                | ✅ Berhasil       |
| RHEL                   | RPM                | 🔄 Pengembangan  |
| CentOS Stream          | RPM                | 🔄 Pengembangan  |
| Rocky Linux            | RPM                | 🔄 Pengembangan  |
| AlmaLinux              | RPM                | 🔄 Pengembangan  |
| openSUSE               | RPM                | 🔄 Pengembangan  |
| SUSE Linux Enterprise  | RPM                | 🔄 Pengembangan  |
| Debian                 | DEB                | ✅ Berhasil build |
| Ubuntu                 | DEB                | 🔄 Pengujian     |
| Linux Mint             | DEB                | 🔄 Pengujian     |
| Pop!_OS                | DEB                | 🔄 Pengujian     |
| Arch Linux             | Arch Package       | 🔄 Pengembangan  |
| Manjaro                | Arch Package       | 🔄 Pengembangan  |
| EndeavourOS            | Arch Package       | 🔄 Pengembangan  |
| AppImage               | Universal          | 🔄 Pengembangan  |
| Flatpak                | Universal          | 🔄 Pengembangan  |
| Open Build Service     | Multi-distribution | 🔄 Pengembangan  |

---

# 📦 Fedora / RPM

amarPlayer sudah berhasil dibangun sebagai paket RPM pada Fedora.

Target Fedora:

```text
Fedora 44 x86_64
Fedora 44 aarch64
```

Paket dibangun menggunakan Fedora COPR.

## COPR

Repository:

```text
xmuammar/amarPlayer
```

Build yang telah berhasil:

```text
Build ID: 10987450
Status: succeeded
```

## Instalasi Fedora

Aktifkan repository COPR:

```bash
sudo dnf copr enable xmuammar/amarPlayer
```

Kemudian instal amarPlayer:

```bash
sudo dnf install amarPlayer
```

Jalankan:

```bash
amarPlayer
```

---

# 🏢 RPM Family

Packaging RPM amarPlayer direncanakan untuk berbagai distribusi berbasis RPM:

```text
Fedora
RHEL
CentOS Stream
Rocky Linux
AlmaLinux
openSUSE
SUSE Linux Enterprise
```

Target arsitektur:

```text
x86_64
aarch64 / ARM64
```

Tidak semua distribusi memiliki nama atau versi paket dependensi yang sama. Karena itu setiap target distribusi akan diuji secara terpisah.

---

# 🟦 Debian / Ubuntu Family

Paket Debian `.deb` digunakan sebagai format native untuk distribusi berbasis Debian.

Target:

```text
Debian
Ubuntu
Linux Mint
Pop!_OS
dan distribusi berbasis Debian/Ubuntu lainnya
```

Target arsitektur:

```text
amd64 / x86_64
arm64 / aarch64
```

## Status Debian

Paket Debian amarPlayer **sudah berhasil dibangun** menggunakan lingkungan Debian ARM64 melalui Podman.

Paket yang dihasilkan:

```text
amarplayer_1.0.0-1_all.deb
```

Architecture:

```text
all
```

Karena aplikasi utama amarPlayer ditulis menggunakan Python dan tidak membawa binary native khusus arsitektur.

## Isi Paket

Paket `.deb` menyediakan:

```text
/usr/bin/amarPlayer
/usr/share/amarPlayer/amarPlayer.py
/usr/share/applications/amarPlayer.desktop
/usr/share/icons/hicolor/512x512/apps/amarPlayer.png
```

## Dependency Debian

Paket menggunakan dependency sistem:

```text
python3
python3-pyside6.qtcore
python3-pyside6.qtgui
python3-pyside6.qtwidgets
python3-gi
python3-gst-1.0
python3-mutagen
python3-pil
gstreamer1.0-tools
gstreamer1.0-plugins-base
gstreamer1.0-plugins-good
gstreamer1.0-plugins-bad
gstreamer1.0-libav
```

Dependency tidak dibundel ke dalam file `.deb`. Sistem Debian/Ubuntu akan menangani dependency tersebut melalui package manager.

## Build Debian

Environment build menggunakan Podman dengan container:

```text
amarplayer-debian-builder
```

Setelah environment builder tersedia, build dapat dilakukan dengan:

```bash
cd ~/aplikasiMp3 && \
podman exec amarplayer-debian-builder \
bash -lc 'dpkg-buildpackage -us -uc -b'
```

Hasil:

```text
amarplayer_1.0.0-1_all.deb
```

Build menggunakan container Debian yang sudah memiliki dependency dan tool packaging sehingga proses build berikutnya tidak perlu mengulang instalasi dependency.

## Instalasi Debian / Ubuntu

Setelah paket `.deb` tersedia:

```bash
sudo apt install ./amarplayer_1.0.0-1_all.deb
```

Kemudian jalankan:

```bash
amarPlayer
```

---

# 🏹 Arch Linux Family

Packaging Arch direncanakan untuk:

```text
Arch Linux
Manjaro
EndeavourOS
dan distribusi berbasis Arch lainnya
```

Format paket:

```text
.pkg.tar.zst
```

---

# 📦 AppImage

AppImage digunakan sebagai salah satu format universal amarPlayer.

Tujuannya adalah memungkinkan pengguna menjalankan amarPlayer pada berbagai distribusi Linux tanpa harus memasang paket native khusus untuk setiap distribusi.

Contoh:

```bash
chmod +x amarPlayer.AppImage
./amarPlayer.AppImage
```

Target:

```text
Linux x86_64
Linux aarch64 / ARM64
```

AppImage sangat berguna untuk pengguna yang ingin mengunduh satu file dan langsung menjalankan aplikasi.

---

# 📦 Flatpak

Flatpak direncanakan sebagai format distribusi universal untuk desktop Linux.

Targetnya adalah membuat amarPlayer dapat digunakan pada berbagai lingkungan desktop Linux tanpa harus menyediakan paket native secara manual untuk setiap distribusi.

Target arsitektur:

```text
x86_64
aarch64 / ARM64
```

---

# 🏗️ Open Build Service

Open Build Service (OBS) direncanakan sebagai sistem build lintas distribusi.

OBS akan digunakan untuk membantu membangun paket amarPlayer untuk berbagai target distribusi Linux dari source yang sama.

Target pengembangan:

```text
Fedora
openSUSE
SUSE Linux Enterprise
Debian
Ubuntu
dan distribusi lain yang didukung OBS
```

---

# 🌍 Strategi Distribusi Linux

Target akhir distribusi amarPlayer:

```text
                         amarPlayer
                             │
             ┌───────────────┴───────────────┐
             │                               │
      Native Packages                  Universal Packages
             │                               │
      ┌──────┼──────┐                  ┌─────┴─────┐
      │      │      │                  │           │
     RPM    DEB    Arch            AppImage     Flatpak
      │      │      │                  │           │
   Fedora Debian  Arch              Linux       Linux
   RHEL   Ubuntu  Manjaro           x86_64      Desktop
   SUSE   Mint    EndeavourOS       ARM64       ARM64
```

Dengan pendekatan ini, pengguna tidak harus menggunakan Fedora untuk menjalankan amarPlayer.

---

# 💻 Windows

Windows juga menjadi salah satu target distribusi amarPlayer.

Packaging Windows dikembangkan secara terpisah dari packaging Linux.

Target:

```text
Windows x64
Windows ARM64
```

Build Windows dilakukan menggunakan sistem CI/CD ketika lingkungan Windows x64 tidak tersedia secara lokal.

---

# ▶️ Menjalankan dari Source

Clone repository:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
cd amarPlayer
```

Sebelum menjalankan aplikasi, instal dependency sesuai distribusi Linux yang digunakan.

---

## 🐧 Instalasi Dependency Source — Fedora

Instal dependency sistem:

```bash
sudo dnf install \
    python3 \
    python3-gobject \
    python3-gstreamer1 \
    python3-pyside6 \
    python3-mutagen \
    python3-pillow \
    gstreamer1 \
    gstreamer1-plugins-base \
    gstreamer1-plugins-good \
    gstreamer1-plugins-bad-free \
    gstreamer1-plugin-mpg123
```

Kemudian jalankan:

```bash
python3 amarPlayer.py
```

---

## 🟦 Instalasi Dependency Source — Debian / Ubuntu

Pada Debian/Ubuntu, paket PySide6 menggunakan modul yang terpisah.

Perbarui database paket:

```bash
sudo apt update
```

Kemudian instal dependency:

```bash
sudo apt install \
    python3 \
    python3-pyside6.qtcore \
    python3-pyside6.qtgui \
    python3-pyside6.qtwidgets \
    python3-gi \
    python3-gst-1.0 \
    python3-mutagen \
    python3-pil \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-libav
```

Kemudian jalankan:

```bash
python3 amarPlayer.py
```

---

## 🎵 Dependency Multimedia

amarPlayer menggunakan GStreamer sebagai multimedia backend.

GStreamer membutuhkan plugin yang sesuai dengan format audio yang ingin diputar.

Format yang didukung aplikasi:

```text
.mp3
.flac
.wav
.ogg
.oga
.opus
.m4a
.aac
.mp4
```

Ketersediaan format tertentu bergantung pada plugin GStreamer yang tersedia pada distribusi Linux yang digunakan.

---

## 🐍 Dependency Python

Dependency utama amarPlayer:

```text
Python 3
PySide6
PyGObject
Mutagen
Pillow
```

Dependency multimedia:

```text
GStreamer
GStreamer plugins
```

Nama paket dapat berbeda antara Fedora, Debian, Ubuntu, dan distribusi Linux lainnya.

Setelah semua dependency tersedia, jalankan:

```bash
python3 amarPlayer.py
```

---

# 📁 Penyimpanan Playlist

Pada Linux, playlist pengguna disimpan di:

```text
~/.local/share/amarPlayer/amarPlayer_playlist.json
```

Dengan demikian playlist tidak disimpan di dalam direktori instalasi aplikasi.

---

# ⚙️ Konfigurasi

amarPlayer menggunakan konfigurasi dan data pengguna pada direktori data pengguna Linux.

Hal ini memungkinkan aplikasi yang diinstal secara system-wide tetap memiliki data playlist yang terpisah untuk setiap pengguna.

---

# 🔧 Pengembangan

Source utama amarPlayer:

```text
/home/muammar/aplikasiMp3
```

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

Pengembangan dilakukan secara bertahap mulai dari source application, packaging native, hingga universal Linux packaging.

Packaging saat ini mencakup:

```text
Fedora RPM
Debian DEB
```

dan sedang dikembangkan untuk format serta distribusi lainnya.

---

# 🧪 Pengujian

Setiap paket diharapkan melalui pengujian:

1. Build package
2. Instalasi
3. Menjalankan aplikasi
4. Membuka file audio
5. Memutar audio
6. Membaca metadata
7. Menampilkan album art
8. Menggunakan playlist
9. Menggunakan equalizer
10. Pengujian format audio

Pengujian dilakukan secara bertahap pada setiap distribusi dan arsitektur.

---

# 🚀 Roadmap

## Linux

* [x] Fedora RPM
* [x] Fedora x86_64
* [x] Fedora aarch64
* [x] Fedora COPR
* [x] Debian DEB build
* [ ] Debian DEB runtime testing
* [ ] Ubuntu DEB
* [ ] Linux Mint DEB
* [ ] Pop!_OS DEB
* [ ] RHEL RPM
* [ ] CentOS Stream RPM
* [ ] Rocky Linux RPM
* [ ] AlmaLinux RPM
* [ ] openSUSE RPM
* [ ] SUSE Linux Enterprise RPM
* [ ] Arch Linux package
* [ ] Manjaro package
* [ ] AppImage x86_64
* [ ] AppImage aarch64
* [ ] Flatpak
* [ ] Open Build Service
* [ ] Automated multi-distribution releases

## Windows

* [ ] Windows x64
* [ ] Windows ARM64
* [ ] Automated Windows release

---

# 📊 Target Arsitektur

amarPlayer ditujukan untuk dua arsitektur utama:

```text
x86_64 / amd64
aarch64 / arm64
```

ARM64 sangat penting untuk perangkat modern seperti:

* Apple Silicon melalui Linux/Asahi
* ARM laptop
* ARM desktop
* ARM server
* Single-board computer yang kompatibel

---

# 📜 Lisensi

amarPlayer menggunakan:

```text
MIT License
```

---

# 👨‍💻 Developer

**Muammar, SST., M.Kom.**

Project:

```text
amarPlayer
```

GitHub:

```text
https://github.com/xmuammar/amarPlayer
```

---

# ❤️ Tentang amarPlayer

amarPlayer dikembangkan sebagai project pribadi untuk menghasilkan pemutar musik desktop yang sederhana, praktis, dan dapat digunakan sehari-hari.

Pengembangan tidak hanya berfokus pada aplikasi, tetapi juga pada bagaimana aplikasi dapat didistribusikan kepada pengguna Linux dari berbagai distribusi dan arsitektur.

Target akhirnya adalah:

> **Satu aplikasi, banyak distribusi Linux, banyak arsitektur, dan proses distribusi yang semakin otomatis.**

