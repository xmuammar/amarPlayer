# Android audio permission

`org.amarplayer.amarplayer.AmarPlayerActivity` extends the existing Qt
`PythonActivity`. Buildozer includes this directory with `android.add_src` and
uses the subclass as `android.entrypoint`; `main.py` only starts the player.

The Activity requests `READ_MEDIA_AUDIO` on API 33+, or
`READ_EXTERNAL_STORAGE` on older supported versions. It requests no microphone
or video access. Existing grants do not show another prompt. After a denial,
the next launch offers an explanation or a link to app settings when Android
will no longer show its permission prompt. After allowing access, tap Scan.

The implementation uses the native Android permission API because the Qt
bootstrap does not bundle Kivy's `android.permissions` module. See Android's
[runtime permission guide](https://developer.android.com/training/permissions/requesting)
and [granular media permissions](https://developer.android.com/about/versions/13/behavior-changes-13#granular-media-permissions).

Launch the updated APK through its launcher icon or:

```bash
adb -s DEVICE shell am start -W -n org.amarplayer.amarplayer/org.amarplayer.amarplayer.AmarPlayerActivity
```

When reusing an existing Gradle distribution for an incremental build, copy
the Java source into its `src/main/java` tree and update the launcher Activity
in `src/main/AndroidManifest.xml` to the configured entry point. Update the
Python bytecode in `assets/private.tar` and its `private_version` resource too.
A normal Buildozer packaging run obtains the Java source and entry point from
`buildozer.spec`. Preserve the existing distribution and compiled native libraries.
