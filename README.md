# amarPlayer 🎵

**amarPlayer** adalah pemutar musik desktop modern yang dikembangkan oleh **Muammar, SST, M.Kom** menggunakan Python, PySide6, GStreamer, dan Mutagen.

Aplikasi ini dirancang untuk menjadi pemutar musik desktop yang ringan, modern, sederhana, dan dapat digunakan pada beberapa platform.

---

## 🖥️ Platform

| Platform         | Arsitektur            | Format                 | Status            |
| ---------------- | --------------------- | ---------------------- | ----------------- |
| 🐧 Fedora Linux  | ARM64 / AArch64       | AppImage               | ✅ Aktif           |
| 🍎 macOS         | Apple Silicon / ARM64 | App Bundle / AppImage* | 🚧 Pengembangan   |
| 🪟 Windows 11    | x64 / AMD64           | `.exe` Installer       | 🚧 GitHub Actions |
| 🐧 Linux lainnya | ARM64 / x64           | AppImage               | 🚧 Pengembangan   |
| 🍎 macOS Intel   | x64                   | App Bundle             | 🚧 Pengembangan   |
| 🪟 Windows ARM64 | ARM64                 | `.exe`                 | 🔮 Rencana        |

> * Format distribusi macOS dapat berubah mengikuti metode packaging yang digunakan.

---

## 🏗️ Arsitektur Build

### Linux ARM64

Target utama saat ini adalah:

```text
Fedora Linux
      │
      ├── Python 3.14
      ├── PySide6
      ├── PyGObject
      ├── GStreamer
      ├── Mutagen
      └── Nuitka
             │
             ▼
       Standalone Binary
             │
             ▼
      Portable GStreamer
             │
             ▼
          AppDir
             │
             ▼
          AppImage
```

Hasil:

```text
amarPlayer-Linux-aarch64.AppImage
```

AppImage membawa runtime GStreamer dan plugin yang diperlukan sehingga aplikasi dapat dijalankan sebagai paket portable.

---

# 🪟 Windows x64

Build Windows menggunakan **GitHub Actions** sehingga developer tidak membutuhkan komputer Windows untuk melakukan proses build.

Target:

```text
Windows 11
    │
    ├── Python 3.12 x64
    ├── PySide6
    ├── PyGObject
    ├── GStreamer 1.28.x
    ├── Mutagen
    └── Nuitka
           │
           ▼
      amarPlayer.exe
           │
           ▼
       Inno Setup
           │
           ▼
amarPlayer-Setup-Windows-x64.exe
```

Build dilakukan pada:

```text
GitHub Actions
        ↓
windows-2022
        ↓
x86-64 / AMD64
```

Pengguna akhir cukup menjalankan:

```text
amarPlayer-Setup-Windows-x64.exe
```

Tidak diperlukan:

* Python
* Nuitka
* Git
* GStreamer development tools
* Source code
* IDE

---

# 🍎 macOS

Target macOS difokuskan terutama pada Apple Silicon:

```text
Mac
 │
 ├── Apple Silicon
 │      ├── M1
 │      ├── M2
 │      ├── M3
 │      └── M4
 │
 └── ARM64
```

Target aplikasi:

```text
amarPlayer.app
```

Packaging macOS akan dikembangkan setelah build Linux ARM64 dan Windows x64 stabil.

---

# 🐧 Linux

Platform Linux merupakan salah satu target utama amarPlayer.

Target arsitektur:

```text
ARM64 / AArch64
x86-64 / AMD64
```

Distribusi utama:

```text
AppImage
```

Keuntungan AppImage:

* Portable
* Tidak membutuhkan instalasi package manager
* Mudah dipindahkan
* Dapat dijalankan dari file
* Cocok untuk distribusi aplikasi desktop Linux

---

# ⚙️ Teknologi

amarPlayer menggunakan:

| Teknologi      | Fungsi                           |
| -------------- | -------------------------------- |
| Python         | Bahasa pemrograman utama         |
| PySide6        | GUI desktop                      |
| Qt             | Framework antarmuka              |
| GStreamer      | Audio playback                   |
| PyGObject      | Binding GStreamer/GObject        |
| Mutagen        | Membaca metadata audio           |
| Pillow         | Pengolahan album art/icon        |
| Nuitka         | Kompilasi dan packaging aplikasi |
| AppImage       | Distribusi Linux                 |
| Inno Setup     | Installer Windows                |
| GitHub Actions | Automated build                  |

---

# 🎧 Format Audio

amarPlayer mendukung berbagai format audio melalui GStreamer:

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

Dukungan format sebenarnya bergantung pada plugin GStreamer yang tersedia pada build masing-masing platform.

---

# ✨ Fitur

### 🎵 Music Player

* Play
* Pause
* Stop
* Previous
* Next
* Seek
* Volume control
* Playlist
* Shuffle
* Repeat
* Drag & Drop audio
* Command-line file opening

### 🔎 Library & Playlist

* Scan file audio
* Playlist persistence
* Search
* Multiple audio formats
* Metadata audio
* Album artwork
* Persistent playlist

Playlist disimpan secara lokal.

Linux:

```text
~/.local/share/amarPlayer/amarPlayer_playlist.json
```

