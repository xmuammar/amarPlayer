# amarPlayer 🎵

**amarPlayer** adalah pemutar musik desktop modern yang dikembangkan oleh **Muammar, SST, M.Kom** menggunakan Python, PySide6, GStreamer, dan Mutagen.

Aplikasi ini dirancang untuk menjadi pemutar musik desktop yang ringan, modern, sederhana, portable, dan dapat digunakan pada beberapa platform.

---

# 🖥️ Platform

| Platform         | Arsitektur            | Format           | Status          |
| ---------------- | --------------------- | ---------------- | --------------- |
| 🐧 Fedora Linux  | ARM64 / AArch64       | AppImage         | ✅ Aktif         |
| 🐧 Linux x64     | x86-64 / AMD64        | AppImage         | 🚧 Pengembangan |
| 🍎 macOS         | Apple Silicon / ARM64 | `.app`           | 🚧 Pengembangan |
| 🍎 macOS Intel   | x64                   | `.app`           | 🚧 Pengembangan |
| 🪟 Windows 11    | x64 / AMD64           | `.exe` Installer | 🚧 Pengembangan |
| 🪟 Windows ARM64 | ARM64                 | `.exe`           | 🔮 Rencana      |

---

# ✨ Fitur

* 🎵 Play / Pause / Stop
* ⏮ Previous / Next
* 🔊 Volume control
* 🔀 Shuffle
* 🔁 Repeat
* 📋 Playlist
* 🔎 Search
* 🎨 Album artwork
* 🏷️ Audio metadata
* 🎚️ 10-band equalizer
* 🖱️ Drag & Drop
* 📂 Scan folder
* 💾 Playlist persistence
* ⌨️ Command-line file opening
* 🎧 MP3, FLAC, WAV, OGG, OPUS, M4A, AAC, dan format lainnya
* 📦 Portable AppImage pada Linux
* 🪟 Windows installer
* 🤖 Automated Windows build melalui GitHub Actions

---

# 📦 Instalasi

## 🐧 Linux — AppImage

Untuk Linux, amarPlayer didistribusikan dalam bentuk **AppImage**.

Contoh file:

```text
amarPlayer-Linux-aarch64.AppImage
```

### 1. Download AppImage

Download file AppImage dari halaman **Releases** repository GitHub.

Setelah selesai, masuk ke folder tempat file berada:

```bash
cd ~/Downloads
```

### 2. Berikan permission executable

```bash
chmod +x amarPlayer-Linux-aarch64.AppImage
```

### 3. Jalankan

```bash
./amarPlayer-Linux-aarch64.AppImage
```

amarPlayer kemudian dapat digunakan tanpa instalasi package tambahan.

---

## 🐧 Fedora Linux

Pada Fedora ARM64, AppImage dapat dijalankan langsung:

```bash
chmod +x amarPlayer-Linux-aarch64.AppImage
./amarPlayer-Linux-aarch64.AppImage
```

Tidak diperlukan:

```text
Python
Nuitka
Git
Compiler
GStreamer development package
```

karena dependency aplikasi dibundel ke dalam paket distribusi.

---

# 🪟 Windows 11

Untuk pengguna Windows, gunakan installer:

```text
amarPlayer-Setup-Windows-x64.exe
```

### 1. Download installer

Download:

```text
amarPlayer-Setup-Windows-x64.exe
```

dari halaman **Releases** atau artifact build yang tersedia.

### 2. Jalankan installer

Klik dua kali:

```text
amarPlayer-Setup-Windows-x64.exe
```

Jika Windows menampilkan peringatan keamanan karena aplikasi belum memiliki tanda tangan digital, pilih opsi untuk melanjutkan hanya jika file diperoleh dari sumber resmi project.

### 3. Ikuti proses instalasi

Installer akan memasang amarPlayer ke komputer.

Secara umum:

```text
Installer
   ↓
amarPlayer
   ↓
Start Menu
   ↓
Desktop Shortcut
```

### 4. Jalankan

Setelah instalasi selesai, amarPlayer dapat dijalankan melalui:

```text
Start Menu → amarPlayer
```

atau shortcut Desktop.

---

# 🍎 macOS

Dukungan macOS masih dalam tahap pengembangan.

Target utama:

```text
Apple Silicon
M1
M2
M3
M4
```

Distribusi nantinya ditargetkan dalam bentuk:

```text
amarPlayer.app
```

Panduan instalasi macOS akan ditambahkan setelah build macOS stabil.

---

# ▶️ Menjalankan amarPlayer

## Linux

Jika menggunakan AppImage:

```bash
./amarPlayer-Linux-aarch64.AppImage
```

Jika executable hasil build tersedia:

```bash
./amarPlayer
```

---

## Windows

Jalankan:

```text
amarPlayer.exe
```

atau gunakan shortcut:

```text
Start Menu → amarPlayer
```

---

# 🎵 Menambahkan Musik

Ada beberapa cara untuk menambahkan musik.

