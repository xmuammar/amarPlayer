[app]
title = amarPlayer
package.name = amarPlayer
package.domain = org.amarPlayer
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,qml,js
version = 0.1
requirements = python3,shiboken6,PySide6
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.archs = arm64-v8a
android.api = 36
android.minapi = 24
android.allow_backup = True
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false
android.ndk_path = /home/muammar/.android-ndk-arm64/r29
p4a.bootstrap = qt
p4a.local_recipes = /home/muammar/aplikasiMp3/deployment/recipes
p4a.branch = develop
android.permissions = android.permission.CAMERA, android.permission.MODIFY_AUDIO_SETTINGS, android.permission.BLUETOOTH, android.permission.RECORD_AUDIO, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.INTERNET
android.add_jars = /home/muammar/aplikasiMp3/deployment/jar/PySide6/jar/Qt6AndroidBindings.jar,/home/muammar/aplikasiMp3/deployment/jar/PySide6/jar/Qt6AndroidMultimedia.jar,/home/muammar/aplikasiMp3/deployment/jar/PySide6/jar/Qt6Android.jar
p4a.extra_args = --qt-libs=Gui,Multimedia,Widgets,Core --load-local-libs=plugins_multimedia_ffmpegmediaplugin,plugins_multimedia_androidmediaplugin,plugins_platforms_qtforandroid --init-classes=
icon.filename = /home/muammar/.local/lib/python3.14/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[buildozer]
log_level = 2
warn_on_root = 1
bin_dir = /home/muammar/aplikasiMp3

