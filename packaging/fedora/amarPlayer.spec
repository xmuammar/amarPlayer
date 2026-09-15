
Name:           amarPlayer
Version:        1.0.0
Release:        1%{?dist}
Summary:        Modern music player for Linux

License:        MIT
URL:            https://github.com/xmuammar/amarPlayer
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme

Requires:       python3
Requires:       python3-gobject
Requires:       python3-gstreamer1
Requires:       python3-pyside6
Requires:       python3-mutagen
Requires:       python3-pillow

Requires:       gstreamer1
Requires:       gstreamer1-plugins-base
Requires:       gstreamer1-plugins-good
Requires:       gstreamer1-plugins-bad-free
Requires:       gstreamer1-plugin-mpg123

%description
amarPlayer is a modern music player written in Python using
PySide6, PyGObject, and GStreamer.

Features include playlist management, audio metadata,
album artwork, search, shuffle, repeat, and a 10-band
equalizer.

%prep
%autosetup -n %{name}-%{version}

%build
# amarPlayer is a Python application.
# No compilation is required.

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

install -m 0755 amarPlayer.py \
    %{buildroot}%{_bindir}/amarPlayer

install -m 0644 amarPlayer.png \
    %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/amarPlayer.png

cat > %{buildroot}%{_datadir}/applications/amarPlayer.desktop <<EOF
[Desktop Entry]
Name=amarPlayer
Comment=Modern Music Player
Exec=amarPlayer %U
Icon=amarPlayer
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Player;
MimeType=audio/mpeg;audio/flac;audio/wav;audio/ogg;audio/x-ogg;audio/opus;audio/mp4;audio/aac;
Keywords=music;audio;player;mp3;flac;
StartupNotify=true
EOF

desktop-file-validate \
    %{buildroot}%{_datadir}/applications/amarPlayer.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    if [ -x /usr/bin/gtk-update-icon-cache ]; then
        /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    fi
fi

%files
%license
%doc README.md

%{_bindir}/amarPlayer
%{_datadir}/applications/amarPlayer.desktop
%{_datadir}/icons/hicolor/512x512/apps/amarPlayer.png

%changelog
* Mon Sep 15 2026 Muammar <xmuammar@gmail.com> - 1.0.0-1
- Initial amarPlayer RPM package

