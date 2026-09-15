[app]

# title of your application
title = amarPlayer

# project root directory. default = The parent directory of input_file
project_dir = .

# source file entry point path. default = main.py
input_file = main.py

# directory where the executable output is generated
exec_directory = .

# path to the project file relative to project_dir
project_file = 

# application icon
icon = /home/muammar/.local/lib/python3.14/site-packages/PySide6/scripts/deploy_lib/pyside_icon.jpg

[python]

# python path
python_path = /usr/bin/python3.11

# python packages to install
packages = Nuitka==4.1.1

# buildozer = for deploying Android application
android_packages = buildozer==1.5.0,cython==0.29.33

[qt]

# paths to required qml files. comma separated
# normally all the qml files required by the project are added automatically
# design studio projects include the qml files using qt resources
qml_files = 

# excluded qml plugin binaries
excluded_qml_plugins = 

# qt modules used. comma separated
modules = Gui,Multimedia,Widgets,Core

# qt plugins used by the application. only relevant for desktop deployment
# for qt plugins used in android application see [android][plugins]
plugins = 

[android]

# path to pyside wheel
wheel_pyside = /home/muammar/aplikasiMp3/android-wheels/pyside6-6.11.2-android_aarch64.whl

# path to shiboken wheel
wheel_shiboken = /home/muammar/aplikasiMp3/android-wheels/shiboken6-6.11.2-android_aarch64.whl

# plugins to be copied to libs folder of the packaged application. comma separated
plugins = multimedia_ffmpegmediaplugin,multimedia_androidmediaplugin,platforms_qtforandroid

[nuitka]

# usage description for permissions requested by the app as found in the info.plist file
# of the app bundle. comma separated
# eg = extra_args = --show-modules --follow-stdlib
macos.permissions = 

# mode of using nuitka. accepts standalone or onefile. default = onefile
mode = onefile

# specify any extra nuitka arguments
extra_args = --quiet --noinclude-qt-translations

[buildozer]

# build mode
# possible values = ["aarch64", "armv7a", "i686", "x86_64"]
# release creates a .aab, while debug creates a .apk
mode = debug

# path to pyside6 and shiboken6 recipe dir
recipe_dir = /home/muammar/aplikasiMp3/deployment/recipes

# path to extra qt android .jar files to be loaded by the application
jars_dir = /home/muammar/aplikasiMp3/deployment/jar/PySide6/jar

# if empty, uses default ndk path downloaded by buildozer
ndk_path = /home/muammar/.pyside6_android_deploy/android-ndk/android-ndk-r27c

# if empty, uses default sdk path downloaded by buildozer
sdk_path = 

# other libraries to be loaded at app startup. comma separated.
local_libs = plugins_multimedia_ffmpegmediaplugin,plugins_multimedia_androidmediaplugin,plugins_platforms_qtforandroid

# architecture of deployed platform
arch = aarch64

