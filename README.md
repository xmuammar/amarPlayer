# 🎵 amarPlayer

**amarPlayer** adalah pemutar musik desktop modern yang dikembangkan oleh **Muammar, SST, M.Kom** menggunakan **Python, PySide6, GStreamer, Mutagen, dan Pillow**.

Aplikasi ini dirancang sebagai pemutar musik desktop yang ringan, modern, sederhana, dan dapat dikembangkan menjadi aplikasi portable untuk Linux maupun Windows.

---

---

# 🖥️ Platform

| Platform         | Arsitektur            | Format           | Status          |
| ---------------- | --------------------- | ---------------- | --------------- |
| 🐧 Fedora Linux  | ARM64 / AArch64       | AppImage         | ✅ Aktif         |
| 🐧 Linux x64     | x86-64 / AMD64        | AppImage         | 🚧 Pengembangan |
| 🍎 macOS         | Apple Silicon / ARM64 | `.app`           | 🚧 Pengembangan |
| 🍎 macOS Intel   | x64                   | `.app`           | 🚧 Pengembangan |
| 🪟 Windows 11    | x64 / AMD64           | `.exe` Installer | 🔮 Rencana      |
| 🪟 Windows ARM64 | ARM64                 | `.exe`           | 
🚧 Pengembangan |

---
## ✨ Fitur

* 🎵 Pemutar musik desktop modern
* 🖥️ Antarmuka berbasis **PySide6**
* 🔊 Audio engine menggunakan **GStreamer**
* 🎚️ Equalizer 10-band
* 📂 Drag & Drop file musik
* 🔎 Pencarian lagu
* 📋 Playlist
* 🔀 Shuffle
* 🔁 Repeat
* ⏯️ Play / Pause
* ⏭️ Next / Previous
* ⏱️ Progress bar dan kontrol posisi lagu
* 🖼️ Album art / cover lagu
* 🏷️ Pembacaan metadata audio menggunakan Mutagen
* 💾 Playlist tersimpan secara permanen
* 📁 Membuka file audio langsung melalui command line
* 🎧 Mendukung berbagai format audio
* 🌙 Tampilan dark dan compact
* 📦 Dapat dikompilasi menjadi aplikasi standalone
* 🐧 Dukungan portable AppImage untuk Linux
* 🪟 Installer Windows x64
* 🚀 Build otomatis menggunakan GitHub Actions

---

## 🎧 Format Audio

amarPlayer mendukung berbagai format audio, antara lain:

```text
MP3
FLAC
WAV
OGG
OGA
OPUS
M4A
AAC
MP4
```

Dukungan format bergantung pada plugin GStreamer yang tersedia pada build.

---

# 🛠️ Teknologi

amarPlayer menggunakan:

| Teknologi      | Fungsi                            |
| -------------- | --------------------------------- |
| Python         | Bahasa pemrograman utama          |
| PySide6        | Antarmuka GUI                     |
| GStreamer      | Pemutaran audio                   |
| PyGObject      | Integrasi Python dengan GStreamer |
| Mutagen        | Metadata dan tag audio            |
| Pillow         | Pengolahan gambar/album art       |
| Nuitka         | Kompilasi aplikasi                |
| AppImage       | Distribusi portable Linux         |
| Inno Setup     | Installer Windows                 |
| GitHub Actions | Build otomatis Windows            |

---

# 📁 Struktur Project

Struktur utama repository:

```text
amarPlayer/
├── .github/
│   └── workflows/
│       └── build-windows.yml
│
├── amarPlayer.py
├── amarPlayer.png
├── .gitignore
└── README.md
```

File musik seperti:

```text
musik.mp3
```

tidak dimasukkan ke repository Git karena ukurannya besar dan hanya digunakan untuk pengujian lokal.

---

# 🐧 Linux

amarPlayer dikembangkan dan diuji pada Linux, termasuk:

```text
Fedora Linux
Fedora Asahi Remix
ARM64 / aarch64
```

Pada build portable, GStreamer dapat disertakan bersama aplikasi sehingga aplikasi tidak sepenuhnya bergantung pada instalasi GStreamer sistem.

## AppImage

Hasil build Linux berbentuk:

```text
amarPlayer-Linux-aarch64.AppImage
```

AppImage dapat dijalankan langsung:

```bash
./amarPlayer-Linux-aarch64.AppImage
```

Tidak diperlukan instalasi tradisional untuk menjalankan versi portable.

---

# 🪟 Windows

Versi Windows dibuat menggunakan:

```text
Windows x64
Python 3.12
Nuitka
PySide6
PyGObject
GStreamer 1.28.7
Inno Setup
```

Build Windows dilakukan menggunakan **GitHub Actions**, sehingga developer tidak harus memiliki komputer Windows untuk melakukan proses build.

Hasil akhirnya berupa:

```text
amarPlayer-Setup-Windows-x64.exe
```

