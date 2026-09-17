package org.amarplayer.amarplayer;

import android.Manifest;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;
import android.widget.Toast;

import org.kivy.android.PythonActivity;

/** Audio permission handling for the Qt bootstrap, without Kivy/PyJNIus. */
public class AmarPlayerActivity extends PythonActivity {
    private static final int AUDIO_REQUEST = 4701;
    private static final String TAG = "AmarPlayerPermission";
    private static final String CHECKED = "audioPermissionChecked";

    private String audioPermission() {
        return Build.VERSION.SDK_INT >= 33
                ? Manifest.permission.READ_MEDIA_AUDIO
                : Manifest.permission.READ_EXTERNAL_STORAGE;
    }

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        if (state == null || !state.getBoolean(CHECKED, false)) {
            // Let Qt finish attaching its window before showing Android UI.
            getWindow().getDecorView().post(this::checkAudioPermission);
        }
    }

    @Override
    protected void onSaveInstanceState(Bundle state) {
        state.putBoolean(CHECKED, true);
        super.onSaveInstanceState(state);
    }

    private void checkAudioPermission() {
        if (isFinishing() || isDestroyed()
                || checkSelfPermission(audioPermission()) == PackageManager.PERMISSION_GRANTED) {
            return;
        }
        boolean requested = getPreferences(MODE_PRIVATE).getBoolean("audioRequested", false);
        if (requested && !shouldShowRequestPermissionRationale(audioPermission())) {
            new AlertDialog.Builder(this)
                    .setTitle("Akses musik belum diizinkan")
                    .setMessage("Izinkan akses musik dan audio di pengaturan aplikasi, "
                            + "lalu kembali dan ketuk Scan.")
                    .setPositiveButton("Pengaturan", (dialog, which) -> startActivity(
                            new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                                    Uri.parse("package:" + getPackageName()))))
                    .setNegativeButton("Nanti", null)
                    .show();
        } else if (shouldShowRequestPermissionRationale(audioPermission())) {
            new AlertDialog.Builder(this)
                    .setTitle("Izinkan akses musik")
                    .setMessage("amarPlayer memerlukan akses audio untuk mencari dan "
                            + "memutar file MP3 di perangkat ini.")
                    .setPositiveButton("Lanjutkan", (dialog, which) -> requestAudioPermission())
                    .setNegativeButton("Nanti", null)
                    .show();
        } else {
            requestAudioPermission();
        }
    }

    private void requestAudioPermission() {
        getPreferences(MODE_PRIVATE).edit().putBoolean("audioRequested", true).apply();
        requestPermissions(new String[] {audioPermission()}, AUDIO_REQUEST);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] results) {
        if (requestCode != AUDIO_REQUEST) {
            super.onRequestPermissionsResult(requestCode, permissions, results);
            return;
        }
        boolean granted = results.length > 0 && results[0] == PackageManager.PERMISSION_GRANTED;
        Log.i(TAG, granted ? "Audio permission granted" : "Audio permission denied");
        Toast.makeText(this, granted
                ? "Akses musik diizinkan. Ketuk Scan untuk memuat lagu."
                : "Akses musik belum diizinkan. Aktifkan melalui pengaturan aplikasi.",
                Toast.LENGTH_LONG).show();
    }
}
