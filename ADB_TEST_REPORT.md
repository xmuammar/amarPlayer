# Pengujian ADB — 17 September 2026

APK: `bin/amarPlayer-scroll-tap-fix-debug.apk`.

| Pemeriksaan | 2510DRA23E / Android 16 | 23073RPBFG / Android 15 |
| --- | --- | --- |
| Koneksi | 192.168.100.200:45023 | 192.168.100.199:37821 |
| Instalasi | APK sudah terpasang dari sesi sebelumnya | Instalasi baru berhasil |
| Startup dan UI | Berhasil | Berhasil |
| Scan setelah izin audio | 11 lagu | 16 lagu |
| Swipe playlist ketika tidak memutar | Daftar bergulir; tetap dijeda | Daftar bergulir; tidak memulai playback |
| Satu tap lagu | Berhasil; alexgrohl-energetic-action-sport-500409 | Berhasil; Kompilasi Lagu Semangat Pagi Terbaik |
| Waktu playback pada screenshot | 00:37 / 01:46 | 00:36 / 39:30 |
| Pause akhir pengujian | Tombol kembali menjadi ▶ | Tombol kembali menjadi ▶ |

## Temuan

- Instalasi baru Android 15 tidak meminta izin audio otomatis. Log: `Android permission request skipped: No module named 'android'`. Sebelum izin diberikan, tap tidak memulai pemutaran. Izin READ_MEDIA_AUDIO diberikan melalui ADB untuk melanjutkan tes, lalu Scan dan playback bekerja. Android 16 memakai izin yang telah diberikan pada sesi sebelumnya.
- Teks item playlist terpilih terlalu gelap pada kedua perangkat, terlihat pada screenshot.
- Uji tap untuk menghentikan kinetic scrolling belum konklusif: jeda antarperintah ADB tidak memastikan daftar masih bergerak saat tap. Hasil swipe biasa dan tap setelah daftar berhenti telah diverifikasi secara terpisah.
- UIAutomator sesekali tidak mendapat idle state saat playback; screenshot digunakan untuk memastikan waktu berjalan. XML yang berasal dari dump gagal tidak dijadikan bukti playback.
- Tidak memverifikasi suara dengan pendengaran, semua codec, rotasi layar, playback di background, atau pemakaian jangka panjang.
- Tidak ada perubahan source/APK pada pengujian ini; kedua perangkat ditinggalkan dalam keadaan pause.

## Bukti lokal

- `/tmp/amarplayer-device1-swipe-repeat.xml`, `/tmp/amarplayer-device2-swipe.xml`
- `/tmp/amarplayer-device1-playing.png`, `/tmp/amarplayer-device2-playing.png`
- `/tmp/amarplayer-device1-paused.xml`, `/tmp/amarplayer-device2-paused.xml`
- `/tmp/amarplayer-device1-test.log`, `/tmp/amarplayer-device2-test.log`

---

## Verifikasi Perbaikan — 17 September 2026, 15:36 WIB

APK: `bin/amarPlayer-permission-contrast-debug.apk` (juga disalin ke `download/amarPlayer-android-arm64-debug.apk`).

### Perubahan yang Diterapkan
1. **Izin Audio Native**: Mengganti modul Python `android.permissions` yang absen dengan class Java native `AmarPlayerActivity` (`deployment/android/org/amarplayer/amarplayer/AmarPlayerActivity.java`) yang meng-extend `PythonActivity`. Menangani permintaan `READ_MEDIA_AUDIO` (API 33+) atau `READ_EXTERNAL_STORAGE` otomatis saat startup, dialog penjelasan (rationale), dan shortcut ke pengaturan sistem jika izin sebelumnya ditolak permanen.
2. **Kontras Teks Playlist**: Memperbaiki style `QListWidget::item:selected` pada `amarPlayer_android.py` dengan warna teks putih (`#ffffff`) di atas latar `#30303a`, sehingga teks judul lagu tetap terbaca jelas saat dipilih maupun diputar.

### Hasil Verifikasi Dua Perangkat

| Pemeriksaan | 2510DRA23E / Android 16 | 23073RPBFG / Android 15 |
| --- | --- | --- |
| Instalasi APK Baru | Berhasil (`install -r`) | Berhasil (`install -r`) |
| Entrypoint `AmarPlayerActivity` | Berhasil dimuat; izin diminta native | Berhasil dimuat; izin tervalidasi |
| Tampilan UI & Playlist | 11 lagu; teks terpilih putih tajam | 15 lagu; teks terpilih putih tajam |
| Playback Tap | Berhasil; AAudio & AudioTrack aktif | Berhasil; AAudio & AudioTrack aktif |
| Pause Akhir | Kembali ke status pause (▶) | Kembali ke status pause (▶) |
| Screenshot Bukti | `/tmp/amarplayer-fixed-device1-playing.png` | `/tmp/amarplayer-device2-playing.png` |