---

# 🎚️ Equalizer

amarPlayer menyediakan equalizer 10-band berbasis GStreamer:

```text
equalizer-10bands
```

Equalizer memungkinkan pengguna mengatur karakter suara secara manual.

---

# 🖼️ Album Art

Metadata dan artwork audio dapat dibaca menggunakan:

```text
Mutagen
+
Pillow
```

Album artwork ditampilkan langsung pada interface amarPlayer.

---

# 📂 Command Line

amarPlayer dapat menerima file audio melalui command line.

Contoh Linux:

```bash
./amarPlayer lagu.mp3
```

Beberapa file:

```bash
./amarPlayer lagu1.mp3 lagu2.mp3 lagu3.mp3
```

File audio akan dimasukkan ke playlist dan file yang sesuai akan diputar.

---

# 🖱️ Drag & Drop

File audio dapat ditambahkan ke amarPlayer dengan:

```text
Drag file
   ↓
Drop ke amarPlayer
   ↓
File masuk playlist
```

---

# 📦 Distribusi

## Linux

Output:

```text
amarPlayer-Linux-aarch64.AppImage
```

Contoh:

```bash
chmod +x amarPlayer-Linux-aarch64.AppImage
```

Kemudian:

```bash
./amarPlayer-Linux-aarch64.AppImage
```

---

## Windows

Output:

```text
amarPlayer-Setup-Windows-x64.exe
```

Installer menangani:

```text
Install amarPlayer
       ↓
Start Menu shortcut
       ↓
Desktop shortcut
       ↓
Application registration
```

---

# 🔨 Build System

Source code dikembangkan menggunakan Python.

Build production menggunakan **Nuitka**.

Linux:

```text
Python
 ↓
Nuitka
 ↓
Standalone
 ↓
GStreamer runtime
 ↓
AppDir
 ↓
AppImage
```

Windows:

```text
Python
 ↓
Nuitka
 ↓
Standalone
 ↓
GStreamer runtime
 ↓
Inno Setup
 ↓
Windows Installer
```

---

# 🤖 Automated Windows Build

Windows build dilakukan menggunakan:

```text
GitHub Actions
```

Workflow:

```text
.github/workflows/build-windows.yml
```

Proses:

```text
Checkout source
       ↓
Setup Python x64
       ↓
Install dependencies
       ↓
Install GStreamer
       ↓
Test PyGObject
       ↓
Test GStreamer
       ↓
Build dengan Nuitka
       ↓
Bundle GStreamer
       ↓
Build Inno Setup
       ↓
Upload artifact
```

Artifact:

```text
amarPlayer-Windows-x64
```

---

# 💻 Development Environment

Contoh lingkungan pengembangan Linux:

```text
OS       : Fedora Linux
CPU      : Apple M1
Architecture : AArch64
Python   : 3.14
GUI      : PySide6
Audio    : GStreamer
Compiler : Nuitka
```

Windows build tidak memerlukan komputer Windows karena proses build dilakukan oleh GitHub Actions.

---

# 📁 Struktur Project

```text
amarPlayer/
│
├── amarPlayer.py
├── amarPlayer.png
├── .gitignore
│
├── .github/
│   └── workflows/
│       └── build-windows.yml
│
└── README.md
```

File audio pribadi seperti:

```text
musik.mp3
```

tidak dimasukkan ke repository.

---

# 🔐 Repository

Source code:

**GitHub — xmuammar/amarPlayer**

```text
https://github.com/xmuammar/amarPlayer
```

Repository digunakan untuk:

* Source code
* Version control
* Issue tracking
* Windows build
* Release
* Pengembangan lintas platform

---

# 🚧 Status Pengembangan

### Linux ARM64

**Status: 🟢 Stabil / digunakan**

Target utama saat ini:

```text
Fedora Asahi Linux
+
Apple Silicon M1
+
ARM64
+
AppImage
```

### Windows x64

**Status: 🟡 Pengembangan**

Build otomatis menggunakan:

```text
GitHub Actions
+
Windows 2022
+
Python 3.12
+
Nuitka
+
GStreamer
+
Inno Setup
```

### macOS Apple Silicon

**Status: 🟡 Direncanakan**

### Linux x64

**Status: 🟡 Direncanakan**

### Windows ARM64

**Status: 🔵 Rencana jangka panjang**

---

# 🎯 Tujuan Project

amarPlayer dibuat dengan tujuan sederhana:

> **Membuat pemutar musik sendiri yang modern, ringan, portable, dan dapat digunakan di berbagai sistem operasi.**

Project ini juga menjadi eksperimen dalam:

```text
Python
+
GUI Development
+
Audio Processing
+
GStreamer
+
Nuitka
+
Application Packaging
+
Cross-platform Development
+
CI/CD
```

---

# 👨‍💻 Developer

**Muammar, SST, M.Kom**

Focus:

```text
Software Development
Data Science
Machine Learning
Web Development
Desktop Application
Cross-platform Application
```

---

# 📜 License

Lisensi project akan ditentukan pada tahap release publik.

---

## ⭐ amarPlayer

**Build it. Play it. Own it.**

🎵 **amarPlayer — Music Player buatan sendiri.**