Installer menggunakan instalasi per-user sehingga tidak memerlukan hak administrator.

Lokasi instalasi default:

```text
%LOCALAPPDATA%\Programs\amarPlayer
```

---

# ⚙️ Build Windows Otomatis

Workflow GitHub Actions tersedia di:

```text
.github/workflows/build-windows.yml
```

Workflow melakukan proses:

```text
Checkout source
        ↓
Setup Python 3.12 x64
        ↓
Install dependencies
        ↓
Verifikasi PyGObject
        ↓
Verifikasi GStreamer
        ↓
Test amarPlayer
        ↓
Compile dengan Nuitka
        ↓
Bundle GStreamer
        ↓
Bundle GStreamer plugins
        ↓
Bundle GObject typelibs
        ↓
Bundle DLL
        ↓
Test amarPlayer.exe
        ↓
Install Inno Setup
        ↓
Build Windows Installer
        ↓
Upload Artifact
```

---

# 🎛️ GStreamer Portable

Build Windows menyertakan runtime GStreamer yang diperlukan oleh amarPlayer.

Runtime mencakup komponen seperti:

```text
GStreamer DLL
GStreamer plugins
GObject
GLib
GIO
GModule
libffi
PCRE
Typelib
PyGObject runtime
```

Environment runtime disiapkan melalui:

```text
PATH
PYGI_DLL_DIRS
PYGI_DLL_PATH
GST_PLUGIN_PATH
GST_PLUGIN_SYSTEM_PATH_1_0
GI_TYPELIB_PATH
```

Hal ini memungkinkan aplikasi menemukan library, plugin, dan typelibs yang berada di dalam paket aplikasi.

GStreamer yang digunakan pada build Windows:

```text
GStreamer 1.28.7
```

---

# 🧩 Nuitka

amarPlayer dikompilasi menggunakan **Nuitka** dalam mode standalone.

Konsep build:

```text
amarPlayer.py
      ↓
    Nuitka
      ↓
amarPlayer.exe
      +
Python runtime
      +
PySide6
      +
PyGObject
      +
GStreamer
      +
Plugins
```

Dengan mode standalone, aplikasi tidak memerlukan instalasi source Python amarPlayer untuk dijalankan.

---

# 🔊 Audio Engine

amarPlayer menggunakan GStreamer sebagai audio engine.

Secara konsep:

```text
File Audio
    ↓
GStreamer
    ↓
Decoder
    ↓
Audio Processing
    ↓
10-Band Equalizer
    ↓
Volume
    ↓
Audio Output
```

Untuk pemutaran audio digunakan pipeline berbasis:

```text
playbin
```

Equalizer menggunakan:

```text
equalizer-10bands
```

---

# 🎚️ Equalizer

amarPlayer menyediakan equalizer 10-band.

Band frekuensi digunakan untuk mengatur karakter suara mulai dari frekuensi rendah hingga tinggi.

Contoh:

```text
60 Hz
170 Hz
310 Hz
600 Hz
1 kHz
3 kHz
6 kHz
12 kHz
14 kHz
16 kHz
```

Implementasi aktual mengikuti konfigurasi equalizer GStreamer yang tersedia pada runtime.

---

# 📋 Playlist

Playlist amarPlayer disimpan secara permanen di sistem pengguna.

Linux:

```text
~/.local/share/amarPlayer/amarPlayer_playlist.json
```

Dengan demikian playlist tidak hilang ketika aplikasi diperbarui atau ketika AppImage diganti dengan versi baru.

---

# 📂 Membuka File dari Command Line

amarPlayer dapat menerima file audio melalui command line.

Contoh:

```bash
./amarPlayer-Linux-aarch64.AppImage ~/Music/lagu.mp3
```

Beberapa file juga dapat diberikan sekaligus:

```bash
./amarPlayer-Linux-aarch64.AppImage \
    ~/Music/lagu1.mp3 \
    ~/Music/lagu2.mp3 \
    ~/Music/lagu3.mp3
```

Aplikasi akan memproses file audio tersebut dan memasukkannya ke playlist.

---

# 🖱️ Drag & Drop

File audio dapat dimasukkan ke aplikasi menggunakan:

```text
Drag & Drop
```

File akan divalidasi berdasarkan ekstensi audio yang didukung.

---

# 🖼️ Album Art

amarPlayer membaca cover/album art dari metadata file audio apabila tersedia.

Library:

```text
Pillow
Mutagen
```

digunakan untuk menangani metadata dan gambar.

Icon utama aplikasi:

```text
amarPlayer.png
```

---

# 🔐 Git dan GitHub

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

Branch utama:

```text
main
```

Repository menggunakan Git untuk menyimpan source code dan workflow build.

File besar seperti musik pengujian tidak dimasukkan ke Git:

```gitignore
musik.mp3
```

---

# 🚫 File yang Tidak Masuk Repository

Beberapa file sengaja diabaikan melalui `.gitignore`:

