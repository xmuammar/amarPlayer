
# amarPlayer

**amarPlayer** adalah aplikasi pemutar musik desktop yang dikembangkan oleh **Muammar, SST., M.Kom.** menggunakan Python, PySide6, GStreamer, Mutagen, dan Pillow.

amarPlayer dibuat sebagai pemutar musik desktop yang sederhana, modern, ringan, dan dapat dikembangkan untuk berbagai sistem operasi dan arsitektur.

Pengembangan amarPlayer saat ini tidak hanya berfokus pada Linux desktop, tetapi juga mulai diperluas ke **Android**, dengan rencana pengembangan berikutnya menuju platform lain seperti **iOS**.

---

# ✨ Fitur

* Pemutar musik desktop berbasis PySide6
* GStreamer sebagai multimedia backend pada desktop Linux
* QtMultimedia sebagai multimedia backend Android
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
* Equalizer 10-band pada desktop
* Dukungan berbagai format audio
* Membuka file musik melalui command line
* Antarmuka desktop yang sederhana dan responsif
* Port Android menggunakan source terpisah

---

# 🎵 Format Audio

amarPlayer mendukung berbagai format audio melalui backend multimedia yang tersedia pada masing-masing platform:

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

Ketersediaan format tertentu bergantung pada plugin multimedia yang tersedia pada sistem operasi dan platform pengguna.

---

# 🛠️ Teknologi

amarPlayer dikembangkan menggunakan:

* Python 3
* PySide6
* GStreamer
* QtMultimedia
* PyGObject
* Mutagen
* Pillow

### Desktop Linux

Backend multimedia:

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

### Android

Backend multimedia Android telah dipindahkan dari GStreamer ke QtMultimedia:

```text
Python
   │
   ▼
PySide6
   │
   ▼
amarPlayer_android.py
   │
   ▼
QMediaPlayer
   │
   ▼
QAudioOutput
   │
   ▼
Android Audio
```

Pemindahan ini dilakukan agar port Android menggunakan multimedia backend yang sesuai dengan lingkungan Qt Android.

---

# 📂 Struktur Project

```text
amarPlayer/
├── amarPlayer.py
├── amarPlayer_android.py
├── main.py
├── amarPlayer.png
├── amarPlayer-debug.log
├── README.md
├── build-installer.sh
│
├── packaging/
│   ├── debian/
│   │   ├── control
│   │   ├── rules
│   │   ├── changelog
│   │   └── amarPlayer.desktop
│   │
│   └── fedora/
│       └── amarPlayer.spec
│
├── debian/
│   ├── control
│   ├── rules
│   ├── changelog
│   └── amarPlayer.desktop
│
├── android-wheels/
│   ├── pyside6-6.11.2-android_aarch64.whl
│   └── shiboken6-6.11.2-android_aarch64.whl
│
├── release/
│
├── .github/
│   └── workflows/
│       └── build-rpm.yml
│
└── appimagetool-aarch64.AppImage
```

---

# 🖥️ Multi-Platform Architecture

Pengembangan amarPlayer menggunakan source terpisah berdasarkan platform.

```text
                         amarPlayer
                             │
             ┌───────────────┼───────────────┐
             │               │               │
          Desktop          Android           iOS
             │               │               │
    amarPlayer.py   amarPlayer_android.py   Future Port
             │               │
        GStreamer       QtMultimedia
```

`amarPlayer.py` merupakan source utama desktop dan **tidak diubah oleh proses port Android**.

Android menggunakan:

```text
amarPlayer_android.py
```

sedangkan `main.py` digunakan sebagai entry point yang diperlukan oleh sistem deployment Android.

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

Paket:

```text
amarplayer_1.0.0-1_all.deb
```

Architecture:

```text
all
```

Karena aplikasi utama amarPlayer ditulis menggunakan Python dan tidak membawa binary native khusus arsitektur.

## Isi Paket

```text
/usr/bin/amarPlayer
/usr/share/amarPlayer/amarPlayer.py
/usr/share/applications/amarPlayer.desktop
/usr/share/icons/hicolor/512x512/apps/amarPlayer.png
```

## Dependency Debian

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

Dependency tidak dibundel ke dalam file `.deb`. Sistem Debian/Ubuntu akan menangani dependency melalui package manager.

## Build Debian

Environment build menggunakan Podman:

```text
amarplayer-debian-builder
```

Build:

```bash
cd ~/aplikasiMp3 && \
podman exec amarplayer-debian-builder \
bash -lc 'dpkg-buildpackage -us -uc -b'
```

Hasil:

```text
amarplayer_1.0.0-1_all.deb
```

## Instalasi Debian / Ubuntu

```bash
sudo apt install ./amarplayer_1.0.0-1_all.deb
```

Kemudian:

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

---

# 📦 Flatpak

Flatpak direncanakan sebagai format distribusi universal untuk desktop Linux.

Target:

```text
x86_64
aarch64 / ARM64
```

---

# 🏗️ Open Build Service

Open Build Service (OBS) direncanakan sebagai sistem build lintas distribusi.

Target:

