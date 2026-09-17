# amarPlayer

**[⬇ Download APK, RPM, DEB, dan AppImage](download/README.md)**

Paket instalasi tersedia di folder [`download/`](download/). Windows EXE belum tersedia.
Installation packages are available in [`download/`](download/); Windows EXE is not available yet.

**Pemutar Musik Modern Berbasis Python, PySide6, GStreamer & QtMultimedia**

**Modern Music Player Built with Python, PySide6, GStreamer & QtMultimedia**

---

## Download / Unduh

| Platform | Paket / Package | Status |
| --- | --- | --- |
| Android ARM64 | [APK debug](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-android-arm64-debug.apk) | Startup dan pemutaran MP3 diuji / Startup and MP3 playback tested |
| Fedora 44 | [RPM noarch](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-1.0.0-1.fc44.noarch.rpm) | Versi / Version 1.0.0 |
| Debian / Ubuntu | [DEB](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarplayer_1.0.0-1_all.deb) | Versi / Version 1.0.0 |
| Linux ARM64 | [AppImage](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-Linux-aarch64.AppImage) | aarch64 |
| Windows | EXE | Belum tersedia / Not available yet |

Ukuran file, checksum, dan petunjuk Git LFS tersedia di [panduan download](download/README.md).
File sizes, checksums, and Git LFS instructions are available in the [download guide](download/README.md).

### Instalasi / Installation

Unduh paket yang sesuai, lalu jalankan perintah berikut dari folder unduhan.
Download the matching package, then run the appropriate command from your downloads folder.

```bash
# Fedora 44
sudo dnf install ./amarPlayer-1.0.0-1.fc44.noarch.rpm

# Debian / Ubuntu
sudo apt install ./amarplayer_1.0.0-1_all.deb

# Linux ARM64
chmod +x amarPlayer-Linux-aarch64.AppImage
./amarPlayer-Linux-aarch64.AppImage

# Android ARM64 via ADB
adb -s DEVICE install -r amarPlayer-android-arm64-debug.apk
```

APK juga dapat dibuka langsung di HP untuk instalasi. Android masih berupa debug build eksperimental; paket desktop merupakan build yang sudah tersedia sebelumnya.
You can also open the APK on your phone to install it. Android remains an experimental debug build; desktop packages are previously available builds.

## Bahasa / Language