```text

__pycache__/
*.pyc

dist/
build/
release/


*.AppImage
*.msi
*.exe
```

Tujuannya agar repository tetap berisi source code dan konfigurasi build, bukan file binary hasil kompilasi berukuran besar.

---

# 🧪 Pengujian

Sebelum installer Windows dibuat, GitHub Actions melakukan beberapa pemeriksaan:

### Python

```text
Python 3.12 x64
```

### PyGObject

```text
import gi
```

### GStreamer

```text
Gst.init(None)
```

### amarPlayer

```text
import amarPlayer
```

### Nuitka

Memastikan:

```text
amarPlayer.exe
```

berhasil dibuat.

### Runtime

Memastikan environment GStreamer dan PyGObject tersedia sebelum executable dijalankan.

---

# 📦 Windows Installer

Installer Windows dibuat menggunakan:

```text
Inno Setup
```

Installer menghasilkan:

```text
amarPlayer-Setup-Windows-x64.exe
```

Installer menyediakan:

* instalasi amarPlayer
* shortcut Start Menu
* shortcut Desktop
* uninstall
* registrasi aplikasi Windows
* runtime aplikasi yang diperlukan

Instalasi menggunakan:

```text
PrivilegesRequired=lowest
```

sehingga dirancang untuk instalasi per-user tanpa membutuhkan administrator.

---

# 🚀 GitHub Actions

Untuk membuat build Windows:

1. Buka repository GitHub.
2. Pilih menu **Actions**.
3. Pilih:

```text
Build amarPlayer Windows x64
```

4. Klik:

```text
Run workflow
```

5. Tunggu proses build selesai.
6. Download artifact:

```text
amarPlayer-Windows-x64
```

Artifact berisi installer Windows.

---

# 🧑‍💻 Pengembangan Lokal

Clone repository:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
```

Masuk ke directory:

```bash
cd amarPlayer
```

Install dependency:

```bash
python3 -m pip install PySide6 mutagen Pillow PyGObject
```

Pastikan GStreamer dan plugin yang diperlukan tersedia pada sistem.

Kemudian jalankan:

```bash
python3 amarPlayer.py
```

---

# 🏗️ Filosofi Pengembangan

amarPlayer dikembangkan bukan sekadar sebagai contoh aplikasi pemutar musik.

Proyek ini dibangun dari kebutuhan nyata untuk memiliki:

```text
Pemutar musik sendiri
        ↓
Antarmuka sendiri
        ↓
Audio engine sendiri
        ↓
Playlist sendiri
        ↓
Equalizer sendiri
        ↓
Build portable
        ↓
Installer sendiri
        ↓
Distribusi sendiri
```

Tujuannya adalah membuat aplikasi yang benar-benar dapat digunakan sehari-hari, bukan hanya project latihan.

---

# 📌 Status Project

**Status: Aktif dalam pengembangan**

Komponen saat ini:

```text
GUI                         ✅
PySide6                     ✅
GStreamer                   ✅
Metadata                    ✅
Album Art                   ✅
Playlist                    ✅
Search                      ✅
Shuffle                     ✅
Repeat                      ✅
Equalizer 10-band           ✅
Drag & Drop                 ✅
Command-line file opening  ✅
Linux AppImage              ✅
GStreamer portable Linux   ✅
Windows x64 build           ✅
GitHub Actions              ✅
Windows installer           🚧
Windows runtime testing     🚧
```

---

# 🗺️ Roadmap

Rencana pengembangan:

* [x] Music player dasar
* [x] PySide6 GUI
* [x] GStreamer audio engine
* [x] Playlist
* [x] Search
* [x] Shuffle
* [x] Repeat
* [x] Equalizer
* [x] Album art
* [x] Drag & Drop
* [x] Command-line file opening
* [x] Linux standalone build
* [x] Linux AppImage
* [x] Portable GStreamer
* [x] GitHub repository
* [x] GitHub Actions Windows build
* [x] Nuitka Windows standalone build
* [x] Windows installer generation
* [ ] Final Windows runtime validation
* [ ] Windows audio file association
* [ ] Windows installer/uninstaller refinement
* [ ] macOS build
* [ ] Release versioning
* [ ] Public release

---

# 👨‍💻 Developer

**Muammar, SST, M.Kom**

Background:

```text
Informatika
Software Development
Data Science
Machine Learning
Web Development
```

amarPlayer merupakan proyek pengembangan pribadi untuk membangun aplikasi desktop yang dapat digunakan secara nyata sekaligus menjadi ruang eksperimen dalam pengembangan software lintas platform.

---

# ❤️ amarPlayer

> **Pakai pemutar musik salah ❌**
> **Buat sendiri pemutar musik "amarPlayer" ✅**

---

## License

License project dapat ditentukan pada tahap rilis publik.

Saat ini repository terutama digunakan sebagai project pengembangan dan eksperimen pribadi.