```text
Fedora
openSUSE
SUSE Linux Enterprise
Debian
Ubuntu
dan distribusi lain yang didukung OBS
```

---

# 📱 Android

Android sekarang menjadi salah satu target pengembangan aktif amarPlayer.

Port Android dibuat dengan pendekatan **porting source**, bukan membuat aplikasi yang benar-benar terpisah.

Source desktop:

```text
amarPlayer.py
```

tetap dipertahankan.

Source Android:

```text
amarPlayer_android.py
```

digunakan untuk menyesuaikan aplikasi dengan API dan multimedia backend Android.

---

# 🔄 Porting Android

Port Android telah melalui beberapa perubahan utama.

## Backend Multimedia

Desktop:

```text
GStreamer
```

Android:

```text
QMediaPlayer
QAudioOutput
```

Fitur dasar yang sudah dimigrasikan:

```text
Play                  ✅
Pause                 ✅
Stop                  ✅
Seek                  ✅
Duration              ✅
End of media          ✅
Volume                ✅
Error handling        ✅
Playlist              ✅
Close event           ✅
```

GStreamer dan GLib timer **tidak digunakan lagi pada source Android**.

---

# 📂 Android Storage

Android menggunakan mekanisme penyimpanan aplikasi melalui Qt:

```python
QStandardPaths.StandardLocation.AppDataLocation
```

Playlist Android disimpan pada direktori data aplikasi.

Source Android juga telah disiapkan untuk menangani URI Android:

```text
content://
```

Hal ini penting karena Android modern menggunakan Storage Access Framework dan content URI untuk akses file media.

---

# 🎵 Android Media URI

amarPlayer Android mendukung konsep:

```text
content://media/...
```

Source Android memiliki fungsi untuk:

* mendeteksi Android URI
* membaca ekstensi media
* membuka media menggunakan `QFile`
* membaca metadata dari data media
* membuat cache lokal untuk kebutuhan playback
* menyimpan URI ke playlist

Format yang dipertahankan antara lain:

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

---

# 🖼️ Android Metadata dan Album Art

Port Android mempertahankan pembacaan metadata menggunakan Mutagen.

Metadata yang ditangani meliputi:

```text
Title
Artist
Album
Album Art
```

Untuk URI Android, data media dapat dibaca melalui `QFile` dan diproses dari memory buffer.

Album art juga dipertahankan untuk format yang didukung Mutagen.

---

# 🎚️ Equalizer Android

Antarmuka equalizer 10-band tetap dipertahankan.

Namun backend DSP equalizer GStreamer yang digunakan pada desktop belum diaktifkan pada Android.

Status:

```text
Equalizer UI       ✅
Preset UI          ✅
Android DSP        ⏳ Belum diaktifkan
```

Hal ini sengaja dipisahkan agar port Android dapat terlebih dahulu mencapai tahap playback yang stabil.

---

# 📦 Android Build Toolchain

Tool deployment yang digunakan:

```text
pyside6-android-deploy
```

Versi PySide6:

```text
6.11.2
```

Python host yang digunakan untuk deployment:

```text
Python 3.11
```

Python 3.11 diperlukan oleh tool deployment Android yang digunakan dalam project ini.

---

# 🧰 Android Wheels

Wheel Android yang sudah tersedia secara lokal:

```text
android-wheels/
├── pyside6-6.11.2-android_aarch64.whl
└── shiboken6-6.11.2-android_aarch64.whl
```

Target arsitektur Android saat ini:

```text
aarch64 / ARM64
```

Wheel tersebut telah diunduh dan disimpan secara lokal agar tidak perlu diunduh kembali pada proses berikutnya.

---

# 🐍 Python 3.11 Android Deployment

Python 3.11 telah dipasang khusus untuk kebutuhan deployment Android.

Dependency deployment yang telah tersedia:

```text
Jinja2
pkginfo
tqdm
packaging==24.1
```

Host PySide6:

```text
PySide6 6.11.2
```

Host Shiboken:

```text
Shiboken6 6.11.2
```

---

# 📱 Android Entry Point

Tool Android membutuhkan entry point bernama:

```text
main.py
```

Karena itu project memiliki:

```python
import runpy

runpy.run_path(
    "amarPlayer_android.py",
    run_name="__main__"
)
```

`main.py` hanya berfungsi sebagai entry point deployment Android.

Source utama Android tetap:

```text
amarPlayer_android.py
```

---

# 🏗️ Status Android Build

Proses deployment Android **sudah mencapai tahap pemeriksaan toolchain**, tetapi APK belum berhasil dibuat.

Tool deployment mendeteksi kebutuhan Android NDK:

```text
Android NDK r27c
```

Ukuran archive NDK:

```text
±664 MB
```

Pada percobaan pertama, download mencapai:

```text
±105 MB / ±664 MB
```

sebelum proses dihentikan untuk menghemat kuota internet.

File parsial masih tersimpan:

```text
~/.pyside6_android_deploy/android-ndk/android-ndk-r27c-linux.zip
```

Ukuran terakhir yang tercatat:

```text
104988672 bytes
```

