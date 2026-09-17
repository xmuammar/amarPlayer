# Download amarPlayer

Klik nama file untuk mengunduh paket yang sesuai perangkat Anda.
Click a filename to download the package for your device.

| Platform | Download | Ukuran / Size | Keterangan |
| --- | --- | --- | --- |
| Android ARM64 | [amarPlayer-android-arm64-debug.apk](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-android-arm64-debug.apk) | 115.62 MiB | APK debug; perbaikan startup FFmpeg, dialog izin audio native, scrolling/tap playlist, dan pemutaran MP3 diuji pada HP Android 15 & 16. |
| Fedora 44 | [amarPlayer-1.0.0-1.fc44.noarch.rpm](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-1.0.0-1.fc44.noarch.rpm) | 0.03 MiB | Paket RPM noarch versi 1.0.0. |
| Debian / Ubuntu | [amarplayer_1.0.0-1_all.deb](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarplayer_1.0.0-1_all.deb) | 0.02 MiB | Paket DEB versi 1.0.0; membutuhkan dependensi desktop. |
| Linux ARM64 / aarch64 | [amarPlayer-Linux-aarch64.AppImage](https://media.githubusercontent.com/media/xmuammar/amarPlayer/main/download/amarPlayer-Linux-aarch64.AppImage) | 55.74 MiB | AppImage untuk ARM64, bukan x86_64. |

Windows (`.exe`) belum tersedia. Tautan akan ditambahkan setelah installer Windows dibuat dan diuji.
Windows installers are not available yet.

APK Android masih berupa debug build eksperimental. RPM, DEB dan AppImage merupakan build desktop yang sudah tersedia sebelumnya; tidak diuji ulang pada pembaruan Android ini.

## Verifikasi unduhan

Checksum tersedia di [SHA256SUMS](SHA256SUMS). Setelah mengunduh paket dan file checksum ke direktori yang sama:

```bash
sha256sum --check --ignore-missing SHA256SUMS
```

## Untuk pengembang

Paket di folder ini disimpan menggunakan Git LFS agar APK yang melebihi batas ukuran Git biasa dapat diunggah. Gunakan tautan di atas untuk mengunduh langsung; arsip source ZIP tidak selalu menyertakan isi file LFS.

```bash
git lfs install
git clone https://github.com/xmuammar/amarPlayer.git
cd amarPlayer
git lfs pull --include="download/*"
```

Untuk memperbarui paket, salin hasil build yang telah diuji ke `download/`, perbarui checksum dan daftar unduhan, lalu commit dan push. Ekstensi `.rpm`, `.deb`, `.apk`, `.exe`, dan `.AppImage` di folder ini dikonfigurasi menggunakan Git LFS.