## Cara 1 — Drag & Drop

Buka amarPlayer kemudian tarik file musik ke jendela aplikasi.

Contoh:

```text
File Manager
     │
     ├── lagu1.mp3
     ├── lagu2.flac
     └── lagu3.wav
            │
            ▼
       amarPlayer
```

File akan masuk ke playlist.

---

## Cara 2 — Scan Folder

Gunakan fungsi scan/library yang tersedia pada interface amarPlayer untuk mencari file audio dalam folder.

Contoh struktur:

```text
Music/
├── Album 1/
│   ├── lagu1.mp3
│   └── lagu2.mp3
│
├── Album 2/
│   ├── lagu3.flac
│   └── lagu4.mp3
│
└── Album 3/
    └── lagu5.ogg
```

---

## Cara 3 — Command Line

amarPlayer dapat menerima file audio dari command line.

Contoh:

```bash
./amarPlayer lagu.mp3
```

Beberapa file:

```bash
./amarPlayer lagu1.mp3 lagu2.mp3 lagu3.mp3
```

Dengan AppImage:

```bash
./amarPlayer-Linux-aarch64.AppImage lagu.mp3
```

Beberapa file:

```bash
./amarPlayer-Linux-aarch64.AppImage \
    lagu1.mp3 \
    lagu2.mp3 \
    lagu3.mp3
```

File akan ditambahkan ke playlist dan file yang sesuai akan diputar.

---

# 📂 Membuka Musik dari File Manager

Pada Linux, amarPlayer dapat didaftarkan sebagai aplikasi pembuka file audio.

Contohnya:

```text
Klik kanan lagu.mp3
        ↓
Open With
        ↓
amarPlayer
```

Jika amarPlayer telah ditetapkan sebagai aplikasi default, cukup klik dua kali file audio:

```text
lagu.mp3
     ↓
amarPlayer
     ↓
Play
```

---

# 🎧 Format Audio

amarPlayer menggunakan GStreamer sebagai engine audio.

Format yang ditargetkan:

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

Dukungan aktual bergantung pada plugin GStreamer yang tersedia pada build masing-masing platform.

---

# 🎚️ Equalizer

amarPlayer menyediakan equalizer 10-band.

Engine:

```text
GStreamer
    ↓
equalizer-10bands
```

Equalizer dapat digunakan untuk menyesuaikan karakter suara sesuai preferensi pengguna.

---

# 🔀 Shuffle

Mode Shuffle dapat digunakan untuk memutar playlist secara acak.

Contoh:

```text
Playlist:

01. Lagu A
02. Lagu B
03. Lagu C
04. Lagu D

Shuffle:

03 → 01 → 04 → 02
```

---

# 🔁 Repeat

Mode Repeat digunakan untuk mengatur pengulangan pemutaran.

Tergantung mode yang tersedia pada aplikasi:

```text
Repeat Off
Repeat Playlist
Repeat Track
```

---

# 🔊 Volume

Volume dapat dikontrol langsung dari interface amarPlayer.

Pengguna dapat menyesuaikan volume tanpa mengubah volume sistem.

---

# 🔎 Search

Gunakan fitur pencarian untuk menemukan lagu dalam playlist/library.

Contoh:

```text
Search:
"India"
```

akan membantu menemukan lagu yang metadata atau judulnya mengandung kata tersebut.

---

# 🖼️ Album Artwork

amarPlayer membaca metadata dan artwork menggunakan:

```text
Mutagen
+
Pillow
```

Jika file audio mempunyai cover album yang tertanam dalam metadata, artwork dapat ditampilkan pada interface.

Contoh:

```text
song.mp3
   │
   ├── Title
   ├── Artist
   ├── Album
   └── Album Artwork
```

---

# 💾 Playlist Persistence

Playlist amarPlayer disimpan secara lokal sehingga playlist dapat dipertahankan ketika aplikasi ditutup.

Pada Linux:

```text
~/.local/share/amarPlayer/amarPlayer_playlist.json
```

File ini tidak berada di dalam AppImage.

Artinya:

```text
AppImage
   ≠
Playlist
```

Mengganti atau memperbarui AppImage tidak secara otomatis menghapus playlist pengguna.

---

# 🗂️ Lokasi Data Pengguna

Linux:

```text
~/.local/share/amarPlayer/
```

Contoh:

```text
~/.local/share/amarPlayer/
└── amarPlayer_playlist.json
```

Pada Windows dan macOS, lokasi data pengguna akan mengikuti mekanisme penyimpanan data platform masing-masing pada build final.

---

# 🛠️ Troubleshooting

## AppImage tidak bisa dijalankan

Pastikan executable permission sudah diberikan:

```bash
chmod +x amarPlayer-Linux-aarch64.AppImage
```

Kemudian:

```bash
./amarPlayer-Linux-aarch64.AppImage
```

---

## Tidak ada suara

Periksa terlebih dahulu output audio sistem.