Karena file tersebut masih tersedia, proses berikutnya dapat dilanjutkan dari data yang sudah ada apabila toolchain Android kembali dilanjutkan.

---

# ⚠️ Status APK

Saat ini:

```text
Android source       ✅
Android port         ✅
Android wheels       ✅
main.py              ✅
PySide6 host         ✅
Shiboken6 host       ✅
NDK                   🔄 Download tertunda
Android SDK           ⏳ Belum disiapkan
APK                   ⏳ Belum dibangun
```

**amarPlayer Android belum dianggap selesai sampai APK berhasil dibangun dan diuji pada perangkat Android.**

---

# 💻 Windows

Windows juga menjadi salah satu target distribusi amarPlayer.

Target:

```text
Windows x64
Windows ARM64
```

Build Windows dikembangkan melalui CI/CD apabila lingkungan Windows x64 tidak tersedia secara lokal.

Status:

```text
Windows x64     🔄 CI/CD
Windows ARM64   ⏳ Pengembangan
```

---

# ▶️ Menjalankan dari Source

Clone repository:

```bash
git clone https://github.com/xmuammar/amarPlayer.git
cd amarPlayer
```

Desktop:

```bash
python3 amarPlayer.py
```

Android source:

```bash
python3 amarPlayer_android.py
```

Entry point Android:

```bash
python3 main.py
```

Pastikan dependency yang sesuai dengan platform sudah tersedia.

---

# 🐍 Dependensi Python

Dependensi utama:

```text
Python 3
PySide6
PyGObject
Mutagen
Pillow
```

Dependensi multimedia desktop:

```text
GStreamer
GStreamer plugins
```

Backend Android:

```text
QtMultimedia
QMediaPlayer
QAudioOutput
```

Nama paket dapat berbeda antara distribusi Linux.

---

# 📁 Penyimpanan Playlist

## Linux

```text
~/.local/share/amarPlayer/amarPlayer_playlist.json
```

## Android

Android menggunakan:

```text
QStandardPaths.AppDataLocation
```

sehingga data aplikasi mengikuti mekanisme penyimpanan Android.

---

# ⚙️ Konfigurasi

amarPlayer menggunakan direktori data pengguna agar konfigurasi dan playlist tidak bergantung pada lokasi instalasi aplikasi.

Dengan demikian aplikasi yang diinstal secara system-wide tetap memiliki data pengguna yang terpisah.

---

# 🔧 Pengembangan

Source utama:

```text
/home/muammar/aplikasiMp3
```

Repository:

```text
https://github.com/xmuammar/amarPlayer
```

Pengembangan dilakukan secara bertahap:

```text
Source Application
       │
       ├── Linux Desktop
       │      └── RPM / DEB / AppImage / Flatpak
       │
       ├── Android
       │      └── APK
       │
       ├── Windows
       │      └── x64 / ARM64
       │
       └── iOS
              └── Future Port
```

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
11. Pengujian seek
12. Pengujian volume
13. Pengujian perpindahan lagu
14. Pengujian penyimpanan playlist

Pengujian dilakukan secara bertahap pada setiap distribusi, arsitektur, dan platform.

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

## Android

* [x] Android source port
* [x] `amarPlayer_android.py`
* [x] Android `main.py`
* [x] QMediaPlayer
* [x] QAudioOutput
* [x] Play / Pause
* [x] Seek
* [x] Duration
* [x] Volume
* [x] Playlist
* [x] Android `content://` URI handling
* [x] Android data directory
* [x] Android media cache
* [x] Android PySide6 wheel
* [x] Android Shiboken wheel
* [x] Python 3.11 deployment environment
* [ ] NDK r27c
* [ ] Android SDK
* [ ] APK build
* [ ] APK installation test
* [ ] Android runtime testing
* [ ] Android DSP equalizer
* [ ] Android release build

## Windows

* [ ] Windows x64
* [ ] Windows ARM64
* [ ] Automated Windows release

## Future

* [ ] iOS port
* [ ] Automated multi-platform release pipeline
* [ ] Unified release management

---

# 📊 Target Arsitektur

amarPlayer ditujukan untuk beberapa arsitektur:

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
* Android ARM64 devices

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

amarPlayer dikembangkan sebagai project pribadi untuk menghasilkan pemutar musik desktop yang sederhana, praktis, ringan, dan dapat digunakan sehari-hari.

Pengembangan amarPlayer tidak hanya berfokus pada pembuatan aplikasi, tetapi juga pada bagaimana aplikasi tersebut dapat didistribusikan kepada pengguna dari berbagai sistem operasi, distribusi Linux, arsitektur CPU, dan perangkat.

Pengembangan dimulai dari aplikasi desktop Linux, kemudian berkembang ke packaging RPM dan DEB, dan sekarang mulai diperluas ke Android.

Pendekatan pengembangan amarPlayer adalah mempertahankan source desktop yang sudah stabil sambil membuat port khusus untuk platform yang memiliki kebutuhan berbeda.

Target akhirnya adalah:

> **Satu aplikasi, banyak platform, banyak distribusi, banyak arsitektur, dan proses distribusi yang semakin otomatis.**