* [🇮🇩 Bahasa Indonesia](#-bahasa-indonesia)
* [🇬🇧 English](#-english)

---

# 🇮🇩 Bahasa Indonesia

## Tentang amarPlayer

**amarPlayer** adalah aplikasi pemutar musik open-source yang dikembangkan menggunakan **Python dan PySide6**.

Proyek ini awalnya dibuat sebagai pemutar musik desktop untuk Linux dengan **GStreamer** sebagai backend audio.

Dalam perkembangannya, amarPlayer mulai dikembangkan menjadi aplikasi lintas platform, termasuk eksperimen porting ke **Android ARM64** menggunakan **PySide6 QtMultimedia**.

amarPlayer tetap mempertahankan source desktop utama, sementara versi Android dikembangkan secara terpisah agar perubahan khusus Android tidak merusak versi desktop yang sudah berjalan.

---

# Status Proyek

| Platform          | Status                    | Keterangan                 |
| ----------------- | ------------------------- | -------------------------- |
| Linux Desktop     | ✅ Berjalan                | Versi desktop utama        |
| Fedora            | ✅ Berjalan                | RPM berhasil dibuat        |
| Fedora COPR       | ✅ Berhasil                | x86_64 dan aarch64         |
| Debian / Ubuntu   | ✅ Package berhasil dibuat | `.deb` tersedia            |
| Android ARM64     | 🧪 Eksperimental          | APK debug ARM64 berhasil dibuat |
| Instalasi Android | ✅ Berhasil                | APK dapat dipasang melalui ADB |
| Android Runtime   | ✅ Teruji                  | Scan folder, playlist, dan playback diuji pada perangkat ARM64 |
| Windows           | 🚧 Eksperimental          | Pengembangan berikutnya    |

---

# Fitur Utama

## Pemutar Musik

amarPlayer menyediakan kontrol pemutaran musik seperti:

* Play
* Pause
* Next
* Previous
* Seek
* Volume mengikuti kontrol sistem perangkat
* Shuffle
* Repeat

---

## Playlist

Fitur playlist meliputi:

* Menambahkan file musik
* Menambahkan banyak lagu sekaligus
* Menghapus lagu
* Memilih lagu
* Menyimpan playlist
* Membuka kembali playlist
* Mencari lagu

---

## Metadata Audio

amarPlayer dapat membaca informasi metadata lagu seperti:

* Judul
* Artist
* Album
* Durasi
* Metadata audio
* Album artwork

Metadata diproses menggunakan library seperti **Mutagen**.

---

## Album Artwork

Jika file musik memiliki cover album di dalam metadata, amarPlayer dapat menampilkannya pada antarmuka aplikasi.

Pemrosesan gambar dapat menggunakan **Pillow**.

---

## Pencarian

Playlist memiliki fitur pencarian untuk menemukan lagu dengan cepat tanpa harus menggulir seluruh daftar musik.

---

## Shuffle dan Repeat

amarPlayer mendukung:

* Normal playback
* Shuffle
* Repeat

---

## Equalizer 10-Band

Versi Linux memiliki antarmuka **equalizer 10-band**.

Pada versi Android, panel equalizer desktop tidak ditampilkan. Backend QtMultimedia Android belum menyediakan DSP 10-band yang sama seperti desktop.

---

# Status Android Terbaru

Port Android menggunakan `main.py` sebagai entry point dan menjalankan modul `amarPlayer_android` dari bytecode APK. Build memakai Python 3.11, PySide6 6.11.2, Shiboken6, QtMultimedia, dan arsitektur `arm64-v8a`.

Perbaikan Android yang sudah diterapkan:

* Play, pause, previous, next, shuffle, repeat, volume, dan seek terhubung ke `QMediaPlayer`.
* File lokal Android disalin ke cache aplikasi sebelum diputar agar kompatibel dengan scoped storage.
* Playlist disimpan di `AppDataLocation/amarPlayer/amarPlayer_playlist.json`.
* Android menyediakan tombol `Scan` tunggal; pemindaian dibatasi ke folder `mp3`, `Music`, dan `Download` yang diizinkan aplikasi.
* Izin `READ_MEDIA_AUDIO` (Android 13+) atau `READ_EXTERNAL_STORAGE` diminta otomatis melalui Activity native `AmarPlayerActivity` saat startup pertama tanpa modul Kivy `android.permissions`.
* Teks lagu yang terpilih pada playlist berlatar kontras tinggi dengan warna teks putih agar mudah terbaca.
* Layout player berubah vertikal pada layar sempit dan tinggi baris playlist dibuat tetap agar teks tidak bertumpuk.
* Playlist memakai pixel scrolling dan kinetic scrolling agar swipe terasa halus. Geser untuk scroll tidak memutar lagu; tap yang selesai tanpa drag pada item yang sama baru memulai playback.
* Volume internal tidak ditampilkan; keluaran aplikasi menggunakan level penuh dan volume diatur dengan tombol speaker HP.

Format yang dipindai dan diputar pada Android dibatasi ke MP3 agar hasil scan dan playback konsisten.

## Build Android di Fedora Asahi

Build dilakukan tanpa menghapus cache `.buildozer`:

```bash
export ANDROIDNDK="$HOME/.android-ndk-arm64/r29"
export ANDROID_NDK_HOME="$ANDROIDNDK"
export ANDROID_NDK_ROOT="$ANDROIDNDK"
export JAVA_HOME="$HOME/.jdk/jdk-21"
export PATH="$JAVA_HOME/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export LD_LIBRARY_PATH="$HOME/.android-ndk-arm64/compat${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
buildozer -v android debug
```

Pada host Fedora dengan page size 16K, Gradle dapat perlu dijalankan melalui `muvm` dan memakai override AAPT2 yang tercantum di `CHAT_CONTEXT.md`. Arsip build lokal berada di `bin/`; APK publik tersedia di `download/`. Instalasi menggunakan endpoint ADB eksplisit:

```bash
adb -s DEVICE install -r download/amarPlayer-android-arm64-debug.apk
```

Build Android terbaru memakai distribution Qt minimal yang hanya membawa
library Core, Gui, Widgets, Multimedia, Network, Concurrent, codec FFmpeg,
serta stub SSL dan crypto yang dibutuhkan FFmpeg. APK perbaikan publik berada di
`download/amarPlayer-android-arm64-debug.apk` (115,62 MiB / sekitar 121 MB).
Build optimized sebelumnya kehilangan stub SSL sehingga aplikasi menutup saat startup;
kedua stub sudah ditambahkan dan build perbaikan telah diuji di HP.

---

# Format Audio

Android hanya memindai dan memutar file **MP3**. Dukungan format desktop mengikuti backend GStreamer dan codec yang tersedia pada sistem.

---

# Teknologi

## Linux Desktop

Versi desktop menggunakan:

* Python
* PySide6
* Qt
* PyGObject
* GStreamer
* Mutagen
* Pillow

Arsitektur sederhananya:

```text
Python
   │
   ├── PySide6 / Qt
   │      └── Antarmuka Desktop
   │
   ├── GStreamer
   │      └── Pemutaran Audio
   │
   ├── Mutagen
   │      └── Metadata Audio
   │
   └── Pillow
          └── Album Artwork
```

---

## Android

Port Android menggunakan:

* Python
* PySide6
* Qt
* QtMultimedia
* python-for-android
* Buildozer
* Android SDK
* Android NDK
* Gradle
* Java 21

Arsitektur:

```text
Android
   │
   └── Qt / PySide6
          │
          ├── QtMultimedia
          │      └── Audio Playback
          │
          ├── Python
          │      └── Logic Aplikasi
          │
          └── Qt Android Platform
```

GStreamer pada versi Android telah digantikan dengan **QtMultimedia**.

---

# Struktur Source Code

```text
amarPlayer/
│
├── amarPlayer.py
│   └── Aplikasi desktop utama
│
├── amarPlayer_android.py
│   └── Versi Android
│
├── main.py
│   └── Entry point Android
│
├── amarPlayer.png
│   └── Icon aplikasi
│
├── README.md
│
├── buildozer.spec
│   └── Konfigurasi Android
│
├── pysidedeploy.spec
│
├── deployment/
│   ├── recipes/
│   └── jar/
│
├── packaging/
│   ├── fedora/
│   └── debian/
│
├── android-wheels/
│   └── PySide6 / Shiboken Android wheels
│
├── download/
│   └── APK, RPM, DEB, AppImage (Git LFS), README, SHA256SUMS
│
├── bin/
│   └── Hasil build lokal
│
└── .buildozer/
    └── Cache build Android
```

---

# Menjalankan amarPlayer di Linux

Clone repository:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
cd amarPlayer
```

Install library Python:

```bash
python3 -m pip install PySide6 mutagen Pillow
```

Kemudian jalankan:

```bash
python3 amarPlayer.py
```

---

# Dependency Fedora

Contoh dependency:

```bash
sudo dnf install \
python3 \
python3-gobject \
python3-gstreamer1 \
gstreamer1 \
gstreamer1-plugins-base \
gstreamer1-plugins-good \
gstreamer1-plugins-bad-free \
gstreamer1-plugin-mpg123
```

---

# Fedora RPM

amarPlayer telah berhasil dibuat menjadi package RPM.

Contoh hasil build:

```text
amarPlayer-1.0.0-1.fc44.noarch.rpm
amarPlayer-1.0.0-1.fc44.src.rpm
```

RPM mencakup:

* amarPlayer
* Desktop launcher
* Icon aplikasi
* MIME association
* Dokumentasi README

---

# Fedora COPR

Build amarPlayer melalui Fedora COPR telah berhasil untuk:

```text
x86_64
aarch64
```

---

# Debian Package

Package Debian juga telah berhasil dibuat:

```text
amarplayer_1.0.0-1_all.deb
```

Konfigurasi Debian berada pada:

```text
packaging/debian/
```

---

# Android Port

Versi Android merupakan **port dari amarPlayer**, bukan aplikasi baru yang dibuat dari nol.

Tujuannya adalah mempertahankan sebanyak mungkin:

* Antarmuka PySide6
* Logic playlist
* Metadata
* Artwork
* Sistem pencarian
* Struktur aplikasi

sambil mengganti komponen yang tidak kompatibel dengan Android.

---

## QtMultimedia

Pada Android, backend GStreamer diganti menjadi:

```python
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
```

Komponen utama:

```text
QMediaPlayer
QAudioOutput
```

---

## Penyimpanan Android

Data internal aplikasi menggunakan:

```python
QStandardPaths.AppDataLocation
```

agar sesuai dengan sistem penyimpanan Android.

---

## Content URI Android

Android sering memberikan file dengan URI:

```text
content://...
```

bukan path Linux biasa.

Versi Android amarPlayer telah mulai mendukung:

* `content://`
* Android file picker
* Local cache
* Persiapan file sebelum playback

---

# Build Android ARM64

APK Android ARM64 pertama berhasil dibuat menggunakan:

```text
Fedora Asahi Remix
Apple Silicon
ARM64 / aarch64
```

Target APK:

```text
arm64-v8a
```

Konfigurasi utama:

```text
Android API      : 36
Minimum API      : 24
Architecture     : arm64-v8a
Java             : JDK 21
Android NDK      : r29
```

---

# Fedora Asahi dan Apple Silicon

Mesin build menggunakan:

```text
Architecture : aarch64
Page Size    : 16384 bytes / 16 KB
```

Beberapa Android SDK tools dari Google hanya tersedia sebagai binary Linux:

```text
x86_64
```

Salah satu yang paling penting adalah:

```text
aapt2
```

---

# Native Android NDK ARM64

Untuk menghindari ketergantungan penuh terhadap emulator x86_64, digunakan Android NDK ARM64 native.

Versi:

```text
Android NDK r29
```

Toolchain yang berhasil dijalankan secara native antara lain:

```text
clang
ld.lld
llvm-ar
llvm-strip
llvm-ranlib
```

---

# Masalah AAPT2

AAPT2 Android SDK merupakan binary x86_64.

Menjalankannya langsung melalui FEX pada host Fedora Asahi dengan page size 16 KB menyebabkan masalah.

Solusi yang berhasil adalah menjalankan proses Gradle di dalam:

```text
muvm
```

Host:

```text
Page Size = 16384
```

Di dalam muvm:

```text
Page Size = 4096
```

Arsitektur build akhirnya:

```text
Fedora Asahi ARM64
        │
        ▼
      muvm
   Page Size 4K
        │
        ▼
      Gradle
        │
        ▼
      AAPT2
        │
        ▼
       APK
```

Pengujian daemon AAPT2 berhasil menghasilkan:

```text
Ready
Exiting daemon
```

---

# APK Android Pertama

Build Android pertama yang berhasil menghasilkan:

```text
amarPlayer-debug.apk
```

Ukuran sekitar:

```text
174 MB
```

Lokasi asli:

```text
.buildozer/android/platform/build-arm64-v8a/
dists/amarPlayer/build/outputs/apk/debug/
amarPlayer-debug.apk
```

Salinan lokal dapat ditempatkan di:

```text
bin/
```

---

# Status Android Saat Ini

Terakhir diuji pada 17 September 2026 menggunakan HP ARM64 model 2510DRA23E.

| Pemeriksaan | Hasil |
| --- | --- |
| Instalasi pembaruan APK | Berhasil, data aplikasi dipertahankan |
| Startup Python dan Qt | Berhasil; library FFmpeg dimuat |
| Tampilan aplikasi | Header, tombol Scan, kontrol player, dan playlist tampil |
| Pemutaran MP3 | Satu tap memulai playback; waktu berjalan dan AudioTrack aktif menuju speaker |

Masalah layar putih pada build lama dan kegagalan startup akibat library SSL FFmpeg yang hilang sudah diperbaiki. Lagu dijeda setelah pengujian; suara tidak diverifikasi melalui pendengaran.

Izin media sudah diberikan pada perangkat pengujian. Alur permintaan izin pada instalasi baru belum tervalidasi; log masih mencatat modul `android.permissions` tidak tersedia. Scan dibatasi ke folder `mp3`, `Music`, dan `Download` yang dapat diakses aplikasi.

---

# Debug Android Tanpa Kabel

amarPlayer dapat di-debug menggunakan:

```text
Wireless ADB
```

Pair perangkat:

```bash
adb pair IP_ADDRESS:PAIRING_PORT
```

Hubungkan:

```bash
adb connect IP_ADDRESS:DEBUG_PORT
```

Periksa perangkat:

```bash
adb devices
```

Lihat log:

```bash
adb logcat
```

Wireless ADB digunakan untuk memeriksa startup, interaksi UI, dan log playback pada perangkat.

---

# Build Cache

Build Android menghasilkan cache yang cukup besar:

```text
.buildozer/
```

Ukuran cache dapat melebihi:

```text
4 GB
```

Cache ini sengaja dipertahankan agar dependency yang sudah berhasil dikompilasi tidak perlu dibuat ulang.

Folder tersebut sebaiknya tidak dimasukkan ke GitHub.

---

# Git

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

Clone:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
```

Workflow Git:

```bash
git add README.md download/ .gitattributes .gitignore
git commit -m "Update amarPlayer"
git push origin main
```

Paket publik di `download/` disimpan melalui **Git LFS**, termasuk APK. Pasang Git LFS dan jalankan `git lfs install` sebelum clone; gunakan `git lfs pull --include="download/*"` untuk mengambil paket pada clone yang sudah ada. Arsip build lain dan cache tetap lokal. Tambahkan file source yang diubah secara eksplisit saat commit.

---

# Milestone

## Linux

```text
Desktop Application       ✅
PySide6 GUI               ✅
GStreamer                 ✅
Playlist                  ✅
Metadata                  ✅
Album Artwork             ✅
Search                    ✅
Shuffle                   ✅
Repeat                    ✅
10-Band Equalizer         ✅
```

## Packaging

```text
Fedora RPM                ✅
Fedora SRPM               ✅
Fedora COPR x86_64        ✅
Fedora COPR aarch64       ✅
Debian Package            ✅
```

## Android

```text
Android Port              ✅
PySide6 Android Wheels    ✅
QtMultimedia              ✅
Content URI               ⚠️ Not fully validated
Native ARM64 NDK          ✅
Python ARM64              ✅
Qt / PySide6 Packaging    ✅
JDK 21                    ✅
Gradle                    ✅
AAPT2 + muvm              ✅
APK Generation            ✅
APK Installation          ✅
Application Launch        ✅
Android UI                ✅ Tested
MP3 Playback              ✅ Tested
```

---

# Roadmap

1. Memvalidasi dan memperbaiki permintaan izin media pada instalasi Android baru.
2. Menguji scan, playlist, playback, dan kontrol player pada lebih banyak perangkat.
3. Memvalidasi metadata, album artwork, dan penanganan `content://`.
4. Menyiapkan release Android stabil dengan penandatanganan release.
5. Melanjutkan dukungan Windows dan menyediakan installer EXE setelah diuji.

---

# Filosofi Pengembangan

amarPlayer bermula sebagai proyek pemutar musik pribadi di Linux.

Seiring perkembangan proyek, amarPlayer menjadi eksperimen lintas platform untuk mempelajari bagaimana aplikasi Python/PySide6 dapat berjalan di berbagai sistem operasi.

Versi desktop tetap dipertahankan sebagai versi utama, sementara Android dikembangkan secara bertahap tanpa mengorbankan source desktop yang sudah berjalan.

---

# Lisensi

amarPlayer menggunakan:

**MIT License**

---

# Developer

**Muammar**

GitHub:

```text
https://github.com/xmuammar
```

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

---

# Ringkasan

```text
Linux Desktop        ✅
Fedora RPM           ✅
Fedora COPR          ✅
Debian Package       ✅
Android ARM64 APK    ✅
Install Android      ✅
Android UI           ✅ Teruji
Android MP3          ✅ Playback teruji
```

Target berikutnya adalah memvalidasi izin media pada instalasi baru dan menguji stabilitas pada lebih banyak perangkat Android.

---

---

# 🇬🇧 English

## About amarPlayer

**amarPlayer** is an open-source music player developed with **Python and PySide6**.

The project originally started as a Linux desktop music player using **GStreamer** as its audio backend.

It has gradually evolved into a cross-platform project, including an experimental **Android ARM64** port using **PySide6 QtMultimedia**.

The original desktop source is preserved while Android-specific development is maintained separately to prevent Android changes from breaking the working Linux desktop version.

---

# Project Status

| Platform             | Status          | Notes                            |
| -------------------- | --------------- | -------------------------------- |
| Linux Desktop        | ✅ Working       | Main desktop version             |
| Fedora               | ✅ Working       | RPM successfully built           |
| Fedora COPR          | ✅ Working       | x86_64 and aarch64               |
| Debian / Ubuntu      | ✅ Package Built | `.deb` available                 |
| Android ARM64        | 🧪 Experimental | APK successfully built           |
| Android Installation | ✅ Working       | APK installs successfully        |
| Android Runtime      | ✅ Tested       | Folder scan, playlist, and playback tested on ARM64 device |
| Windows              | 🚧 Experimental | Future development               |

---

# Main Features

## Music Playback

amarPlayer provides:

* Play
* Pause
* Next
* Previous
* Seek
* Volume controlled by the device system
* Shuffle
* Repeat

---

## Playlist Management

Playlist functionality includes:

* Add music files
* Add multiple tracks
* Remove tracks
* Select tracks
* Save playlists
* Restore playlists
* Search tracks

---

## Audio Metadata

amarPlayer can read:

* Title
* Artist
* Album
* Duration
* Audio metadata
* Album artwork

Metadata processing is handled using libraries such as **Mutagen**.

---

## Album Artwork

If embedded album artwork exists inside the audio file, amarPlayer can display it in the player interface.

Image processing can be handled through **Pillow**.

---

## Search

The playlist can be searched to quickly locate tracks.

---

## Shuffle and Repeat

amarPlayer supports:

* Normal playback
* Shuffle
* Repeat

---

## 10-Band Equalizer

The Linux version includes a **10-band equalizer** interface.

The equalizer interface is desktop-only; Android QtMultimedia does not provide the same 10-band DSP processing.

---

# Supported Audio Formats

Android scanning and playback are intentionally limited to MP3 for consistent results.

Supported Android format:

* MP3

Actual support depends on the multimedia backend and installed codecs.

---

# Technology Stack

## Linux Desktop

The desktop version uses:

* Python
* PySide6
* Qt
* PyGObject
* GStreamer
* Mutagen
* Pillow

Architecture:

```text
Python
   │
   ├── PySide6 / Qt
   │      └── Desktop GUI
   │
   ├── GStreamer
   │      └── Audio Playback
   │
   ├── Mutagen
   │      └── Audio Metadata
   │
   └── Pillow
          └── Album Artwork
```

---

## Android

The Android port uses:

* Python
* PySide6
* Qt
* QtMultimedia
* python-for-android
* Buildozer
* Android SDK
* Android NDK
* Gradle
* Java 21

Architecture:

```text
Android
   │
   └── Qt / PySide6
          │
          ├── QtMultimedia
          │      └── Audio Playback
          │
          ├── Python
          │      └── Application Logic
          │
          └── Qt Android Platform
```

GStreamer was replaced by **QtMultimedia** for Android.

---

# Source Structure

```text
amarPlayer/
│
├── amarPlayer.py
│   └── Main desktop application
│
├── amarPlayer_android.py
│   └── Android port
│
├── main.py
│   └── Android entry point
│
├── amarPlayer.png
│
├── README.md
│
├── buildozer.spec
│
├── pysidedeploy.spec
│
├── deployment/
│
├── packaging/
│   ├── fedora/
│   └── debian/
│
├── android-wheels/
│
├── download/
│   └── APK, RPM, DEB, AppImage (Git LFS), README, SHA256SUMS
│
├── bin/
│
└── .buildozer/
```

---

# Running on Linux

Clone:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
cd amarPlayer
```

Install Python dependencies:

```bash
python3 -m pip install PySide6 mutagen Pillow
```

Run:

```bash
python3 amarPlayer.py
```

---

# Fedora Dependencies

```bash
sudo dnf install \
python3 \
python3-gobject \
python3-gstreamer1 \
gstreamer1 \
gstreamer1-plugins-base \
gstreamer1-plugins-good \
gstreamer1-plugins-bad-free \
gstreamer1-plugin-mpg123
```

---

# Fedora RPM

amarPlayer has successfully been packaged as an RPM.

Example:

```text
amarPlayer-1.0.0-1.fc44.noarch.rpm
amarPlayer-1.0.0-1.fc44.src.rpm
```

---

# Fedora COPR

Successful COPR builds:

```text
x86_64
aarch64
```

---

# Debian Package

A Debian package was also successfully created:

```text
amarplayer_1.0.0-1_all.deb
```

Packaging configuration:

```text
packaging/debian/
```

---

# Android Port

The Android version is a **port of amarPlayer**, not an unrelated application rewritten from scratch.

The goal is to preserve:

* PySide6 UI
* Playlist logic
* Metadata handling
* Album artwork
* Search
* Application structure

while replacing desktop-specific components.

---

# QtMultimedia

Android playback uses:

```python
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
```

Main components:

```text
QMediaPlayer
QAudioOutput
```

---

# Android Storage

Application data uses:

```python
QStandardPaths.AppDataLocation
```

---

# Android Content URI

Android commonly returns files as:

```text
content://...
```

The Android port includes support for:

* Content URIs
* Android file picker
* Local cache handling
* Preparing selected files for playback

---

# Android ARM64 Build

The first successful Android ARM64 build was produced on:

```text
Fedora Asahi Remix
Apple Silicon
ARM64 / aarch64
```

Target:

```text
arm64-v8a
```

Main configuration:

```text
Android API      : 36
Minimum API      : 24
Architecture     : arm64-v8a
Java             : JDK 21
Android NDK      : r29
```

---

# Fedora Asahi / Apple Silicon

Build host:

```text
Architecture : aarch64
Page Size    : 16384 bytes / 16 KB
```

Some Android SDK tools are distributed only as Linux x86_64 binaries.

One important example is:

```text
aapt2
```

---

# Native ARM64 Android NDK

A native ARM64 Android NDK was used.

Version:

```text
NDK r29
```

Working native tools include:

```text
clang
ld.lld
llvm-ar
llvm-strip
llvm-ranlib
```

---

# AAPT2 and muvm

Running x86_64 AAPT2 directly through FEX on the 16 KB Fedora Asahi host caused compatibility problems.

The successful solution was running Gradle inside **muvm**.

Host:

```text
Page Size = 16384
```

Inside muvm:

```text
Page Size = 4096
```

Build architecture:

```text
Fedora Asahi ARM64
        │
        ▼
      muvm
   4K Page Size
        │
        ▼
      Gradle
        │
        ▼
      AAPT2
        │
        ▼
       APK
```

AAPT2 daemon successfully returned:

```text
Ready
Exiting daemon
```

---

# First Android APK

Successful output:

```text
amarPlayer-debug.apk
```

Approximate size:

```text
174 MB
```

Original path:

```text
.buildozer/android/platform/build-arm64-v8a/
dists/amarPlayer/build/outputs/apk/debug/
amarPlayer-debug.apk
```

---

# Current Android Status

Last tested on 17 September 2026 on an ARM64 phone, model 2510DRA23E.

| Check | Result |
| --- | --- |
| APK update installation | Successful; app data preserved |
| Python and Qt startup | Successful; FFmpeg libraries loaded |
| Application UI | Header, Scan button, playback controls, and playlist displayed |
| MP3 playback | One tap starts playback; elapsed time advances and AudioTrack routes to the speaker |

The old blank-screen issue and the startup failure caused by missing FFmpeg SSL libraries have been fixed. Playback was paused after testing; audible output was not independently checked.

The current APK is `download/amarPlayer-android-arm64-debug.apk` (115.62 MiB / approximately 121 MB). Its minimal Qt bundle includes the SSL and crypto stubs required by FFmpeg.

Runtime audio permissions are handled automatically by the native `AmarPlayerActivity` without relying on Kivy's missing `android.permissions` module, verified on fresh installations on both Android 16 and Android 15 devices. Android supports MP3 only and scans accessible `mp3`, `Music`, and `Download` folders. System volume buttons control the output volume. Playlist swipes and taps that stop kinetic scrolling do not start playback; a deliberate tap on one item plays it, and selected playlist items use high-contrast white text.

---

# Wireless Android Debugging

Wireless ADB can be used without a USB cable.

Pair:

```bash
adb pair IP_ADDRESS:PAIRING_PORT
```

Connect:

```bash
adb connect IP_ADDRESS:DEBUG_PORT
```

Verify:

```bash
adb devices
```

Logs:

```bash
adb logcat
```

---

# Build Cache

Android builds generate a large cache:

```text
.buildozer/
```

It may exceed:

```text
4 GB
```

The build cache is intentionally preserved to avoid rebuilding successfully compiled dependencies.

---

# Git

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

Clone:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
```

Development workflow:

```bash
git add README.md download/ .gitattributes .gitignore
git commit -m "Update amarPlayer"
git push origin main
```

Public packages in `download/`, including the APK, are stored using **Git LFS**. Install Git LFS and run `git lfs install` before cloning; use `git lfs pull --include="download/*"` for an existing clone. Other build archives and caches remain local. Explicitly stage any changed source files when committing.

---

# Milestones

## Linux

```text
Desktop Application       ✅
PySide6 GUI               ✅
GStreamer                 ✅
Playlist                  ✅
Metadata                  ✅
Album Artwork             ✅
Search                    ✅
Shuffle                   ✅
Repeat                    ✅
10-Band Equalizer         ✅
```

## Packaging

```text
Fedora RPM                ✅
Fedora SRPM               ✅
Fedora COPR x86_64        ✅
Fedora COPR aarch64       ✅
Debian Package            ✅
```

## Android

```text
Android Port              ✅
PySide6 Android Wheels    ✅
QtMultimedia              ✅
Content URI               ⚠️ Not fully validated
Native ARM64 NDK          ✅
Python ARM64              ✅
Qt / PySide6 Packaging    ✅
JDK 21                    ✅
Gradle                    ✅
AAPT2 + muvm              ✅
APK Generation            ✅
APK Installation          ✅
Application Launch        ✅
Android UI                ✅ Tested
MP3 Playback              ✅ Tested
```

---

# Roadmap

1. Validate and fix media permission prompts on fresh Android installations.
2. Test scanning, playlists, playback, and player controls on more devices.
3. Validate metadata, album artwork, and `content://` handling.
4. Prepare a stable Android release with release signing.
5. Continue Windows support and provide an EXE installer after testing.

---

# Development Philosophy

amarPlayer started as a personal Linux music-player project.

It gradually evolved into a cross-platform experiment exploring how Python and PySide6 applications can run across different operating systems.

The Linux desktop version remains the reference implementation while Android development continues independently.

---

# License

amarPlayer is distributed under the:

**MIT License**

---

# Developer

**Muammar**

GitHub:

```text
https://github.com/xmuammar
```

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

---

# Current Summary

```text
Linux Desktop        ✅ Working
Fedora RPM           ✅ Built
Fedora COPR          ✅ Built
Debian Package       ✅ Built
Android ARM64 APK    ✅ Built
Android Installation ✅ Working
Android UI           ✅ Tested
Android MP3          ✅ Playback tested
```

The next milestones are validating media permissions on fresh installations and testing stability across more Android devices.