Pada Linux, amarPlayer menggunakan GStreamer dan audio system seperti:

```text
PipeWire
PulseAudio
ALSA
```

Pastikan perangkat audio sistem berfungsi normal.

---

## File MP3 tidak bisa diputar

Pastikan file tidak rusak.

Tes file menggunakan GStreamer:

```bash
gst-launch-1.0 playbin uri="file:///path/ke/lagu.mp3"
```

Jika menggunakan AppImage portable, gunakan build resmi amarPlayer yang menyediakan GStreamer runtime.

---

## Playlist hilang

Periksa:

```bash
ls ~/.local/share/amarPlayer/
```

Kemudian:

```bash
cat ~/.local/share/amarPlayer/amarPlayer_playlist.json
```

---

# 🧑‍💻 Untuk Developer

Clone repository:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
```

Masuk ke directory:

```bash
cd amarPlayer
```

---

# 🐍 Menjalankan dari Source

Install dependency:

```bash
python3 -m pip install PySide6 mutagen Pillow
```

Kemudian jalankan:

```bash
python3 amarPlayer.py
```

Untuk development Linux, GStreamer dan PyGObject juga harus tersedia pada sistem.

---

# 🔨 Build Linux

Build standalone menggunakan Nuitka:

```bash
python3 -m nuitka \
    --mode=standalone \
    --enable-plugin=pyside6 \
    --follow-imports \
    --output-dir=dist \
    --output-filename=amarPlayer \
    --product-name="amarPlayer" \
    --file-description="Modern Music Player" \
    --company-name="Muammar" \
    amarPlayer.py
```

Output:

```text
dist/
└── amarPlayer.dist/
    └── amarPlayer
```

---

# 🪟 Build Windows

Windows build dilakukan melalui GitHub Actions.

Workflow:

```text
.github/workflows/build-windows.yml
```

Workflow melakukan:

```text
Checkout
   ↓
Python 3.12 x64
   ↓
PySide6
   ↓
PyGObject
   ↓
GStreamer
   ↓
Mutagen
   ↓
Pillow
   ↓
Nuitka
   ↓
Standalone application
   ↓
GStreamer bundle
   ↓
Inno Setup
   ↓
Windows Installer
```

Output:

```text
amarPlayer-Setup-Windows-x64.exe
```

---

# 📦 Release

Release production akan menyediakan paket sesuai platform:

```text
Linux ARM64
amarPlayer-Linux-aarch64.AppImage

Linux x64
amarPlayer-Linux-x86_64.AppImage

Windows x64
amarPlayer-Setup-Windows-x64.exe

macOS Apple Silicon
amarPlayer-macOS-arm64.app
```

Nama file dapat berubah mengikuti versi release.

---

# 📁 Struktur Project

```text
amarPlayer/
│
├── amarPlayer.py
├── amarPlayer.png
├── README.md
├── .gitignore
│
└── .github/
    └── workflows/
        └── build-windows.yml
```

File musik pribadi seperti:

```text
musik.mp3
```

tidak dimasukkan ke repository.

---

# 🤖 CI/CD

Windows build menggunakan:

```text
GitHub Actions
```

Runner:

```text
windows-2022
```

Arsitektur:

```text
x86-64 / AMD64
```

Build dilakukan secara otomatis berdasarkan workflow yang berada di:

```text
.github/workflows/build-windows.yml
```

---

# 🏗️ Teknologi

| Teknologi      | Fungsi                    |
| -------------- | ------------------------- |
| Python         | Bahasa pemrograman        |
| PySide6        | GUI                       |
| Qt             | Desktop UI                |
| PyGObject      | GObject/GStreamer binding |
| GStreamer      | Audio engine              |
| Mutagen        | Metadata audio            |
| Pillow         | Image processing          |
| Nuitka         | Application compilation   |
| AppImage       | Linux distribution        |
| Inno Setup     | Windows installer         |
| Git            | Version control           |
| GitHub Actions | CI/CD                     |

---

# 🖥️ Arsitektur

```text
Linux
├── ARM64 / AArch64
└── x86-64 / AMD64

Windows
├── x64 / AMD64
└── ARM64 (planned)

macOS
├── Apple Silicon / ARM64
└── Intel / x86-64
```

---

# 🚧 Status Pengembangan

| Platform            | Status          |
| ------------------- | --------------- |
| Fedora ARM64        | 🟢 Aktif        |
| Linux ARM64         | 🟢 Aktif        |
| Linux x64           | 🟡 Pengembangan |
| Windows x64         | 🟡 Pengembangan |
| macOS Apple Silicon | 🟡 Pengembangan |
| macOS Intel         | 🔵 Rencana      |
| Windows ARM64       | 🔵 Rencana      |

---

# 🎯 Tujuan Project

amarPlayer dibuat dengan tujuan:

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

# ⭐ amarPlayer

**Build it. Play it. Own it.**

🎵 **amarPlayer — Music Player buatan sendiri.**
